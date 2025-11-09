# play.py
import chess
import chess.pgn
import datetime

# Importa a classe Engine
from engine import Engine
from visualizer import plot_evaluation

def main():
    """Função principal que gerencia o loop do jogo interativo."""
    
    # --- CARREGA AS CONFIGURAÇÕES DO ENGINE NO INÍCIO ---
    engine = Engine(optimized_file="optimized_constants_opening.json")

    # Configurações iniciais do jogo
    board = chess.Board()
    search_depth = 3
    
    # Prepara um objeto 'game' para gravar a partida em formato PGN
    game = chess.pgn.Game()
    node = game
    game.headers["Event"] = "Partida Humano vs. Engine"
    game.headers["Site"] = "Local"
    game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")

    # Prepara uma lista para guardar o histórico da avaliação para o gráfico
    eval_history = [0.0]

    # Pergunta ao jogador com qual cor ele quer jogar
    while True:
        player_color_str = input("Você quer jogar com as Brancas (digite 'b') ou Pretas (digite 'p')? ").lower()
        if player_color_str in ['b', 'p']:
            player_is_white = (player_color_str == 'b')
            break
        else:
            print("Entrada inválida. Por favor, digite 'b' ou 'p'.")
    
    # Adiciona os nomes dos jogadores aos cabeçalhos do PGN
    if player_is_white:
        game.headers["White"] = "Humano"
        game.headers["Black"] = "Engine"
    else:
        game.headers["White"] = "Engine"
        game.headers["Black"] = "Humano"


    # Loop principal do jogo: continua enquanto o jogo não acabar
    while not board.is_game_over():
        print("\n" + "="*30)
        print(board)
        print("="*30)
        
        move = None
        # Esta é a linha completa para verificar se é a vez do jogador humano
        is_player_turn = (board.turn == chess.WHITE and player_is_white) or \
                         (board.turn == chess.BLACK and not player_is_white)

        if is_player_turn:
            # Loop para garantir que o jogador faça um lance válido
            while True:
                try:
                    move_san = input("Seu lance (ex: e4, Nf3, O-O): ")
                    move = board.parse_san(move_san)
                    break # Se o lance foi válido, sai do loop
                except ValueError:
                    print("Lance inválido ou ilegal! Tente novamente.")
        else: # Turno do Engine
            # A chamada ao engine, agora mais simples
            engine_move = engine.get_engine_move(board, search_depth)
            move = engine_move
            move_san = board.san(move)
            print(f"Engine joga: {move_san}")
        
        # Executa o lance no tabuleiro
        board.push(move)
        # Adiciona o lance à nossa gravação da partida
        node = node.add_variation(move)
        
        # Calcula a pontuação e adiciona ao histórico para o gráfico
        score = engine.evaluate_board(board)
        eval_history.append(score)

    # Seção de Pós-Jogo
    print("\n======== FIM DE JOGO! ========")
    result = board.result()
    print("Resultado: " + result)
    print("="*30)
    print(board)
    
    game.headers["Result"] = result

    # Gera nomes de arquivo únicos usando data e hora
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pgn_filename = f"partida_vs_engine_{timestamp}.pgn"
    graph_filename = f"grafico_avaliacao_{timestamp}.png"

    # Salva a partida jogada em um arquivo PGN
    with open(pgn_filename, "w", encoding="utf-8") as pgn_file:
        exporter = chess.pgn.FileExporter(pgn_file)
        game.accept(exporter)
    print(f"\nPartida salva com sucesso em '{pgn_filename}'")

    # Gera o gráfico da partida que acabamos de jogar
    plot_evaluation(eval_history, graph_filename)
    
# Ponto de entrada do script
if __name__ == "__main__":
    main()