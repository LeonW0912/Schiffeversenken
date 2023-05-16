import pygame
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget
import sys
import random
import time

class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 24)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Alle Benötigten Variablen
WHITE = pygame.Color("WHITE")
GRAY = pygame.Color("GRAY")
BLACK = pygame.Color("BLACK")
Ship_Size = 5
click_counter = 0
richtung = 4 #1 Links 2 Rechts 3 Hoch 4 Runter
check_var = False

#PyQt6
app = QApplication(sys.argv)
window = QMainWindow()
widget = QWidget()
layout = QHBoxLayout(widget)
button = QPushButton("Test")

layout.addWidget(button)
widget.setLayout(layout)
window.setCentralWidget(widget)
window.setGeometry(100, 100, 300, 300)
button.setGeometry(100, 125, 100, 50)

window.show()

pygame.init()

def draw_Grid():
    global click_counter
    global Ship_Size
    global check_var
    global richtung
    blocksize = 50

    # Layout (A-J & 1-10)
    font = pygame.font.SysFont(None, 25)
    for i in range(10):
        # A-J rechts vom Grid
        text = font.render(chr(ord('A') + i), True, BLACK)
        screen.blit(text, (10 * blocksize + 20, i * blocksize + 10))

        # 1-10 unterhalb des Grids
        text = font.render(str(i + 1), True, BLACK)
        screen.blit(text, (i * blocksize + 20, 10 * blocksize + 10))

    # Grid
    for x in range(0, 10*blocksize, blocksize):
        for y in range(0, 10*blocksize, blocksize):
            rect = pygame.Rect(x, y, blocksize, blocksize)
            if visual_array[y//blocksize][x//blocksize] == 0:   #Normales Feld ohne alles
                pygame.draw.rect(screen, GRAY, rect, 1)
            elif visual_array[y//blocksize][x//blocksize] == 1: #Feld mit Explosion (also getroffen)
                screen.blit(exp_image, rect)
            elif visual_array[y//blocksize][x//blocksize] == 2: #Feld mit Splash (also daneben)
                screen.blit(spl_image, rect)
            elif visual_array[y//blocksize][x//blocksize] == 3:
                visual_array[y//blocksize][x//blocksize] = 0
                if richtung == 1:   # Rechts
                    check_var = False
                    for i in range(Ship_Size):
                        if x//blocksize + i >= 10:
                            check_var = True
                        else:
                            if visual_array[y//blocksize][x//blocksize + i] > 0:
                                check_var = True
                                break
                    if check_var == False:
                        for i in range(Ship_Size):
                            visual_array[y//blocksize][x//blocksize + i] = 5
                            Ships_P1[y//blocksize][x//blocksize + i] = 1
                    else:
                        click_counter = click_counter - 1
                        print("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!")
                elif richtung == 2: # Links
                    check_var = False
                    for i in range(Ship_Size):
                        if visual_array[y//blocksize][x//blocksize - i] > 0 or x - i >= 0:
                            check_var = True
                    if check_var == False:
                        for i in range(Ship_Size):
                            visual_array[y//blocksize][x//blocksize - i] = 5
                            Ships_P1[y//blocksize][x//blocksize - i] = 1
                    else:
                        click_counter = click_counter - 1
                        print("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!")
                elif richtung == 3: # Hoch
                    check_var = False
                    for i in range(Ship_Size):
                        if visual_array[y//blocksize - i][x//blocksize] > 0 or x - i >= 0:
                            check_var = True
                    if check_var == False:
                        for i in range(Ship_Size):
                            visual_array[y//blocksize - i][x//blocksize] = 5
                            Ships_P1[y//blocksize - i][x//blocksize] = 1
                    else:
                        click_counter = click_counter - 1
                        print("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!")
                elif richtung == 4: # Runter
                    check_var = False
                    for i in range(Ship_Size):
                        if y//blocksize + i >= 10:
                            check_var = True
                        else:
                            if visual_array[y//blocksize + i][x//blocksize] > 0:
                                check_var = True
                    if check_var == False:
                        for i in range(Ship_Size):
                            visual_array[y//blocksize + i][x//blocksize] = 5
                            Ships_P1[y//blocksize + i][x//blocksize] = 1
                    else:
                        click_counter = click_counter - 1
                        print("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!")

                if click_counter == 10:
                    Ship_Size = 0
            elif visual_array[y//blocksize][x//blocksize] == 4: # Überprüfung Treffer / Daneben
                Ship_Size = 1 #Platzhalter
            elif visual_array[y//blocksize][x//blocksize] == 5: # Platzhalter Schiff Image
                screen.blit(placeholder, rect)
            else:
                destroy_Grid()

def destroy_Grid():
    global visual_array
    visual_array[9][9] = 6
    screen.fill((255, 255, 255))
    pygame.display.flip()
    pygame.display.update()
    #draw_Grid()

def get_clicked_index(pos):
    blocksize = 50
    for x in range(0, 10*blocksize, blocksize):
        for y in range(0, 10*blocksize, blocksize):
            rect = pygame.Rect(x, y, blocksize, blocksize)
            if rect.collidepoint(pos):
                return (x // blocksize, y // blocksize)
    return None

def generate_random_grid(): #Erstellt Grid mit zufällig platzierten Schiffen
    #5er Schiff
    placed = False
    placeable = True
    while not placed:
        random_x = random.randint(0, 9)
        random_y = random.randint(0, 9)
        direction = random.randint(1, 4)
        if direction == 1: # Rechts
            for i in range(5):
                if random_x >= 10:
                    placeable = False
            if placeable == True:
                placed = True
                for j in range(5):
                    Ships_P2[random_y][random_x + j] = 1
        elif direction == 2: # Links
            for i in range(5):
                if random_x <= 0:
                    placeable = False
            if placeable == True:
                placed = True
                for j in range(5):
                    Ships_P2[random_y][random_x - j] = 1

        elif direction == 3: # Hoch
            for i in range (5):
                if random_y <= 0:
                    placeable = False
            if placeable == True:
                placed = True
                for j in range(5):
                    Ships_P2[random_y + j][random_x] = 1

        elif direction == 4: # Runter
            for i in range(5):
                if random_y >= 10:
                    placeable = False
            if placeable == True:
                placed = True
                for j in range(5):
                    Ships_P2[random_y - j][random_x] = 1

    #2x 4er Schiffe
    for k in range(2):
        placed = False
        placeable = True
        while not placed:
            random_x = random.randint(0, 9)
            random_y = random.randint(0, 9)
            direction = random.randint(1, 4)
            if direction == 1:  # Rechts
                for i in range(4):
                    if random_x >= 10:
                        placeable = False
                    elif Ships_P2[random_y][random_x + j] == 1:
                        placeable = False

                if placeable == True:
                    placed = True
                    for j in range(4):
                        Ships_P2[random_y][random_x + j] = 1
            elif direction == 2:  # Links
                for i in range(4):
                    if random_x <= 0:
                        placeable = False
                    elif Ships_P2[random_y][random_x - j] == 1:
                        placeable = False

                if placeable == True:
                    placed = True
                    for j in range(4):
                        Ships_P2[random_y][random_x - j] = 1

            elif direction == 3:  # Hoch
                for i in range(4):
                    if random_y <= 0:
                        placeable = False
                    elif Ships_P2[random_y + j][random_x] == 1:
                        placeable = False

                if placeable == True:
                    placed = True
                    for j in range(4):
                        Ships_P2[random_y + j][random_x] = 1

            elif direction == 4:  # Runter
                for i in range(4):
                    if random_y >= 10:
                        placeable = False
                    elif Ships_P2[random_y - j][random_x] == 1:
                        placeable = False

                if placeable == True:
                    placed = True
                    for j in range(4):
                        Ships_P2[random_y - j][random_x] = 1

    #3x 3er Schiffe
    for k in range(3):
        placed = False
        placeable = True
        while not placed:
            random_x = random.randint(0, 9)
            random_y = random.randint(0, 9)
            direction = random.randint(1, 4)
            if direction == 1:  # Rechts
                for i in range(3):
                    if random_x >= 10:
                        placeable = False
                    elif Ships_P2[random_y][random_x + j] == 1:
                        placeable = False

                if placeable == True:
                    placed = True
                    for j in range(3):
                        Ships_P2[random_y][random_x + j] = 1
            elif direction == 2:  # Links
                for i in range(3):
                    if random_x <= 0:
                        placeable = False
                    elif Ships_P2[random_y][random_x - j] == 1:
                        placeable = False

                if placeable == True:
                    placed = True
                    for j in range(3):
                        Ships_P2[random_y][random_x - j] = 1

            elif direction == 3:  # Hoch
                for i in range(3):
                    if random_y <= 0:
                        placeable = False
                    elif Ships_P2[random_y + j][random_x] == 1:
                        placeable = False

                if placeable == True:
                    placed = True
                    for j in range(3):
                        Ships_P2[random_y + j][random_x] = 1

            elif direction == 4:  # Runter
                for i in range(3):
                    if random_y >= 10:
                        placeable = False
                    elif Ships_P2[random_y - j][random_x] == 1:
                        placeable = False

                if placeable == True:
                    placed = True
                    for j in range(3):
                        Ships_P2[random_y - j][random_x] = 1

    #4x 2er Schiffe
    for k in range(4):
        placed = False
        placeable = True
        while not placed:
            random_x = random.randint(0, 9)
            random_y = random.randint(0, 9)
            direction = random.randint(1, 4)
            if direction == 1:  # Rechts
                for i in range(2):
                    if random_x >= 10:
                        placeable = False
                    elif Ships_P2[random_y][random_x + j] == 1:
                        placeable = False

                if placeable == True:
                    placed = True
                    for j in range(2):
                        Ships_P2[random_y][random_x + j] = 1
            elif direction == 2:  # Links
                for i in range(2):
                    if random_x <= 0:
                        placeable = False
                    elif Ships_P2[random_y][random_x - j] == 1:
                        placeable = False

                if placeable == True:
                    placed = True
                    for j in range(2):
                        Ships_P2[random_y][random_x - j] = 1

            elif direction == 3:  # Hoch
                for i in range(2):
                    if random_y <= 0:
                        placeable = False
                    elif Ships_P2[random_y + j][random_x] == 1:
                        placeable = False

                if placeable == True:
                    placed = True
                    for j in range(2):
                        Ships_P2[random_y + j][random_x] = 1

            elif direction == 4:  # Runter
                for i in range(2):
                    if random_y >= 10:
                        placeable = False
                    elif Ships_P2[random_y - j][random_x] == 1:
                        placeable = False

                if placeable == True:
                    placed = True
                    for j in range(2):
                        Ships_P2[random_y - j][random_x] = 1
    print(Ships_P2)

#Arrays
visual_array = np.zeros((10, 10), dtype=int) #Zur Visuellen Darstellung
Ships_P1 = np.zeros((10, 10), dtype=int)     #Schiffpositionen von P1
Ships_P2 = np.zeros((10, 10), dtype=int)     #Schiffpositionen von P2
Grid_P1 = np.zeros((10, 10), dtype=int)      # Treffer / Daneben P1
Grid_P2 = np.zeros((10, 10), dtype=int)      # Treffer / Daneben P2

#PyGame Variablen
FPS = 20
screen_width = 1280
screen_height = 550
pygame.display.set_caption("Schiffe versenken by Leon Walter")
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Variablen die für den Button gebraucht werden
button_width = 200
button_height = 50
button_x = (screen_width - button_width) // 2 + 25
button_y = (screen_height - button_height) // 2
button = Button(button_x, button_y, button_width, button_height, (255, 0, 0), "Feld abgeben")

# Bildvariablen
exp_image = pygame.image.load('explosion.jpg')
spl_image = pygame.image.load('splash.jpg')
placeholder = pygame.image.load('PlaceHolder.png')

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button is not None:
                if button.is_clicked(event.pos):
                    button.color = pygame.Color("BLUE")
                    print('Button clicked')
                    print(click_counter)
                    print(Ships_P1)
                    # Check if all Ships are placed
                    if click_counter == 10:
                        destroy_Grid()
                        visual_array = np.zeros((10, 10), dtype=int)
                        button = None
                        generate_random_grid()
                    else:
                        print("Es sind noch nicht alle Schiffe platziert")
            index = get_clicked_index(event.pos)
            if index is not None:
                x = index[0]
                y = index[1]
                if Ship_Size != 0:
                    visual_array[y][x] = 3
                if click_counter != 10:
                    click_counter = click_counter + 1

                if click_counter == 2:
                    Ship_Size = 4
                elif click_counter == 4:
                    Ship_Size = 3
                elif click_counter == 7:
                    Ship_Size = 2
                #Wird Ausgeführt BEVOR das ins array geht deswegen wann geschieht es + 1

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                print("Rechts")
                richtung = 1
            elif event.key == pygame.K_LEFT:
                print("Links")
                richtung = 2
            elif event.key == pygame.K_UP:
                print("Hoch")
                richtung = 3
            elif event.key == pygame.K_DOWN:
                print("Runter")
                richtung = 4

    if button is not None:
        button.draw(screen)
    draw_Grid()

    def closeEvent(self, event): #Schließevent für beides
        pygame.quit()
        event.accept()

    # Hält das Fenster offen
    pygame.display.flip()
    clock.tick(FPS)

# Schließe alles wenn running = False
pygame.quit()
