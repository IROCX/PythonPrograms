import pygame
import random
pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('FX Hangman')

# fonts
letter_font = pygame.font.SysFont('comicsans', 30)
word_font = pygame.font.SysFont('comicsans', 50)
title_font = pygame.font.SysFont('comicsans', 60)


# game vars
hangman_status = 0
word_list = ['Random', 'developer']
word = random.choice(word_list)
word = word.upper()
guess = []


# load images
images = []
for i in range(7):
    image = pygame.image.load('assets/hangman' + str(i) + '.png')
    images.append(image)

FPS = 60
clock = pygame.time.Clock()
run = True

# button vars
RADIUS = 20
GAP = 20
A = 65
letters = []  # x, y, char, visible
startx, starty = 20, 450
for i in range(26):
    if i < 13:
        x, y = startx + GAP + RADIUS*2*(i % 13) + GAP*(i % 13), starty
    else:
        x, y = startx + GAP + RADIUS*2*(i % 13) + GAP*(i % 13), starty + 50

    letters.append([x, y, chr(A+i), 1])


def draw():

    WINDOW.fill(WHITE)
    # draw title
    text = title_font.render('FX Hangman', 1, BLACK)
    WINDOW.blit(text, (WIDTH/2-text.get_width()/2, 20))

    # draw word
    display_word = ''
    for letter in word:
        if letter in guess:
            display_word += letter + " "
        else:
            display_word+= ' _ '
    word_label = word_font.render(display_word, 1 , BLACK)
    WINDOW.blit(word_label, (400, 200))
    
    # draw buttons
    for letter in letters:
        x, y, char, visible = letter

        if visible:
            pygame.draw.circle(WINDOW, BLACK, (x, y), RADIUS, 3)
            char_label = letter_font.render(char, 1, BLACK)
            WINDOW.blit(char_label, (x-char_label.get_width() /
                                     2, y-char_label.get_height()/2))

    WINDOW.blit(images[hangman_status], (100, 100))
    pygame.display.update()


def display_message(message, *args):
    pygame.time.delay(1000)
    WINDOW.fill(WHITE)
    for i in args:
        text = word_font.render(i, 1, BLACK)
        WINDOW.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    
    text = word_font.render(message, 1, BLACK)
    WINDOW.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2 + GAP*len(args)))
    pygame.display.update()

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for letter in letters:
                x, y, char, visible = letter
                if (x-RADIUS < mx < x+RADIUS) and (y-RADIUS < my < y+RADIUS):
                    guess.append(char)
                    if char not in word:
                        hangman_status+=1
                    letter[3] = 0
    
    draw()

    won = True
    for letter in word:
        if letter not in guess:
            won = False
            break

    if won:
        display_message('Congrats!!! You won.', word)
        pygame.time.delay(3000)
        break
    elif hangman_status==6:
        display_message('Sorry... You lost.')
        pygame.time.delay(3000)
        break

pygame.quit()
