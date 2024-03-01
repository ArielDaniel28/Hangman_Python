#################################################################
# FILE : hangman.py
# WRITER : Ariel Daniel , arieldaniel28 , 208500710
# EXERCISE : intro2cse ex4 2022
# STUDENTS I DISCUSSED THE EXERCISE WITH: No one
# WEB PAGES I USED: None
#################################################################
import hangman_helper

def update_word_pattern(word, pattern, letter):
    """The function gets a word, a pattern and a letter and returns an updated pattern that contains the letter"""
    new_pattern=""
    lowercase_letters="abcdefghijklmnopqrstuvwxyz"
    for i in range(len(word)):
        if word[i]==letter:
            new_pattern+=letter
        elif pattern[i] in lowercase_letters:
            new_pattern+=pattern[i]
        else:
            new_pattern+="_"
    return new_pattern

def check_if_finished(pattern):
    """The function gets the current pattern and returns True if the pattern contains the '_' char, else returns False"""
    for i in pattern:
        if i=="_":
            return True
    return False

def make_pattern(chosen_word):
    """The function gets a word and return a pattern (sequence of the char '_') in the same length as the word"""
    pattern="_"*len(chosen_word)
    return pattern

def is_letter_valid(letter):
    """The function gets a letter and return False and print a message if it isn't a lowercase letter or if its longer than one char,
    other return True"""
    lowercase_letters="abcdefghijklmnopqrstuvwxyz"
    if len(letter)>1 or not letter in lowercase_letters or letter=="":
        print("Your input is invalid, the game will continue to the next round")
        return False
    return True

def is_letter_in_guesses(letter, guesses):
    """The function gets a letter and a list of guesses and returns True and print message if the letter is in the list,
    other returns False"""
    if letter in guesses:
        print("You already chose this letter, the game will continue to the next round")
        return True
    return False

def count_letters_in_word(chosen_word, letter):
    """The function gets a string and a letter and return the number of times that the letter occurs in the string """
    num_letters = 0
    for i in range(len(chosen_word)):
        if chosen_word[i] == letter:
            num_letters = num_letters + 1
    return num_letters

def count_underline_in_word(pattern):
    """The function gets a string and returns the number of times that the char '_' occurs in the string"""
    num_letters = 0
    for i in pattern:
        if i == "_":
            num_letters += 1
    return num_letters

def filter_words_list(word, pattern, wrong_guess_lst):
    """The function gets a list of words, a string (pattern) and a list of wrong guesses and returns new list only
     with the words in the same length as 'pattern' and with the same letters at the same places as 'pattern'"""
    hint_words=[]
    for i in word:
        if len(i)==len(pattern) and not i in wrong_guess_lst:
            hint_words.append(i)
    for i in range(len(pattern)):
        if pattern[i]!="_":
            for j in range(len(hint_words)):
                if hint_words[j][i]!=pattern[i]:
                    hint_words.remove(hint_words[j])
    return hint_words

def run_game_round(chosen_word, pattern, wrong_guesses, score, words_list):
    """The function gets the chosen word, a pattern, list of wrong guesses, the score and the words list and run
     one round of the game. In the ends returns the score and the pattern"""
    hangman_helper.display_state(pattern, wrong_guesses, score, " good luck!")
    input_type, input_value = hangman_helper.get_input()
    if input_type == hangman_helper.LETTER:
        if is_letter_valid(input_value) and not is_letter_in_guesses(input_value, wrong_guesses):
            score -= 1
            if input_value in chosen_word:
                pattern = update_word_pattern(chosen_word, pattern, input_value)
                num_letters=count_letters_in_word(chosen_word, input_value)
                score = score + (num_letters * (num_letters + 1) // 2)
            else:
                wrong_guesses.append(input_value)
    elif input_type == hangman_helper.WORD:
        score -= 1
        if input_value == chosen_word:
            num_letters=count_underline_in_word(pattern)
            pattern=chosen_word
            score += (num_letters * (num_letters + 1) // 2)
        else:
            wrong_guesses.append(input_value)
    elif input_type == hangman_helper.HINT:
        score-=1
        hint_words=filter_words_list(words_list, pattern, wrong_guesses)
        if len(hint_words)>hangman_helper.HINT_LENGTH:
            fix_hint=[]
            for i in range(hangman_helper.HINT_LENGTH):
                if i == 0:
                    fix_hint.append(hint_words[0])
                else:
                    fix_hint.append(hint_words[(i*len(hint_words))//hangman_helper.HINT_LENGTH])
            hint_words.clear()
            hint_words=fix_hint.copy()
        hangman_helper.show_suggestions(hint_words)
    return score, pattern

def restart_game(words_list):
    """The function gets the words list and returns one chosen word, new pattern as long as the word and an empty
     list of wrong guesses"""
    chosen_word=hangman_helper.get_random_word(words_list)
    pattern=make_pattern(chosen_word)
    wrong_guesses=[]
    return chosen_word, pattern, wrong_guesses

def run_single_game(words_list, score):
    """The function gets the words list and the current score, run game rounds until the game finish and return the score"""
    chosen_word, pattern, wrong_guesses=restart_game(words_list)
    while score>0 and check_if_finished(pattern):
        score, pattern=run_game_round(chosen_word, pattern, wrong_guesses, score, words_list)
    if score==0:
        hangman_helper.display_state(pattern, wrong_guesses, score, "You lost! The chosen word was: " + chosen_word)
    else:
        hangman_helper.display_state(pattern, wrong_guesses, score, "You won!")
    return score

def start_new_game():
    """The function starts a new game: load the words to the words list, count the times played and keep the score from the game"""
    word_list=hangman_helper.load_words()
    score=run_single_game(word_list, hangman_helper.POINTS_INITIAL)
    times_played=1
    return word_list, score, times_played

def main():
    word_list, score, times_played=start_new_game()
    while True:
        if score>0:
            msg=" Do you want to play one more time?"
            play_again=hangman_helper.play_again("You played " + str(times_played) + " times, You have " + str(score) + " points." + msg)
            if play_again==False:
                break
            score=run_single_game(word_list, score)
            times_played += 1
        else:
            msg=" Do you want to start new game?"
            play_again=hangman_helper.play_again("You played " + str(times_played) + " times, You have " + str(score) + " points." + msg)
            if play_again==False:
                break
            times_played=0
            score=run_single_game(word_list, hangman_helper.POINTS_INITIAL)

if __name__=="__main__":
    main()