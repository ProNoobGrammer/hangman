import pygame
from math import sqrt
from os.path import join
from random import randint


pygame.init()
pygame.font.init()
SMALL_FONT = pygame.font.SysFont("Comic Sans MS", 15)
BIG_FONT = pygame.font.SysFont("Comic Sans MS", 30)
MEDIUM_FONT = pygame.font.SysFont("Comic Sans MS", 25)
win = pygame.display.set_mode((630, 600))
pygame.display.set_caption("Hangman")
CIRCLE_CENTRES = [(45, 50), (90, 50), (135, 50), (180, 50), (225, 50), (270, 50), (315, 50),
                  (360, 50), (405, 50), (450, 50), (495, 50), (540, 50), (585, 50),
                  (45, 100), (90, 100), (135, 100), (180, 100), (225, 100), (270, 100), (315, 100),
                  (360, 100), (405, 100), (450, 100), (495, 100), (540, 100), (585, 100)]
CIRCLE_RADIUS = 20
CIRCLE_WIDTH = 1
GUESSED_LETTER_COORDS = (45, 500)
HANGMAN_COORDS = (50, 130)


stage1 = pygame.image.load(join('img', '1.png'))
stage2 = pygame.image.load(join('img', '2.png'))
stage3 = pygame.image.load(join('img', '3.png'))
stage4 = pygame.image.load(join('img', '4.png'))
stage5 = pygame.image.load(join('img', '5.png'))
stage6 = pygame.image.load(join('img', '6.png'))
stage7 = pygame.image.load(join('img', '7.png'))
stage8 = pygame.image.load(join('img', '8.png'))

GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (150, 150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

word = ""
guessedLetters = ""
hangmanStage = 0
letterSpaces = []



ALPHABET = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L", 13: "M",
            14: "N", 15: "O", 16: "P", 17: "Q", 18: "R", 19: "S", 20: "T", 21: "U", 22: "V", 23: "W", 24: "X", 25: "Y",
            26: "Z"}

def click(x, y):
    counter = 1
    for centre in CIRCLE_CENTRES:
        distance = sqrt(((centre[0] - x) ** 2) + (centre[1] - y) ** 2)
        if distance <= CIRCLE_RADIUS:
            return ALPHABET.get(counter)
        counter += 1


def wordPicker():
    global word

    wordNumber = randint(1, 9895)
    lineCounter = 0
    with open('Words.txt', 'r') as words:
        for possible_word in words:
            if lineCounter != wordNumber:
                lineCounter += 1
            else:
                if len(possible_word) <= 15:
                    word = possible_word
                    return


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


def checkwin():
    global letterSpaces
    global running
    if '_ ' not in letterSpaces:
        gamewin()


def drawLetters():
    for i in range(26):
        pygame.draw.circle(win, GREEN, CIRCLE_CENTRES[i], CIRCLE_RADIUS, CIRCLE_WIDTH)
        letter = SMALL_FONT.render(ALPHABET.get(i + 1), False, WHITE)
        win.blit(letter, (CIRCLE_CENTRES[i][0] - 6, CIRCLE_CENTRES[i][1] - 8))


def drawGuessedLetters():
    guessedLettersRender = MEDIUM_FONT.render(guessedLetters, False, BLUE)
    win.blit(guessedLettersRender, GUESSED_LETTER_COORDS)

STAGE_TO_PICTURE = {1: stage1, 2: stage2, 3: stage3, 4: stage4, 5: stage5, 6: stage6, 7: stage7, 8: stage8}

def drawHangman():
    if 8 > hangmanStage > 0:
        win.blit(STAGE_TO_PICTURE.get(hangmanStage), HANGMAN_COORDS)
    elif hangmanStage >= 8:
        gameOver()


def drawWordSpaces():
    global letterSpaces
    guessedPartWord = ''
    for letter in letterSpaces:
        guessedPartWord += letter

    wordSpacesRender = BIG_FONT.render(guessedPartWord, False, GREEN)
    win.blit(wordSpacesRender, (340, 250))


def redrawwindow():
    win.fill(GREY)
    drawLetters()
    drawGuessedLetters()
    drawHangman()
    drawWordSpaces()
    checkwin()


def gameOver():
    gameOverRender = BIG_FONT.render('GAME OVER', False, RED)
    win.blit(gameOverRender, (320, 320))
    win.blit(stage8, HANGMAN_COORDS)

    playAgainRender = SMALL_FONT.render('Press SPACE to play again', False, BLACK)
    win.blit(playAgainRender, (320, 400))


def gamewin():
    winRender = BIG_FONT.render('YOU win', False, GREEN)
    win.blit(winRender, (320, 320))

    playAgainRender = SMALL_FONT.render('Press SPACE to play again', False, BLACK)
    win.blit(playAgainRender, (320, 400))


def restartGame():
    global letterSpaces
    global hangmanStage
    global guessedLetters
    global word

    wordPicker()
    letterSpaces = ['_ ' for _ in range(len(word) - 1)]
    hangmanStage = 0
    guessedLetters = ""
    print(word)

wordPicker()
letterSpaces = ['_ ' for _ in range(len(word) - 1)]

print(word)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            guess(click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                restartGame()

    redrawwindow()
    pygame.display.update()

pygame.quit()
