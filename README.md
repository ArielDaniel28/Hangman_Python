To run the Hangman game, follow these steps:

1. Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
2. Download the `hangman.py` file from this repository.
3. Open a terminal or command prompt.
4. Navigate to the directory containing `hangman.py`.
5. Run the command: `python hangman.py`.

## How to Play

1. Upon starting the game, you will be prompted to guess letters or the entire word.
2. Enter a lowercase letter to guess a single letter. If the letter is correct, it will be revealed in the hidden word. If incorrect, it will count as a wrong guess.
3. Enter the entire word if you think you know it. Be cautious, as an incorrect guess will count against you.
4. You can request a hint to narrow down the possible words based on the current pattern.
5. The game ends when you correctly guess the word, run out of attempts, or choose to quit.
6. After each game, you will be given the option to play again or start a new game.

## Dependencies

This program utilizes the `hangman_helper` module for input/output handling and game visualization. Ensure that `hangman_helper.py` is present in the same directory as `hangman.py` for the program to run correctly.

## License

This program was written by a student of the Introduction to Computer Science course at the Hebrew University in Jerusalem as part of the course requirements.
