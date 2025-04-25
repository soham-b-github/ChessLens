import chess 
def validate_fen(fen):
    try:
        board = chess.Board(fen)
        return True, board
    except ValueError as e:
        return False, str(e)