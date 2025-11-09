import chess
import chess.pgn
from engine import Engine
from visualizer import get_advantage_bar, plot_evaluation

def analisar_partida(pgn_file, search_depth):
    engine = Engine()
    eval_history = [0.0]
    with open(pgn_file) as pgn:
        try:
            game = chess.pgn.read_game(pgn)
        except Exception as e:
            print(f"Erro ao ler o arquivo PGN: {e}")
            return

    if game is None:
        print("Não foi possível encontrar uma partida no arquivo PGN.")
        return

    board = game.board()
    move_number = 1
    
    for move in game.mainline_moves():
        if board.turn == chess.WHITE:
            print(f"\nJogada {move_number}. Brancas:")
            move_number += 1
        else:
            print(f"Jogada {move_number -1}. ... Pretas:")
        
        print(f"Lance jogado: {board.san(move)}")
        board.push(move)
        
        score = engine.evaluate_board(board)
        eval_history.append(score)
        bar = get_advantage_bar(score)
        print(f"Avaliação do engine: {score:.2f} {bar}")

        if board.is_game_over():
            print("\nFIM DE JOGO!")
            break
        
        print("Engine pensando...")
        engine_move = engine.find_best_move(board, search_depth)
        print(f"Engine recomendaria: {board.san(engine_move)}")
        print("-----------------------------------")
    
    plot_evaluation(eval_history)

if __name__ == "__main__":
    try:
        with open('partida.pgn'):
            analisar_partida('partida.pgn', search_depth=3)
    except FileNotFoundError:
        print("Erro: Arquivo 'partida.pgn' não encontrado. Por favor, crie este arquivo com uma partida válida.")