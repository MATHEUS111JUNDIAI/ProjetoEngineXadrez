# gui.py
import pygame
import chess
import chess.pgn
import os

# Importamos a classe Engine
from engine import Engine

#  CONFIGURAÇÕES GERAIS 
WIDTH = 800
HEIGHT = 800
SQUARE_SIZE = WIDTH // 8
FPS = 60

# Cores
WHITE_COLOR = (240, 217, 181)
BLACK_COLOR = (181, 136, 99)
HIGHLIGHT_COLOR = (100, 255, 100, 100)
LAST_MOVE_HIGHLIGHT_COLOR = (255, 255, 0, 100)

# Dicionário para carregar as imagens das peças
PIECES = {}

def load_images():
    """Carrega as imagens das peças do diretório 'assets'."""
    assets_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Assets')
    pieces_symbols = ['PW', 'RDW', 'NW', 'BW', 'QW', 'KW', 'PB', 'RDB', 'NB', 'BB', 'QB', 'KB']
    for symbol in pieces_symbols:
        try:
            image_path = os.path.join(assets_path, f"{symbol}.png")
            PIECES[symbol] = pygame.transform.scale(
                pygame.image.load(image_path), (SQUARE_SIZE, SQUARE_SIZE)
            )
        except pygame.error as e:
            print(f"Erro ao carregar a imagem {image_path}: {e}")
            raise SystemExit()

def draw_game_state(screen, board, selected_square, last_move):
    """Função principal de desenho que desenha o tabuleiro e as peças."""
    for row in range(8):
        for col in range(8):
            color = WHITE_COLOR if (row + col) % 2 == 0 else BLACK_COLOR
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    if last_move:
        start_square = last_move.from_square
        end_square = last_move.to_square
        start_row, start_col = 7 - chess.square_rank(start_square), chess.square_file(start_square)
        end_row, end_col = 7 - chess.square_rank(end_square), chess.square_file(end_square)
        
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(LAST_MOVE_HIGHLIGHT_COLOR)
        screen.blit(s, (start_col * SQUARE_SIZE, start_row * SQUARE_SIZE))
        screen.blit(s, (end_col * SQUARE_SIZE, end_row * SQUARE_SIZE))


    if selected_square is not None:
        row, col = 7 - chess.square_rank(selected_square), chess.square_file(selected_square)
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill(HIGHLIGHT_COLOR)
        screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    piece_map = {
        (chess.PAWN, chess.WHITE): 'PW', (chess.PAWN, chess.BLACK): 'PB', (chess.ROOK, chess.WHITE): 'RDW',
        (chess.ROOK, chess.BLACK): 'RDB', (chess.KNIGHT, chess.WHITE): 'NW', (chess.KNIGHT, chess.BLACK): 'NB',
        (chess.BISHOP, chess.WHITE): 'BW', (chess.BISHOP, chess.BLACK): 'BB', (chess.QUEEN, chess.WHITE): 'QW',
        (chess.QUEEN, chess.BLACK): 'QB', (chess.KING, chess.WHITE): 'KW', (chess.KING, chess.BLACK): 'KB',
    }
    for square_index in chess.SQUARES:
        piece = board.piece_at(square_index)
        if piece is not None:
            symbol = piece_map[(piece.piece_type, piece.color)]
            row = 7 - chess.square_rank(square_index)
            col = chess.square_file(square_index)
            screen.blit(PIECES[symbol], pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_game_over(screen, result):
    font = pygame.font.SysFont("Arial", 50)
    text = font.render(f"Fim de Jogo: {result}", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
    screen.blit(text, text_rect)

    font = pygame.font.SysFont("Arial", 30)
    text = font.render("Pressione qualquer tecla para jogar novamente", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))
    screen.blit(text, text_rect)

def start_screen(screen):
    font = pygame.font.SysFont("Arial", 50)
    title = font.render("Chess Engine", True, (0, 0, 0))
    title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/2 - 100))

    font = pygame.font.SysFont("Arial", 30)
    color_text = font.render("Escolha sua cor: (B)rancas ou (P)retas", True, (0, 0, 0))
    color_rect = color_text.get_rect(center=(WIDTH/2, HEIGHT/2))

    depth_text = font.render("Escolha a dificuldade (1-5):", True, (0, 0, 0))
    depth_rect = depth_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))

    screen.fill(WHITE_COLOR)
    screen.blit(title, title_rect)
    screen.blit(color_text, color_rect)
    screen.blit(depth_text, depth_rect)
    pygame.display.flip()

    player_color = None
    search_depth = None

    while player_color is None or search_depth is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    player_color = chess.WHITE
                elif event.key == pygame.K_p:
                    player_color = chess.BLACK
                elif event.unicode.isdigit() and 1 <= int(event.unicode) <= 5:
                    search_depth = int(event.unicode)
    
    return player_color, search_depth


def main():
    """Função principal que inicializa o Pygame e roda o loop do jogo interativo."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Engine de Xadrez")
    clock = pygame.time.Clock()
    
    load_images()
    
    engine = Engine(optimized_file="optimized_constants_opening.json")

    player_turn, search_depth = start_screen(screen)

    board = chess.Board()
    
    player_clicks = []
    selected_square = None
    last_move = None
    game_over = False

    running = True
    while running:
        is_human_turn = (board.turn == player_turn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and not game_over:
                    game = chess.pgn.Game()
                    game.headers["Event"] = "Partida Casual"
                    game.headers["Site"] = "Local"
                    game.headers["Date"] = "????.??.??"
                    game.headers["Round"] = "?"
                    game.headers["White"] = "Jogador Humano" if player_turn == chess.WHITE else "Engine"
                    game.headers["Black"] = "Jogador Humano" if player_turn == chess.BLACK else "Engine"
                    game.headers["Result"] = board.result()

                    node = game
                    for move in board.move_stack:
                        node = node.add_variation(move)

                    save_path = os.path.join(os.path.dirname(__file__), '..', '..', 'partida_salva.pgn')
                    with open(save_path, "w", encoding="utf-8") as pgn_file:
                        exporter = chess.pgn.FileExporter(pgn_file)
                        game.accept(exporter)
                    print("Partida salva em partida_salva.pgn")
            
            if event.type == pygame.MOUSEBUTTONDOWN and is_human_turn and not game_over:
                location = pygame.mouse.get_pos()
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                square_index = chess.square(col, 7 - row)
                
                if selected_square is None:
                    if board.piece_at(square_index) is not None and board.piece_at(square_index).color == board.turn:
                        selected_square = square_index
                else:
                    move = chess.Move(selected_square, square_index)
                    if board.piece_at(selected_square).piece_type == chess.PAWN and chess.square_rank(square_index) in [0, 7]:
                        move.promotion = chess.QUEEN
                    
                    if move in board.legal_moves:
                        board.push(move)
                        last_move = move
                        print(f"Jogador fez o lance: {move.uci()}")
                    else:
                        print("Lance ilegal, tente novamente.")
                    
                    selected_square = None
            
            if event.type == pygame.KEYDOWN and game_over:
                player_turn, search_depth = start_screen(screen)
                board.reset()
                last_move = None
                game_over = False


        if not board.is_game_over() and not is_human_turn and not game_over:
            engine_move = engine.get_engine_move(board, search_depth)
            print(f"Engine joga: {engine_move.uci()}")
            board.push(engine_move)
            last_move = engine_move

        draw_game_state(screen, board, selected_square, last_move)
        
        if board.is_game_over() and not game_over:
            game_over = True
            print("\nFIM DE JOGO!")
            print("Resultado: " + board.result())

        if game_over:
            draw_game_over(screen, board.result())

        pygame.display.flip()
        
        clock.tick(FPS)
            
    pygame.quit()

if __name__ == "__main__":
    main()