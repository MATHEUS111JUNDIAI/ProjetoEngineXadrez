import pygame
import chess
from engine import find_best_move

WIDTH = 800
HEIGHT = 800
SQUARE_SIZE = WIDTH // 8
FPS = 60 

WHITE_COLOR = (240, 217, 181)
BLACK_COLOR = (181, 136, 99)

PIECES = {}

def load_images():
    """Carrega as imagens das peças do diretório 'assets' com a sua nomenclatura."""
    pieces_symbols = ['PW', 'RDW', 'NW', 'BW', 'QW', 'KW', 'PB', 'RDB', 'NB', 'BB', 'QB', 'KB']
    for symbol in pieces_symbols:
        PIECES[symbol] = pygame.transform.scale(
            pygame.image.load(f"Assets/{symbol}.png"), (SQUARE_SIZE, SQUARE_SIZE)
        )

def draw_game_state(screen, board):
    """Função principal de desenho que desenha o tabuleiro e as peças."""
    for row in range(8):
        for col in range(8):
            color = WHITE_COLOR if (row + col) % 2 == 0 else BLACK_COLOR
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            
    piece_map = {
        (chess.PAWN, chess.WHITE): 'PW', (chess.PAWN, chess.BLACK): 'PB',
        (chess.ROOK, chess.WHITE): 'RDW', (chess.ROOK, chess.BLACK): 'RDB',
        (chess.KNIGHT, chess.WHITE): 'NW', (chess.KNIGHT, chess.BLACK): 'NB',
        (chess.BISHOP, chess.WHITE): 'BW', (chess.BISHOP, chess.BLACK): 'BB',
        (chess.QUEEN, chess.WHITE): 'QW', (chess.QUEEN, chess.BLACK): 'QB',
        (chess.KING, chess.WHITE): 'KW', (chess.KING, chess.BLACK): 'KB',
    }
    for square_index in chess.SQUARES:
        piece = board.piece_at(square_index)
        if piece is not None:
            symbol = piece_map[(piece.piece_type, piece.color)]
            row = 7 - chess.square_rank(square_index)
            col = chess.square_file(square_index)
            screen.blit(PIECES[symbol], pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def main():
    """Função principal que inicializa o Pygame e roda o loop do jogo interativo."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Engine de Xadrez")
    clock = pygame.time.Clock()
    
    load_images()
    
    board = chess.Board()
    
    player_turn = chess.WHITE 
    search_depth = 3
    player_clicks = [] 

    running = True
    while running:
        is_human_turn = (board.turn == player_turn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and is_human_turn:
                location = pygame.mouse.get_pos()
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                square_index = chess.square(col, 7 - row)
                
                player_clicks.append(square_index)
                if len(player_clicks) == 2:
                    start_square, end_square = player_clicks
                    
                    move = chess.Move(start_square, end_square)
                    if board.piece_at(start_square).piece_type == chess.PAWN and chess.square_rank(end_square) in [0, 7]:
                        move.promotion = chess.QUEEN
                    
                    if move in board.legal_moves:
                        board.push(move)
                        print(f"Jogador fez o lance: {move.uci()}")
                    else:
                        print("Lance ilegal, tente novamente.")
                    
                    player_clicks = []

        if not board.is_game_over() and not is_human_turn:
            print("Engine está pensando...")
            engine_move = find_best_move(board, search_depth)
            print(f"Engine joga: {engine_move.uci()}")
            board.push(engine_move)

        draw_game_state(screen, board)

        pygame.display.flip()
        
        clock.tick(FPS)
        
        if board.is_game_over():
            print("\nFIM DE JOGO!")
            print("Resultado: " + board.result())
            running = False
            
    pygame.time.wait(5000)
    pygame.quit()

if __name__ == "__main__":
    main()