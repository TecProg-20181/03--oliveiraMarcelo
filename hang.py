# -*- coding: utf-8 -*-
import random
import string
import logging
import sys

WORDLIST_FILENAME = "palavras.txt"

def logSys(log, message):
    logger = logging.getLogger('Logger Message')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()    
    ch.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s -%(name)s - %(levelname)s - %(message)s ')

    ch.setFormatter(formatter)

    logger.addHandler(ch)

    if log == 'debug':
        logger.debug(message)
    
    elif log == 'info':
        logger.info(message)
    
    elif log == 'warnnig':
        logger.warn(message)
    
    else:
        logger.error(message)


def loadWords():
    """
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    logSys('info','Arquivo aberto com sucesso!')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return random.choice(wordlist)


def isWordGuessed(secretWord, lettersGuessed):
    secretLetters = []

    for letter in secretWord:
        if letter in lettersGuessed:
            pass
        else:
            return False

    return True


def countLetters(secretWord):
    if secretWord.__class__ is not str:
        logSys('debug','Secret Word não é uma string')

    letters = []

    for letter in secretWord:
        if letter not in letters:
            letters.append(letter)

    return len(letters)

def validateWord(secretWord, guesses):
    maxTries = 20
    tries = 0
    validatedWord = False
    while not validatedWord:
        uniqueLetters = countLetters(secretWord)
        print 'There are', uniqueLetters, 'unique letters in this word.'
        
        if guesses < uniqueLetters:
            print 'Secret word have too many unique letters, reloading'
            secretWord = loadWords()
            tries += 1
            if tries >= maxTries:
                print 'Max of tries, exiting program'
                return None
        else:
            validatedWord = True
    return secretWord

def fillGuesses(secretWord, lettersGuessed):
    guessed = ''
    for letter in secretWord:
        if letter in lettersGuessed:
            guessed += letter
        else:
            guessed += '_ '
    return guessed

def guessLetter(lettersGuessed):
    # 'abcdefghijklmnopqrstuvwxyz'
    available = string.ascii_lowercase
    for letter in available:
        if letter in lettersGuessed:
            available = available.replace(letter, '')

    print 'Available letters', available

def hangman(secretWord):
    
    guesses = 3
    
    secretWord = validateWord(secretWord, guesses)
    if secretWord == None:
        return

    lettersGuessed = []
    print 'Welcome to the game, Hangam!'
    print 'I am thinking of a word that is', len(secretWord), ' letters long.'
    print '-------------'

    while  isWordGuessed(secretWord, lettersGuessed) == False and guesses >0:
        print 'You have ', guesses, 'guesses left.'

        guessLetter(lettersGuessed)         
    
        letter = raw_input('Please guess a letter: ')

        if letter.isdigit():
            logSys('error','Não é uma letra')

        elif letter in lettersGuessed:

            guessed = ''
            guessed = fillGuesses(secretWord, lettersGuessed)

            print 'Oops! You have already guessed that letter: ', guessed
        elif letter in secretWord:
            lettersGuessed.append(letter)
            guessed = fillGuesses(secretWord, lettersGuessed)

            print 'Good Guess: ', guessed
        else:
            guesses -=1
            lettersGuessed.append(letter)
            guessed = fillGuesses(secretWord, lettersGuessed)

            print 'Oops! That letter is not in my word: ',  guessed
        print '------------'

    else:
        if isWordGuessed(secretWord, lettersGuessed) == True:
            print 'Congratulations, you won!'
        else:
            print 'Sorry, you ran out of guesses. The word was ', secretWord, '.'




secretWord = loadWords().lower()
hangman(secretWord)
