import tkinter as tk
from tkinter import ttk, messagebox
import pygame
import random
import os
from PIL import Image, ImageTk

# Initialize Pygame mixer
pygame.mixer.init()

# Get base directory path
BASE_DIR = os.path.dirname(__file__)

# Constants
THEMES = {
    'light': {
        'bg': '#f0f0f0',
        'fg': '#333333',
        'button_bg': '#ffffff',
        'highlight': '#e0e0e0',
        'text': '#000000'
    },
    'dark': {
        'bg': '#2d2d2d',
        'fg': '#ffffff',
        'button_bg': '#404040',
        'highlight': '#505050',
        'text': '#ffffff'
    }
}

FILE_PATHS = {
    'sounds': {
        'start': os.path.join(BASE_DIR, 'sounds', 'start_game.mp3'),
        'end': os.path.join(BASE_DIR, 'sounds', 'end_game.mp3'),
        'win': os.path.join(BASE_DIR, 'sounds', 'win.mp3'),
        'lose': os.path.join(BASE_DIR, 'sounds', 'lose.mp3'),
        'draw': os.path.join(BASE_DIR, 'sounds', 'draw.mp3'),
        'rock': os.path.join(BASE_DIR, 'sounds', 'rock.mp3'),
        'paper': os.path.join(BASE_DIR, 'sounds', 'paper.mp3'),
        'scissors': os.path.join(BASE_DIR, 'sounds', 'scissors.mp3')
    },
    'images': {
        'rock': os.path.join(BASE_DIR, 'images', 'rock.png'),
        'paper': os.path.join(BASE_DIR, 'images', 'paper.png'),
        'scissors': os.path.join(BASE_DIR, 'images', 'scissors.png')
    }
}

class RockPaperScissors:
    def __init__(self, root):
        # Initialize window
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)
        
        # Game state variables
        self.current_theme = "light"
        self.game_mode = "pvc"
        self.player_score = 0
        self.computer_score = 0
        self.round_wins = {"player": 0, "opponent": 0}
        self.current_round = 1
        self.max_rounds = 3
        self.current_go = 1
        self.max_go = 3
        self.go_wins = {"player": 0, "opponent": 0}
        self.player1_choice = None
        self.player2_choice = None
        
        # Initialize components
        self.load_sounds()
        self.load_images()
        self.setup_gui()
        self.play_sound('start')
        
        # Set window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_sounds(self):
        self.sounds = {}
        for name, path in FILE_PATHS['sounds'].items():
            try:
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
                else:
                    print(f"Missing sound file: {path}")
                    self.sounds[name] = None
            except pygame.error as e:
                print(f"Error loading sound {name}: {str(e)}")
                self.sounds[name] = None

    def load_images(self):
        self.images = {}
        for choice, path in FILE_PATHS['images'].items():
            try:
                if os.path.exists(path):
                    img = Image.open(path)
                    self.images[choice] = {
                        'normal': ImageTk.PhotoImage(img.resize((100, 100))),
                        'hover': ImageTk.PhotoImage(img.resize((150, 150)))
                    }
                else:
                    print(f"Missing image file: {path}")
                    # Create placeholder images
                    self.images[choice] = {
                        'normal': tk.PhotoImage(width=100, height=100),
                        'hover': tk.PhotoImage(width=150, height=150)
                    }
            except Exception as e:
                print(f"Error loading image {choice}: {str(e)}")
                self.images[choice] = {
                    'normal': tk.PhotoImage(width=100, height=100),
                    'hover': tk.PhotoImage(width=150, height=150)
                }

    def setup_gui(self):
        # Configure styles
        self.style = ttk.Style()
        self.style.configure('TFrame', background=THEMES[self.current_theme]['bg'])
        
        # Score display
        self.score_frame = ttk.Frame(self.root)
        self.score_frame.pack(fill=tk.X, pady=10)
        
        self.score_var = tk.StringVar()
        self.score_label = ttk.Label(
            self.score_frame,
            textvariable=self.score_var,
            font=('Arial', 14),
            foreground=THEMES[self.current_theme]['text']
        )
        self.score_label.pack(side=tk.LEFT, padx=10)
        self.update_score_display()
        
        # Theme toggle button
        self.theme_btn = ttk.Button(
            self.score_frame,
            text="🌓",
            command=self.toggle_theme
        )
        self.theme_btn.pack(side=tk.RIGHT, padx=10)
        
        # Computer choice display (for PVC mode)
        self.computer_display_frame = ttk.Frame(self.root)
        self.computer_display_frame.pack(pady=10)
        
        self.computer_display_label = ttk.Label(
            self.computer_display_frame,
            text="Computer's Choice:",
            font=('Arial', 12),
            foreground=THEMES[self.current_theme]['text']
        )
        self.computer_display_label.pack()
        
        self.computer_choice_var = tk.StringVar(value="Waiting...")
        self.computer_choice_display = ttk.Label(
            self.computer_display_frame,
            textvariable=self.computer_choice_var,
            font=('Arial', 14, 'bold'),
            foreground=THEMES[self.current_theme]['text']
        )
        self.computer_choice_display.pack()
        
        # Game mode selector
        self.mode_frame = ttk.Frame(self.root)
        self.mode_frame.pack(pady=10)
        
        self.mode_var = tk.StringVar(value="pvc")
        ttk.Radiobutton(
            self.mode_frame,
            text="Player vs Computer",
            variable=self.mode_var,
            value="pvc",
            command=self.change_mode
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Radiobutton(
            self.mode_frame,
            text="Player 1 vs Player 2",
            variable=self.mode_var,
            value="pvp",
            command=self.change_mode
        ).pack(side=tk.LEFT, padx=10)
        
        # Player 1 choices frame
        self.player1_frame = ttk.Frame(self.root)
        self.player1_frame.pack(pady=20, expand=True)
        
        self.player1_label = ttk.Label(
            self.player1_frame,
            text="Player 1",
            font=('Arial', 14),
            foreground=THEMES[self.current_theme]['text']
        )
        self.player1_label.pack()
        
        self.player1_buttons = self.create_choice_buttons(self.player1_frame, "player1")
        
        # Player 2 choices frame (initially hidden)
        self.player2_frame = ttk.Frame(self.root)
        
        self.player2_label = ttk.Label(
            self.player2_frame,
            text="Player 2",
            font=('Arial', 14),
            foreground=THEMES[self.current_theme]['text']
        )
        self.player2_label.pack()
        
        self.player2_buttons = self.create_choice_buttons(self.player2_frame, "player2")
        
        # Result display
        self.result_var = tk.StringVar()
        self.result_label = ttk.Label(
            self.root,
            textvariable=self.result_var,
            font=('Arial', 12),
            foreground=THEMES[self.current_theme]['text'],
            wraplength=500
        )
        self.result_label.pack(pady=20)
        
        # Restart button (explicit black text)
        self.restart_btn = ttk.Button(
            self.root,
            text="Restart Game",
            command=self.restart_game,
            style='BlackText.TButton'
        )
        self.restart_btn.pack(pady=10)
        
        self.apply_theme()
        self.update_interface_for_mode()

    def create_choice_buttons(self, parent_frame, player):
        buttons = {}
        button_frame = ttk.Frame(parent_frame)
        button_frame.pack()
        
        for i, choice in enumerate(['rock', 'paper', 'scissors']):
            btn = ttk.Button(
                button_frame,
                image=self.images[choice]['normal'],
                command=lambda c=choice, p=player: self.player_choice(c, p)
            )
            btn.grid(row=0, column=i, padx=20)
            btn.bind("<Enter>", lambda e, c=choice: self.on_hover(e, c, True))
            btn.bind("<Leave>", lambda e, c=choice: self.on_hover(e, c, False))
            buttons[choice] = btn
        
        return buttons

    def update_interface_for_mode(self):
        if self.game_mode == "pvc":
            self.computer_display_frame.pack()
            self.player2_frame.pack_forget()
            self.player1_label.config(text="Player")
        else:
            self.computer_display_frame.pack_forget()
            self.player2_frame.pack(pady=20, expand=True)
            self.player1_label.config(text="Player 1")

    def update_score_display(self):
        opponent = "Computer" if self.game_mode == "pvc" else "Player 2"
        text = f"Round {self.current_round}/{self.max_rounds} | "
        text += f"Go {self.current_go}/{self.max_go} | "
        text += f"Player: {self.go_wins['player']} | {opponent}: {self.go_wins['opponent']}"
        self.score_var.set(text)

    def on_hover(self, event, choice, enter):
        if self.game_mode == "pvc":
            self.player1_buttons[choice].configure(
                image=self.images[choice]['hover' if enter else 'normal']
            )
        else:
            if event.widget.master == self.player1_buttons[choice].master:
                self.player1_buttons[choice].configure(
                    image=self.images[choice]['hover' if enter else 'normal']
                )
            else:
                self.player2_buttons[choice].configure(
                    image=self.images[choice]['hover' if enter else 'normal']
                )

    def player_choice(self, choice, player):
        # Play choice-specific sound
        if choice in ['rock', 'paper', 'scissors']:
            self.play_sound(choice)
        
        if player == "player1":
            self.player1_choice = choice
            if self.game_mode == "pvc":
                computer_choice = random.choice(['rock', 'paper', 'scissors'])
                self.computer_choice_var.set(computer_choice.capitalize())
                self.determine_winner(choice, computer_choice)
            else:
                if self.player2_choice is not None:
                    self.determine_winner(self.player1_choice, self.player2_choice)
        else:
            self.player2_choice = choice
            if self.player1_choice is not None:
                self.determine_winner(self.player1_choice, self.player2_choice)

    def determine_winner(self, player_choice, opponent_choice):
        if player_choice == opponent_choice:
            result = "draw"
        elif (player_choice == 'rock' and opponent_choice == 'scissors') or \
             (player_choice == 'scissors' and opponent_choice == 'paper') or \
             (player_choice == 'paper' and opponent_choice == 'rock'):
            result = "player"
        else:
            result = "opponent"
        
        self.handle_result(result, player_choice, opponent_choice)

    def handle_result(self, result, player_choice, opponent_choice):
        result_text = f"Player chose {player_choice.capitalize()}, "
        result_text += f"{'Computer' if self.game_mode == 'pvc' else 'Player 2'} chose {opponent_choice.capitalize()}\n"
        
        if result == "draw":
            self.play_sound('draw')
            result_text += "It's a draw!"
        else:
            winner = "Player" if result == "player" else "Computer" if self.game_mode == "pvc" else "Player 2"
            result_text += f"{winner} wins this go!"
            self.play_sound('win' if result == "player" else 'lose')
            
            if result == "player":
                self.go_wins['player'] += 1
            else:
                self.go_wins['opponent'] += 1
        
        self.result_var.set(result_text)
        self.update_score_display()
        
        # Reset choices for next go
        self.player1_choice = None
        self.player2_choice = None
        
        if self.go_wins['player'] + self.go_wins['opponent'] >= self.max_go:
            self.end_go_phase()
        else:
            self.current_go += 1

    def end_go_phase(self):
        round_winner = "player" if self.go_wins['player'] > self.go_wins['opponent'] else "opponent"
        self.round_wins[round_winner] += 1
        
        if self.current_round >= self.max_rounds:
            self.end_game()
        else:
            self.current_round += 1
            self.current_go = 1
            self.go_wins = {"player": 0, "opponent": 0}
            self.update_score_display()
            self.result_var.set(f"Round {self.current_round} starting!")

    def play_sound(self, sound_name):
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        theme = THEMES[self.current_theme]
        self.root.config(bg=theme['bg'])
        
        # Special style for restart button with black text
        self.style.configure('BlackText.TButton', 
                           foreground='#000000',
                           background=theme['button_bg'])
        
        # Update all widgets
        for widget in self.root.winfo_children():
            if isinstance(widget, (ttk.Frame, ttk.Label)):
                widget.configure(style='TFrame')
            if isinstance(widget, ttk.Label):
                widget.configure(foreground=theme['text'])
        
        self.style.configure('TFrame', background=theme['bg'])
        self.style.configure('TButton', 
                           background=theme['button_bg'], 
                           foreground=theme['fg'])
        self.style.map('TButton',
            background=[('active', theme['highlight'])],
            foreground=[('active', theme['fg'])]
        )

    def change_mode(self):
        self.game_mode = self.mode_var.get()
        self.update_interface_for_mode()
        self.restart_game()

    def restart_game(self):
        self.player_score = 0
        self.computer_score = 0
        self.round_wins = {"player": 0, "opponent": 0}
        self.current_round = 1
        self.current_go = 1
        self.go_wins = {"player": 0, "opponent": 0}
        self.player1_choice = None
        self.player2_choice = None
        self.computer_choice_var.set("Waiting...")
        self.update_score_display()
        self.result_var.set("New game started!")
        self.play_sound('start')

    def end_game(self):
        winner = "Player" if self.round_wins['player'] > self.round_wins['opponent'] else "Computer"
        messagebox.showinfo("Game Over", f"{winner} wins the game!")
        self.restart_game()

    def on_close(self):
        self.play_sound('end')
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = RockPaperScissors(root)
    root.mainloop()