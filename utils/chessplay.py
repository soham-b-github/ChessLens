class ChessPlay:
    def __init__(self):
        """print("ChessPlay initialized. Methods available:", [m for m in dir(self) if not m.startswith('__')])"""

    def start_play(self):
        """Start or resume auto-playing through the positions."""
        if not self.is_playing and self.current_index < len(self.fen_list) - 1:
            self.is_playing = True
            self.play_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.auto_play()
    
    def stop_play(self):
        """Stop auto-playing."""
        if self.is_playing:
            self.is_playing = False
            self.play_button.config(state="normal")
            self.stop_button.config(state="disabled")
            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
    
    def auto_play(self):
        """Cycle through positions with a delay and update clocks."""
        if self.is_playing and self.current_index < len(self.fen_list) - 1:
            self.show_next_position()
            active_player = self.get_active_player(self.fen_list[self.current_index])
            if active_player == 'w' and self.white_time > 0:
                self.white_time -= 1
                if self.use_increment:
                    self.white_time += self.increment
                self.update_clocks()
            elif active_player == 'b' and self.black_time > 0:
                self.black_time -= 1
                if self.use_increment:
                    self.black_time += self.increment
                self.update_clocks()
            if self.white_time <= 0 or self.black_time <= 0:
                self.stop_play()
                return
            self.after_id = self.root.after(self.delay, self.auto_play)
        else:
            self.stop_play()
    
    def update_clocks(self):
        """Update clock display."""
        white_mins, white_secs = divmod(max(0, self.white_time), 60)
        black_mins, black_secs = divmod(max(0, self.black_time), 60)
        self.white_clock_label.config(text=f"White: {white_mins:02d}:{white_secs:02d}")
        self.black_clock_label.config(text=f"Black: {black_mins:02d}:{black_secs:02d}")