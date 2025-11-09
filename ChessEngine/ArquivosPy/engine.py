# engine.py
import chess
import json
import random
from constants import piece_value, piece_psts as default_parameters

class Engine:
    def __init__(self, optimized_file=None, book_file='book.json'):
        self.piece_psts = {}
        self.opening_book = {}
        self.load_parameters(optimized_file)
        self.load_opening_book(book_file)

    def load_parameters(self, optimized_file=None):
        """Carrega os parâmetros de pontuação (PSTs)."""
        if optimized_file:
            try:
                with open(optimized_file, 'r') as f:
                    self.piece_psts = json.load(f)
                print(f"Carregando parâmetros OTIMIZADOS de '{optimized_file}'...")
                return
            except FileNotFoundError:
                print(f"Aviso: Arquivo otimizado '{optimized_file}' não encontrado.")
        
        self.piece_psts = default_parameters
        print("Carregando parâmetros PADRÃO do engine...")

    def evaluate_board(self, board):
        """Calcula a avaliação usando as tabelas carregadas na memória."""
        total_score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                symbol = piece.symbol()
                piece_type = symbol.lower()
                material_score = piece_value[piece_type]
                pst = self.piece_psts[piece_type]
                positional_score = 0
                if symbol.isupper():
                    positional_score = pst[square]
                else:
                    positional_score = pst[chess.square_mirror(square)]
                if symbol.isupper():
                    total_score += material_score + (positional_score / 100.0)
                else:
                    total_score -= (material_score + (positional_score / 100.0))
        return total_score

    def minimax_alpha_beta(self, board, depth, alpha, beta, is_maximizing_player):
        """Algoritmo de busca."""
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board), None

        best_move = None
        if is_maximizing_player:
            max_eval = -9999
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.minimax_alpha_beta(board, depth - 1, alpha, beta, False)
                board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = 9999
            for move in board.legal_moves:
                board.push(move)
                eval, _ = self.minimax_alpha_beta(board, depth - 1, alpha, beta, True)
                board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def find_best_move(self, board, depth):
        """Interface para o Minimax."""
        _, best_move = self.minimax_alpha_beta(board, depth, -9999, 9999, board.turn == chess.WHITE)
        return best_move

    def load_opening_book(self, book_file='book.json'):
        """Carrega o arquivo book.json."""
        try:
            with open(book_file, 'r') as f:
                self.opening_book = json.load(f)
            print("Livro de aberturas carregado com sucesso!")
        except FileNotFoundError:
            print(f"Aviso: '{book_file}' não encontrado. Usando apenas cálculo.")
            self.opening_book = {}

    def get_book_move(self, board):
        """Consulta o livro de aberturas."""
        current_fen = board.fen()
        if current_fen in self.opening_book:
            moves_with_probs = self.opening_book[current_fen]
            moves = [chess.Move.from_uci(mp[0]) for mp in moves_with_probs]
            weights = [mp[1] for mp in moves_with_probs]
            book_move = random.choices(moves, weights, k=1)[0]
            print(f"Engine jogou o lance do livro: {book_move.uci()}")
            return book_move
        return None

    def get_engine_move(self, board, depth, use_book=True):
        """Função "mestre" que decide o lance do engine."""
        if use_book and board.fullmove_number <= 10:
            book_move = self.get_book_move(board)
            if book_move is not None:
                return book_move
        
        print("Posição não encontrada no livro. Calculando com Minimax...")
        return self.find_best_move(board, depth)