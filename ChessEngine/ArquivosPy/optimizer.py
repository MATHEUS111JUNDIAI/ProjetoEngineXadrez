# optimizer.py
import chess
import chess.pgn
import random
import copy
import json

# Importa as funções e constantes dos nossos outros módulos
from engine import find_best_move
from constants import piece_psts as initial_parameters

def get_test_positions(pgn_file, num_games_to_check=50, max_plies_per_game=40):
    """
    Lê um PGN e extrai TODAS as posições e lances até uma certa profundidade (plies)
    para criar um dataset focado em aberturas.
    """
    positions = []
    print(f"Carregando posições de abertura de até {num_games_to_check} jogos (profundidade máx: {max_plies_per_game} meio-lances)...")
    
    with open(pgn_file, "r", encoding="utf-8") as pgn:
        game_count = 0
        while game_count < num_games_to_check:
            try:
                game = chess.pgn.read_game(pgn)
                if game is None:
                    break
                
                board = game.board()
                # Itera pelos lances do jogo, até o limite definido
                for i, move in enumerate(game.mainline_moves()):
                    if i >= max_plies_per_game:
                        break
                    
                    # Adiciona a posição ATUAL e o lance que foi JOGADO NELA
                    positions.append((board.copy(), move))
                    # Executa o lance para avançar para a próxima posição
                    board.push(move)
                
                game_count += 1
            except (ValueError, IndexError):
                continue # Ignora jogos malformados
                
    print(f"{len(positions)} posições de abertura carregadas com sucesso.")
    return positions

def calculate_fitness(depth, test_positions, current_params):
    """Calcula a "nota de fitness" do engine com os parâmetros atuais."""
    matches = 0
    # Para o teste não ser tão demorado, usamos uma amostra aleatória do nosso grande dataset de aberturas
    sample_size = min(len(test_positions), 100) # Testa em, no máximo, 100 posições por iteração
    sample_positions = random.sample(test_positions, k=sample_size)
    
    for i, (board, master_move) in enumerate(sample_positions):
        engine_move = find_best_move(board, depth, current_params)
        if engine_move == master_move:
            matches += 1
            
    fitness_score = (matches / sample_size) * 100
    return fitness_score

def mutate_parameters(params):
    """Faz uma pequena mutação aleatória em um dos valores das tabelas PST."""
    mutated_params = copy.deepcopy(params)
    piece_to_mutate = random.choice(list(mutated_params.keys()))
    square_to_mutate = random.randint(0, 63)
    mutation_value = random.choice([-5, -3, -1, 1, 3, 5])
    
    mutated_params[piece_to_mutate][square_to_mutate] += mutation_value
    
    print(f"\nMutação: Peça '{piece_to_mutate.upper()}', Casa {chess.SQUARE_NAMES[square_to_mutate]}, Valor {mutation_value}")
    return mutated_params

# --- O LOOP DE OTIMIZAÇÃO (HILL CLIMBING) ---
if __name__ == "__main__":
    
    # Parâmetros do Treinamento
    optimization_iterations = 200 # Quantas tentativas de melhoria
    num_games_for_dataset = 100 # Quantos jogos usar para criar nosso dataset de aberturas
    search_depth_for_test = 3   # Profundidade do engine durante o teste
    opening_depth = 40          # Os primeiros 40 meio-lances (20 de cada jogador)

    # Carrega as posições de teste focadas na abertura
    test_positions = get_test_positions(
        'magnus_games.pgn', 
        num_games_to_check=num_games_for_dataset, 
        max_plies_per_game=opening_depth
    )
    
    # Parâmetros e nota iniciais
    current_params = initial_parameters
    print("\nCalculando a nota de fitness inicial do engine...")
    best_fitness = calculate_fitness(search_depth_for_test, test_positions, current_params)
    print(f"Nota de Fitness Inicial (Aberturas): {best_fitness:.2f}%")

    # Loop de otimização
    for i in range(optimization_iterations):
        print("\n" + "="*40)
        print(f"|  Iteração de Otimização {i+1}/{optimization_iterations} | Melhor Nota Atual: {best_fitness:.2f}%  |")
        print("="*40)
        
        mutated_params = mutate_parameters(current_params)
        
        print("Testando a nova versão (isso pode levar alguns minutos)...")
        new_fitness = calculate_fitness(search_depth_for_test, test_positions, mutated_params)
        print(f"Nota da nova versão: {new_fitness:.2f}%")
        
        if new_fitness > best_fitness:
            print(f"🎉 MELHORA ENCONTRADA! Nota aumentou de {best_fitness:.2f}% para {new_fitness:.2f}%. 🎉")
            current_params = mutated_params
            best_fitness = new_fitness
        else:
            print("Nenhuma melhora. Descartando a mutação.")
    
    print("\n" + "="*40)
    print("Otimização Finalizada!")
    print(f"A melhor nota de fitness alcançada foi: {best_fitness:.2f}%")
    
    # Salva os melhores parâmetros encontrados em um novo arquivo
    with open('optimized_constants_opening.json', 'w') as f:
        json.dump(current_params, f, indent=2)
    print("Os melhores parâmetros de ABERTURA foram salvos em 'optimized_constants_opening.json'")