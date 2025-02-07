# Rock-Paper-Scissors Game

A modern GUI implementation of the classic game with sound effects and multiple game modes.

![Game Screenshot](screenshots\screenshot_1.png) 

![Game Screenshot](screenshots\screenshot_2.png)


## Features

- **Two Game Modes:**
  - Player vs Computer (PvC)
  - Player vs Player (PvP)
- **Immersive Sound Effects:**
  - Choice-specific sounds
  - Win/lose/draw feedback
  - Start/end game music
- **Visual Features:**
  - Dark/Light theme toggle
  - Responsive UI design
  - Clear choice displays
  - Computer choice preview (PvC mode)
- **Game Progression:**
  - 3 goes per round
  - Best-of-3 rounds system
  - Real-time score tracking
- **Additional Features:**
  - Modern minimalist design
  - Cross-platform compatibility
  - Error handling for missing assets

## Technologies Used

- **Python 3.x**
- **Tkinter** (GUI)
- **Pygame** (Sound handling)
- **PIL** (Image processing)

## Installation

1. **Prerequisites:**
- Python 3.x
- Required libraries:
    ```bash
    pip install pygame pillow
    ```

2. **Project Setup:**
   ```bash
   git clone https://github.com/yourusername/rock-paper-scissors.git
   cd rock-paper-scissors
   ```

3. **File Structure:**
    ```bash
    rock-paper-scissors/
    ├── main.py
    ├── images/
    │   ├── rock.png        # 200x200px recommended
    │   ├── paper.png       # 200x200px recommended
    │   └── scissors.png    # 200x200px recommended
    ├── sounds/
    │   ├── start_game.mp3  # Game start sound
    │   ├── end_game.mp3    # Game end sound
    │   ├── win.mp3         # Win sound effect
    │   ├── lose.mp3        # Lose sound effect
    │   ├── draw.mp3        # Draw sound effect
    │   ├── rock.mp3        # Rock selection sound
    │   ├── paper.mp3       # Paper selection sound
    │   └── scissors.mp3    # Scissors selection sound
    └── README.md
    ```

## Usage
1. **Running the Game:**

    ``` bash
    - python main.py
    ```

2. **Game Controls:**

    - **PvC Mode**:

        Click choice buttons to play against computer

    - **PvP Mode**:

        Player 1 (left buttons) vs Player 2 (right buttons)

    - **Theme Toggle:** 🌓 button (top-right)

    - **Restart Game:** Bottom restart button

3. **Game Rules**:

    - Each round consists of 3 goes

    - Win 2 goes to win a round

    - First to win 2 rounds wins the match

    - Ties don't award points


## How to Play
1. **Player vs Computer (PvC):**

    - Click any choice button

    - Computer choice displayed above buttons

    - Results shown immediately

2. **Player vs Player (PvP):**

    - Player 1 uses left-side buttons

    - Player 2 uses right-side buttons

    - Both players make selections

    - Results shown after both choices are made

3. **Score Tracking:**

    Top bar shows:

    - Current round

    - Current go

    - Player/opponent scores

4. **Restarting:**

    - Use restart button at any time

    - Resets all scores and progress

## Credits
- **Game Design:** [Tedd Juma](https://github.com/TeddJuma)

- **Sound Effects:** [pixabay.com](https://pixabay.com/)

- **Images:** [freepik.com](https://www.freepik.com/)

## License
MIT License <br>
more information about the license [here](LICENSE).

## Contributing
Contributions welcome! Please open an issue first to discuss proposed changes.

<br>
Enjoy the game! 🎮✂️📄