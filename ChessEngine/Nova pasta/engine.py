import chess
from constants import piece_value, piece_psts

def evaluate_board(board):
    total_score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            symbol = piece.symbol()
            piece_type = symbol.lower()
            material_score = piece_value[piece_type]
            pst = piece_psts[piece_type]
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

def minimax_alpha_beta(board, depth, alpha, beta, is_maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    if is_maximizing_player:
        max_eval = -9999
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = 9999
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move(board, depth):
    best_move = None
    max_eval = -9999
    alpha = -9999
    beta = 9999
    for move in board.legal_moves:
        board.push(move)
        eval = minimax_alpha_beta(board, depth - 1, alpha, beta, False)
        board.pop()
        if eval > max_eval:
            max_eval = eval
            best_move = move
        alpha = max(alpha, eval)
    return best_move