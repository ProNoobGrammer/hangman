import pygame
from math import sqrt
from time import sleep

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("Comic Sans MS", 15)
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 600
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hangman")
CIRCLE_CENTRES = [(45, 50), (90, 50), (135, 50), (180, 50), (225, 50), (270, 50), (315, 50),
                  (360, 50), (405, 50), (450, 50), (495, 50), (540, 50), (595, 50),
                  (45, 100), (90, 100), (135, 100), (180, 100), (225, 100), (270, 100), (315, 100),
                  (360, 100), (405, 100), (450, 100), (495, 100), (540, 100), (595, 100)]
CIRCLE_RADIUS = 20
CIRCLE_WIDTH = 1
alphabet = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 11: "K", 12: "L", 13: "M",
            14: "N", 15: "O", 16: "P", 17: "Q", 18: "R", 19: "S", 20: "T", 21: "U", 22: "V", 23: "W", 24: "X", 25: "Y",
            26: "Z"}

GREEN = (0, 255, 0)
GREY = (150, 150, 150)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def click(x, y):
    counter = 1
    for centre in CIRCLE_CENTRES:
        distance = sqrt(((centre[0] - x) ** 2) + (centre[1] - y) ** 2)
        if distance <= CIRCLE_RADIUS:
            return alphabet.get(counter)
        counter += 1


def redrawWindow():
    win.fill((150, 150, 150))
    for i in range(26):
        pygame.draw.circle(win, GREEN, CIRCLE_CENTRES[i], CIRCLE_RADIUS, CIRCLE_WIDTH)
        letter = FONT.render(alphabet.get(i+1), True, WHITE)
        win.blit(letter, (CIRCLE_CENTRES[i][0] - 7, CIRCLE_CENTRES[i][1] - 7))

running = True
while running:
    sleep(0.2)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            click(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    redrawWindow()
    pygame.display.update()

pygame.quit()