import chess
import chess.engine
import chess.svg
import random

# Piece value table for evaluation
piece_values = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 1000
}


def evaluate_board(board):
    eval = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            value = piece_values.get(piece.piece_type, 0)
            eval += value if piece.color == chess.WHITE else -value
    return eval

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)

    if maximizing_player:
        max_eval = float('-inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = float('inf')
        for move in legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def get_best_move(board, depth):
    best_move = None
    max_eval = float('-inf')

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, float('-inf'), float('inf'), False)
        board.pop()

        if eval > max_eval:
            max_eval = eval
            best_move = move

    return best_move
def play_game():
    board = chess.Board()
    print(board)

    while not board.is_game_over():
        if board.turn == chess.WHITE:
            print("\nYour Turn (WHITE):")
            print(board)
            move = input("Enter your move (e.g., e2e4): ")
            try:
                board.push_san(move)
            except:
                print("Invalid move. Try again.")
        else:
            print("\nAI's Turn (BLACK): Thinking...")
            move = get_best_move(board, 3)  # Depth 3
            print("AI played:", move)
            board.push(move)

        print(board)

    print("Game Over:", board.result())


if __name__ == "__main__":
    play_game()
