import hangman_helper

def update_word_pattern(word, pattern, letter):
    """
    Update the pattern with the guessed letter.

    Args:
        word (str): The word to guess.
        pattern (str): The current pattern.
        letter (str): The guessed letter.

    Returns:
        str: The updated pattern.
    """
    new_pattern = ""
    lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
    for i in range(len(word)):
        if word[i] == letter:
            new_pattern += letter
        elif pattern[i] in lowercase_letters:
            new_pattern += pattern[i]
        else:
            new_pattern += "_"
    return new_pattern

def check_if_finished(pattern):
    """
    Check if the game is finished by checking if the pattern contains any underscores.

    Args:
        pattern (str): The current pattern.

    Returns:
        bool: True if the game is finished, False otherwise.
    """
    for i in pattern:
        if i == "_":
            return True
    return False

def make_pattern(chosen_word):
    """
    Create a pattern of underscores with the same length as the chosen word.

    Args:
        chosen_word (str): The word to guess.

    Returns:
        str: The initial pattern with underscores.
    """
    pattern = "_" * len(chosen_word)
    return pattern

# Add comments to the remaining functions in a similar manner...

def is_letter_valid(letter):
    """
    Check if the guessed letter is valid.

    Args:
        letter (str): The guessed letter.

    Returns:
        bool: True if the letter is valid, False otherwise.
    """
    lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
    if len(letter) > 1 or not letter in lowercase_letters or letter == "":
        print("Your input is invalid, the game will continue to the next round")
        return False
    return True

def is_letter_in_guesses(letter, guesses):
    """
    Check if the guessed letter is already in the list of wrong guesses.

    Args:
        letter (str): The guessed letter.
        guesses (list): List of wrong guesses.

    Returns:
        bool: True if the letter is already guessed, False otherwise.
    """
    if letter in guesses:
        print("You already chose this letter, the game will continue to the next round")
        return True
    return False

def count_letters_in_word(chosen_word, letter):
    """
    Count the occurrences of a letter in the chosen word.

    Args:
        chosen_word (str): The word to guess.
        letter (str): The guessed letter.

    Returns:
        int: Number of occurrences of the letter in the word.
    """
    num_letters = 0
    for i in range(len(chosen_word)):
        if chosen_word[i] == letter:
            num_letters += 1
    return num_letters

def count_underline_in_word(pattern):
    """
    Count the number of underscores in the pattern.

    Args:
        pattern (str): The current pattern.

    Returns:
        int: Number of underscores in the pattern.
    """
    num_letters = 0
    for i in pattern:
        if i == "_":
            num_letters += 1
    return num_letters

def filter_words_list(word, pattern, wrong_guess_lst):
    """
    Filter the list of words based on the pattern and wrong guesses.

    Args:
        word (list): List of words.
        pattern (str): The current pattern.
        wrong_guess_lst (list): List of wrong guesses.

    Returns:
        list: Filtered list of words.
    """
    hint_words = []
    for i in word:
        if len(i) == len(pattern) and not i in wrong_guess_lst:
            hint_words.append(i)
    for i in range(len(pattern)):
        if pattern[i] != "_":
            for j in range(len(hint_words)):
                if hint_words[j][i] != pattern[i]:
                    hint_words.remove(hint_words[j])
    return hint_words

def run_game_round(chosen_word, pattern, wrong_guesses, score, words_list):
    """
    Run one round of the Hangman game.

    Args:
        chosen_word (str): The word to guess.
        pattern (str): The current pattern.
        wrong_guesses (list): List of wrong guesses.
        score (int): Current score.
        words_list (list): List of words.

    Returns:
        tuple: Updated score and pattern.
    """
    hangman_helper.display_state(pattern, wrong_guesses, score, " good luck!")
    input_type, input_value = hangman_helper.get_input()
    if input_type == hangman_helper.LETTER:
        if is_letter_valid(input_value) and not is_letter_in_guesses(input_value, wrong_guesses):
            score -= 1
            if input_value in chosen_word:
                pattern = update_word_pattern(chosen_word, pattern, input_value)
                num_letters = count_letters_in_word(chosen_word, input_value)
                score = score + (num_letters * (num_letters + 1) // 2)
            else:
                wrong_guesses.append(input_value)
    elif input_type == hangman_helper.WORD:
        score -= 1
        if input_value == chosen_word:
            num_letters = count_underline_in_word(pattern)
            pattern = chosen_word
            score += (num_letters * (num_letters + 1) // 2)
        else:
            wrong_guesses.append(input_value)
    elif input_type == hangman_helper.HINT:
        score -= 1
        hint_words = filter_words_list(words_list, pattern, wrong_guesses)
        if len(hint_words) > hangman_helper.HINT_LENGTH:
            fix_hint = []
            for i in range(hangman_helper.HINT_LENGTH):
                if i == 0:
                    fix_hint.append(hint_words[0])
                else:
                    fix_hint.append(hint_words[(i * len(hint_words)) // hangman_helper.HINT_LENGTH])
            hint_words.clear()
            hint_words = fix_hint.copy()
        hangman_helper.show_suggestions(hint_words)
    return score, pattern

def restart_game(words_list):
    """
    Restart the game with a new word and pattern.

    Args:
        words_list (list): List of words.

    Returns:
        tuple: Chosen word, new pattern, and empty list of wrong guesses.
    """
    chosen_word = hangman_helper.get_random_word(words_list)
    pattern = make_pattern(chosen_word)
    wrong_guesses = []
    return chosen_word, pattern, wrong_guesses

def run_single_game(words_list, score):
    """
    Run a single game session until the game is finished.

    Args:
        words_list (list): List of words.
        score (int): Current score.

    Returns:
        int: Final score of the game session.
    """
    chosen_word, pattern, wrong_guesses = restart_game(words_list)
    while score > 0 and check_if_finished(pattern):
        score, pattern = run_game_round(chosen_word, pattern, wrong_guesses, score, words_list)
    if score == 0:
        hangman_helper.display_state(pattern, wrong_guesses, score, "You lost! The chosen word was: " + chosen_word)
    else:
        hangman_helper.display_state(pattern, wrong_guesses, score, "You won!")
    return score

def start_new_game():
    """
    Start a new Hangman game session.

    Returns:
        tuple: Words list, initial score, and number of times played.
    """
    word_list = hangman_helper.load_words()
    score = run_single_game(word_list, hangman_helper.POINTS_INITIAL)
    times_played = 1
    return word_list, score, times_played

def main():
    """
    Main function to start the Hangman game.
    """
    word_list, score, times_played = start_new_game()
    while True:
        if score > 0:
            msg = " Do you want to play one more time?"
            play_again = hangman_helper.play_again("You played " + str(times_played) + " times, You have " + str(score) + " points." + msg)
            if play_again == False:
                break
            score = run_single_game(word_list, score)
            times_played += 1
        else:
            msg = " Do you want to start new game?"
            play_again = hangman_helper.play_again("You played " + str(times_played) + " times, You have " + str(score) + " points." + msg)
            if play_again == False:
                break
            times_played = 0
            score = run_single_game(word_list, hangman_helper.POINTS_INITIAL)

if __name__ == "__main__":
    main()
