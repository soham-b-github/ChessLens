import tkinter as tk
from PIL import Image, ImageTk
import cairosvg
import io
import chess
import chess.svg
from updateboard import ChessBoard
from chessplay import ChessPlay
from tkinter import simpledialog, messagebox, ttk

class ChessViewer(ChessBoard, ChessPlay):
    def __init__(self, fen_list, white_player, black_player, delay=4000):
        # Initialize parent classes
        ChessBoard.__init__(self)
        ChessPlay.__init__(self)
        
        # Verify method availability
        """print("ChessViewer initialized. Methods available:", [m for m in dir(self) if not m.startswith('__')])"""
        if not hasattr(self, 'show_previous_position'):
            raise AttributeError("show_previous_position not found in ChessViewer")
        
        self.fen_list = [fen.strip() for fen in fen_list]
        self.current_index = 0
        self.delay = delay
        self.is_playing = True
        self.after_id = None
        self.white_player = white_player
        self.black_player = black_player
        
        # Initialize tkinter window
        self.root = tk.Tk()
        self.root.title("ChessLens")
        
        # Get time control settings
        self.setup_time_control()
        
        # Position window on the right side of the screen
        screen_width = self.root.winfo_screenwidth()
        window_width = 1000
        window_height = 800
        x_position = screen_width - window_width - 10
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+10")
        
        # Main frame to hold board and clocks
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)
        
        # Clock frames
        self.black_clock_frame = tk.Frame(self.main_frame)
        self.black_clock_frame.grid(row=0, column=2, padx=20, sticky='n')  # Top right
        self.white_clock_frame = tk.Frame(self.main_frame)
        self.white_clock_frame.grid(row=1, column=2, padx=20, sticky='s')  # Bottom right
        
        # Clock labels
        self.white_clock_label = tk.Label(self.white_clock_frame, text="White: 00:00", font=("Elephant", 14))
        self.white_clock_label.pack()
        self.black_clock_label = tk.Label(self.black_clock_frame, text="Black: 00:00", font=("Elephant", 14))
        self.black_clock_label.pack()
        
        # Create canvas for chessboard
        self.board_canvas = tk.Canvas(self.main_frame, width=650, height=650)
        self.board_canvas.grid(row=0, column=1, rowspan=2)
        
        # Create labels for player names
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(pady=5)
        self.white_label = tk.Label(self.player_frame, text=f"White: {self.white_player}", font=("Elephant", 12))
        self.white_label.pack(side=tk.LEFT, padx=10)
        self.black_label = tk.Label(self.player_frame, text=f"Black: {self.black_player}", font=("Elephant", 12))
        self.black_label.pack(side=tk.LEFT, padx=10)
        
        # Create button frame
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=5)
        
        # Create buttons
        self.back_button = tk.Button(self.button_frame, text="Back", command=self.show_previous_position)
        self.back_button.grid(row=0, column=0, padx=5)
        
        self.forward_button = tk.Button(self.button_frame, text="Forward", command=self.show_next_position)
        self.forward_button.grid(row=0, column=1, padx=5)
        
        self.play_button = tk.Button(self.button_frame, text="Play", command=self.start_play)
        self.play_button.grid(row=0, column=2, padx=5)
        self.play_button.config(state="disabled")
        
        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_play)
        self.stop_button.grid(row=0, column=3, padx=5)
        self.stop_button.config(state="normal")
        
        # Initialize image
        self.photo = None
        self.update_clocks()
        self.display_position()
        
        # Start auto-play
        self.auto_play()
    
    def setup_time_control(self):
        """Prompt for time control settings."""
        # Create a dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Time Control")
        dialog.geometry("250x320")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Time unit selection
        tk.Label(dialog, text="Time control:").pack(pady=5)
        unit_var = tk.StringVar(value="minutes")
        ttk.Combobox(dialog, textvariable=unit_var, values=["minutes", "seconds"], state="readonly").pack()
        
        # Time value input
        tk.Label(dialog, text="Time per player:").pack(pady=5)
        time_entry = tk.Entry(dialog)
        time_entry.pack()
        
        # Increment option
        tk.Label(dialog, text="increment?").pack(pady=5)
        increment_var = tk.StringVar(value="no")
        tk.Radiobutton(dialog, text="Yes", variable=increment_var, value="yes").pack()
        tk.Radiobutton(dialog, text="No", variable=increment_var, value="no").pack()
        
        # Increment value input
        tk.Label(dialog, text="Increment (seconds):").pack(pady=5)
        increment_entry = tk.Entry(dialog)
        increment_entry.pack()
        
        def submit():
            try:
                time_value = int(time_entry.get())
                if time_value <= 0:
                    raise ValueError("Time must be positive")
                unit = unit_var.get()
                self.white_time = time_value * 60 if unit == "minutes" else time_value
                self.black_time = self.white_time
                self.use_increment = increment_var.get() == "yes"
                if self.use_increment:
                    increment = int(increment_entry.get())
                    if increment < 0:
                        raise ValueError("Increment cannot be negative")
                    self.increment = increment
                else:
                    self.increment = 0
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))
        
        tk.Button(dialog, text="Submit", command=submit).pack(pady=10)
        self.root.wait_window(dialog)
        if not hasattr(self, 'white_time'):
            # Default to 10 minutes if dialog closed
            self.white_time = 10 * 60
            self.black_time = 10 * 60
            self.use_increment = False
            self.increment = 0
    
    def generate_board_image(self, board):
        """Generate a PNG image from a chess board."""
        svg_data = chess.svg.board(board, size=650)
        png_data = io.BytesIO()
        cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=png_data)
        image = Image.open(png_data)
        return image
    
    def display_position(self):
        """Display the current FEN position and update clocks."""
        if self.current_index >= len(self.fen_list):
            self.board_canvas.delete("all")
            self.stop_play()
            return
        
        if self.current_index < 0:
            self.current_index = 0
        
        fen = self.fen_list[self.current_index]
        is_valid, result = self.validate_fen(fen)
        
        if is_valid:
            board = result
            try:
                image = self.generate_board_image(board)
                self.photo = ImageTk.PhotoImage(image)
                self.board_canvas.delete("all")
                self.board_canvas.create_image(325, 325, image=self.photo)
            except Exception as e:
                self.board_canvas.delete("all")
                print(f"Render error for FEN at index {self.current_index}: {e}")
        else:
            self.board_canvas.delete("all")
            print(f"Validation error for FEN at index {self.current_index}: {result}")
        
        # Update clocks for manual navigation
        active_player = self.get_active_player(fen)
        if active_player == 'w' and self.white_time > 0:
            self.white_time -= 1
            if self.use_increment:
                self.white_time += self.increment
        elif active_player == 'b' and self.black_time > 0:
            self.black_time -= 1
            if self.use_increment:
                self.black_time += self.increment
        self.update_clocks()
        if self.white_time <= 0 or self.black_time <= 0:
            self.stop_play()
            messagebox.showinfo("Game Over", "Time's up!")
    
    def show_next_position(self):
        """Show the next position and update clocks."""
        super().show_next_position()
    
    def show_previous_position(self):
        """Show the previous position and update clocks."""
        super().show_previous_position()
    
    def run(self):
        """Start the tkinter main loop."""
        self.root.mainloop()