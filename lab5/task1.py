import chess

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 100
}

def evaluate_board(board):
    score = 0
    for piece_type in PIECE_VALUES:
        score += len(board.pieces(piece_type, chess.WHITE)) * PIECE_VALUES[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * PIECE_VALUES[piece_type]
    return score

def beam_search_best_move(board, beam_width, depth_limit):
    beam = [(evaluate_board(board), [], board.copy())]

    for depth in range(depth_limit):
        candidates = []
        current_turn = board.turn if depth % 2 == 0 else not board.turn

        for score, sequence, state in beam:
            for move in state.legal_moves:
                new_state = state.copy()
                new_state.push(move)
                new_score = evaluate_board(new_state)
                new_sequence = sequence + [move]
                candidates.append((new_score, new_sequence, new_state))

        # Sort by score, considering whose turn it is
        candidates.sort(key=lambda x: x[0], reverse=current_turn == chess.WHITE)
        beam = candidates[:beam_width]

    if not beam:
        return []

    best_score, best_sequence, _ = beam[0]
    return [(move.uci(), best_score) for move in best_sequence]

board = chess.Board()
beam_width = 5
depth_limit = 3

best_moves = beam_search_best_move(board, beam_width, depth_limit)
print("Best moves:", best_moves)