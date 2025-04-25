import chess
import chess.svg
import io
from FEN import validate_fen

class ChessBoard:
    def __init__(self):
        self.current_index = 0
        self.fen_list = []
        #print("ChessBoard initialized. Methods available:", [m for m in dir(self) if not m.startswith('__')])

    def validate_fen(self, fen):
        """Validate a FEN string."""
        return validate_fen(fen)
    
    def get_active_player(self, fen):
        """Determine the active player from FEN (w or b)."""
        try:
            board = chess.Board(fen)
            return 'w' if board.turn == chess.WHITE else 'b'
        except ValueError:
            return None
    
    def show_next_position(self):
        """Show the next position in the list."""
        self.current_index += 1
        self.display_position()
    
    def show_previous_position(self):
        """Show the previous position in the list."""
        self.current_index -= 1
        self.display_position()