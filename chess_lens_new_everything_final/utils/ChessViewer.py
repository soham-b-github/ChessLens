import tkinter as tk
from PIL import Image, ImageTk
import cairosvg
import io
import chess
import chess.svg

class ChessViewer:
    def __init__(self, fen, white_player="Unknown", black_player="Unknown"):
        self.fen = fen.strip()
        self.white_player = white_player
        self.black_player = black_player
        
        # Initialize tkinter window
        self.root = tk.Tk()
        self.root.title("ChessLens")
        
        # Position window on the right side of the screen
        screen_width = self.root.winfo_screenwidth()
        window_width = 1000
        window_height = 800
        x_position = screen_width - window_width - 10
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+10")
        
        # Main frame to hold board
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)
        
        # Create canvas for chessboard
        self.board_canvas = tk.Canvas(self.main_frame, width=650, height=650)
        self.board_canvas.pack()
        
        # Create labels for player names
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(pady=5)
        self.white_label = tk.Label(self.player_frame, text=f"White: {self.white_player}", font=("Elephant", 12))
        self.white_label.pack(side=tk.LEFT, padx=10)
        self.black_label = tk.Label(self.player_frame, text=f"Black: {self.black_player}", font=("Elephant", 12))
        self.black_label.pack(side=tk.LEFT, padx=10)
        
        # Initialize image
        self.photo = None
        self.display_position()

    def generate_board_image(self, board):
        """Generate a PNG image from a chess board."""
        svg_data = chess.svg.board(board, size=650)
        png_data = io.BytesIO()
        cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=png_data)
        image = Image.open(png_data)
        return image
    
    def display_position(self):
        """Display the provided FEN position."""
        try:
            board = chess.Board(self.fen)
            image = self.generate_board_image(board)
            self.photo = ImageTk.PhotoImage(image)
            self.board_canvas.delete("all")
            self.board_canvas.create_image(325, 325, image=self.photo)
        except Exception as e:
            self.board_canvas.delete("all")
            print(f"Error rendering FEN: {self.fen}: {e}")
    
    def run(self):
        """Start the tkinter main loop."""
        self.root.mainloop()
