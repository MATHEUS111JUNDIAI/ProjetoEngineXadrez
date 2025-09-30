import chess
import chess.pgn 
import datetime 
from engine import find_best_move, evaluate_board
from visualizer import plot_evaluation

def main():
    """
    Função principal que roda o loop do jogo, agora com salvamento e análise.
    """
    board = chess.Board()
    search_depth = 3
    game = chess.pgn.Game()
    game.headers["Event"] = "Partida Humano vs. Engine"
    game.headers["Site"] = "Local"
    game.headers["Date"] = datetime.datetime.now().strftime("%Y.%m.%d")
    node = game
    eval_history = [0.0]

    while True:
        player_color_str = input("Você quer jogar com as Brancas (digite 'b') ou Pretas (digite 'p')? ").lower()
        if player_color_str in ['b', 'p']:
            player_is_white = (player_color_str == 'b')
            break
        else:
            print("Entrada inválida. Por favor, digite 'b' ou 'p'.")

    if player_is_white:
        game.headers["White"] = "Humano"
        game.headers["Black"] = "Engine"
    else:
        game.headers["White"] = "Engine"
        game.headers["Black"] = "Humano"

    while not board.is_game_over():
        print("\n" + "="*30)
        print(board)
        print("="*30)
        
        move = None
        is_player_turn = (board.turn == chess.WHITE and player_is_white) or \
                         (board.turn == chess.BLACK and not player_is_white)

        if is_player_turn:
            while True:
                try:
                    move_san = input("Seu lance (ex: e4, Nf3, O-O): ")
                    move = board.parse_san(move_san)
                    break
                except ValueError:
                    print("Lance inválido ou ilegal! Tente novamente.")
        else:
            print("\nEngine está pensando...")
            move = find_best_move(board, search_depth)
            move_san = board.san(move)
            print(f"Engine joga: {move_san}")
        
        board.push(move)
        node = node.add_variation(move)
        score = evaluate_board(board)
        eval_history.append(score)

    print("\n======== FIM DE JOGO! ========")
    result = board.result()
    print("Resultado: " + result)
    print("==============================")
    print(board)
    
    game.headers["Result"] = result

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pgn_filename = f"partida_vs_engine_{timestamp}.pgn"
    graph_filename = f"grafico_avaliacao_{timestamp}.png"

    with open(pgn_filename, "w", encoding="utf-8") as pgn_file:
        exporter = chess.pgn.FileExporter(pgn_file)
        game.accept(exporter)
    print(f"\nPartida salva com sucesso em '{pgn_filename}'")

    plot_evaluation(eval_history, graph_filename)
    plot_evaluation(eval_history)

if __name__ == "__main__":
    main()