import pygame
from math import sqrt
from os import path
from random import randint


pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("Comic Sans MS", 15)
BIG_FONT = pygame.font.SysFont("Comic Sans MS", 30)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 600
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hangman")
CIRCLE_CENTRES = [(45, 50), (90, 50), (135, 50), (180, 50), (225, 50), (270, 50), (315, 50),
                  (360, 50), (405, 50), (450, 50), (495, 50), (540, 50), (585, 50),
                  (45, 100), (90, 100), (135, 100), (180, 100), (225, 100), (270, 100), (315, 100),
                  (360, 100), (405, 100), (450, 100), (495, 100), (540, 100), (585, 100)]
CIRCLE_RADIUS = 20
CIRCLE_WIDTH = 1
GUESSED_LETTER_COORDS = (45, 500)
HANGMAN_COORDS = (50, 130)  # That means the hangman end coords are (306, 386)
alphabet = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L", 13: "M",
            14: "N", 15: "O", 16: "P", 17: "Q", 18: "R", 19: "S", 20: "T", 21: "U", 22: "V", 23: "W", 24: "X", 25: "Y",
            26: "Z"}

stage1 = pygame.image.load(path.join('img', 'Hangman stages', '1.png'))
stage2 = pygame.image.load(path.join('img', 'Hangman stages', '2.png'))
stage3 = pygame.image.load(path.join('img', 'Hangman stages', '3.png'))
stage4 = pygame.image.load(path.join('img', 'Hangman stages', '4.png'))
stage5 = pygame.image.load(path.join('img', 'Hangman stages', '5.png'))
stage6 = pygame.image.load(path.join('img', 'Hangman stages', '6.png'))
stage7 = pygame.image.load(path.join('img', 'Hangman stages', '7.png'))
stage8 = pygame.image.load(path.join('img', 'Hangman stages', '8.png'))
words = open('Words.txt', 'r')

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (150, 150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

guessedLetters = ""
hangmanStage = 0
letterSpaces = []
stageToPicture = {1: stage1, 2: stage2, 3: stage3, 4: stage4, 5: stage5, 6: stage6, 7: stage7, 8: stage8}


def click(x, y):
    alphabetCounter = 1
    for centre in CIRCLE_CENTRES:
        distance = sqrt(((centre[0] - x) ** 2) + (centre[1] - y) ** 2)
        if distance <= CIRCLE_RADIUS:
            return alphabet.get(alphabetCounter)
        alphabetCounter += 1


def wordPicker():
    global word
    wordNumber = randint(1, 10000)
    lineCounter = 0
    for word in words:
        if lineCounter != wordNumber:
            lineCounter += 1
        else:
            if len(word) <= 15:
                return word


def guess(letter):
    global guessedLetters
    global hangmanStage
    global word
    global letterSpaces

    if letter:  # Checks that the click method hasn't returned None. i.e: The player clicked on an actual letter
        if letter.lower() in word:
            counter = 0
            for correctLetter in list(word):
                if letter.lower() == correctLetter:
                    letterSpaces[counter] = letter.lower()
                counter += 1
        else:
            if letter not in guessedLetters:
                guessedLetters += '  ' + letter
                hangmanStage += 1


def checkWin():
    global letterSpaces
    global running
    if '_' not in letterSpaces:
        running = False


def drawLetters():
    for i in range(26):
        pygame.draw.circle(win, GREEN, CIRCLE_CENTRES[i], CIRCLE_RADIUS, CIRCLE_WIDTH)
        letter = FONT.render(alphabet.get(i + 1), False, WHITE)
        win.blit(letter, (CIRCLE_CENTRES[i][0] - 6, CIRCLE_CENTRES[i][1] - 8))


def drawGuessedLetters():
    guessedLettersRender = FONT.render(guessedLetters, False, BLUE)
    win.blit(guessedLettersRender, GUESSED_LETTER_COORDS)


def drawHangman():
    if 8 >= hangmanStage > 0:
        win.blit(stageToPicture.get(hangmanStage), HANGMAN_COORDS)
    elif hangmanStage > 8:
        gameOver()


def drawWordSpaces():
    global letterSpaces
    guessedPartWord = ''
    for letter in letterSpaces:
        guessedPartWord += letter

    wordSpacesRender = BIG_FONT.render(guessedPartWord, False, GREEN)
    win.blit(wordSpacesRender, (340, 250))


def redrawWindow():
    win.fill((150, 150, 150))
    drawLetters()
    drawGuessedLetters()
    drawHangman()
    drawWordSpaces()
    checkWin()


def gameOver():
    gameOverRender = BIG_FONT.render('GAME OVER', False, GREEN)
    win.blit(gameOverRender, (320, 320))
    win.blit(stage8, HANGMAN_COORDS)

    playAgainRender = FONT.render('Press ENTER to play again', False, BLACK)
    win.blit(playAgainRender, (320, 400))


def restartGame():
    global letterSpaces
    global word
    global hangmanStage
    global guessedLetters

    word = wordPicker()
    letterSpaces = ['_' for _ in range(len(word) - 1)]
    hangmanStage = 0
    guessedLetters = ""
    print(word)    

word = wordPicker()
letterSpaces = ['_' for _ in range(len(word) - 1)]

print(word)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            guess(click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RETURN:
                restartGame()

    redrawWindow()
    pygame.display.update()

pygame.quit()
words.close()
