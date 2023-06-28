import random
import re
import requests
from typing import Callable
from illustration_to_game import draw
from classes import TerminalView
from logger import get_logging

logger_ = get_logging(__name__)

game_commands = TerminalView()
game_commands_comm = '''
    Type "play" to play the game, "score" to show the scoreboard, "help" to show instructions
    and "back" to return to main menu.'''
game_commands.add_command(game_commands_comm)


'''def choose() -> tuple:
    word_list: list = ['python', 'java', 'swift', 'javascript', 'ruby', 'html', 'php']
    word: str = random.choice(word_list)
    gues_word: str = '-' * len(word)
    return word, gues_word'''


def get_words_list() -> list:
    logger_.info('Function get_words_list: creating list of words')
    response = requests.get('https://www.mit.edu/~ecprice/wordlist.10000', timeout=10)
    string_words: str = response.content.decode('utf-8')
    list_words: list = string_words.splitlines()
    return list_words


words: list = get_words_list()
score = dict(win=0, loose=0)


def game() -> None:  # -> tuple:
    # word, gues_word = choose()
    logger_.info('Start the game!')
    word: str = random.choice(words)
    gues_word: str = '-' * len(word)
    i: int = 0
    entered_letters: str = ''
    while i < 8 and gues_word != word:
        print('\n' + gues_word)
        letter: str = input('Input a letter: ')
        letter = check_enter_by_error(letter)
        if letter:
            i_res, gues_word = check_letter(entered_letters, gues_word, letter, word, i)
            i = i_res
    result(word, gues_word)


def check_letter(entered_letters: str, gues_word: str, letter: str, word: str, i: int) -> tuple:
    logger_.info('checking entered letter')
    entered_letters += letter
    if entered_letters.count(letter) > 1:
        print("You have already guessed this letter.")
    elif letter in word:
        gues_word = show_changes(word, letter, gues_word)
    else:
        print(f"The letter {letter} doesn't present in the word.")
        i += 1
        draw(i)
    return i, gues_word


def result(word: str, guested_word: str):  # -> tuple:
    logger_.info('Function result')
    if word != guested_word:
        print(f'\nYou lost! The word was {word}')
        score['loose'] += 1
    else:
        print(f'\nYou guessed the word: {word}! \nYou survived!')
        score['win'] += 1


def show_changes(wrd: str, let: str, str_: str) -> str:
    logger_.info('Function show_changes')
    str_: list = list(str_)
    for i in range(len(wrd)):
        if wrd[i] == let:
            str_[i] = wrd[i]
    return ''.join(str_)


def check_enter_by_error(let: str) -> str:
    logger_.info(f'checking enter values: {let}')
    pattern = re.compile(r'[a-z]')
    matches = re.search(pattern, let)
    if matches:
        return let
    elif len(let) == 1 and (let.isupper() or let.isascii()):
        print('Please, enter a lowercase letter from the English alphabet.')
    else:
        print('Please, input a single letter.')


def instructions_game() -> None:
    logger_.info('Function instructions_game')
    for command in game_commands.display_commands():
        print(command)


def greeting_game() -> None:
    print('''\n\tH A N G M A N
        This is entertainment module with a well known game - hangman. So are you ready to gues a word?''')


def show_score() -> None:
    logger_.info('Function show_score')
    print(f'\nYou won: {score["win"]} times.\nYou lost: {score["loose"]} times.')


functions = {'play': game, 'score': show_score, 'help': instructions_game}


def handler(command: str) -> Callable:
    try:
        return functions[command]()
    except KeyError as error:
        logger_.error(f'Error was occurred: {error}')
        print('I do not understand what you want. Please look at instructions.')


def game_main():
    logger_.info('game module is started')
    greeting_game()
    instructions_game()
    while True:
        answer = input('\nMake your choice: ')
        if answer == 'back':
            print('\nYou returned to the main Menu.')
            break
        handler(answer)
