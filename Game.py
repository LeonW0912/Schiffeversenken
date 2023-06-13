import pygame
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QProgressBar, QLabel, QMessageBox
import sys
import random
import pymsgbox
import time

########################################################################################################################
#                                              Schiffe Versenken by Leon Walter                                        #
########################################################################################################################
# Version: 0.9
#
# TODO: Evtl. Algorithmus in Hinsicht verbessern wenn nichts mehr nach vorne geht das man es in die entgegengesetzte Richtung probiert
# TODO: Evtl. 2 Spielermodus?
# TODO: PyQt6 Oberfläche als Hauptmenü?

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

def QT_button_clicked():
    global difficulty
    sender = window.sender()
    # Alle Buttons auf Standardfarbe zurücksetzen
    button_easy.setStyleSheet('''
    QPushButton {
        background-color: #50C878;
        border-radius: 10px
    }
    QPushButton:hover {
        background-color: #3CB371;
    }
    ''')
    button_medium.setStyleSheet('''
    QPushButton {
        background-color: #50C878;
        border-radius: 10px
    }
    QPushButton:hover {
        background-color: #3CB371;
    }
    ''')
    button_hard.setStyleSheet('''
    QPushButton {
        background-color: #50C878;
        border-radius: 10px
    }
    QPushButton:hover {
        background-color: #3CB371;
    }
    ''')
    # Hintergrundfarbe des geklickten Buttons ändern
    sender.setStyleSheet('''
    QPushButton {
        background-color: #FFFF00;
        border-radius: 10px   
    }
    QPushButton:hover {
        background-color: #FFD700;
    }
    ''')
    if sender.text() == "Einfach":
        print("Einfach ausgewählt")
        difficulty = 1
    elif sender.text() == "Mittel":
        print("Mittel ausgewählt")
        difficulty = 2
    elif sender.text() == "Schwer":
        print("Schwer ausgewählt")
        difficulty = 3


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
layout = QVBoxLayout(widget)

button_easy = QPushButton("Einfach")
button_medium = QPushButton("Mittel")
button_hard = QPushButton("Schwer")

button_easy.setFixedHeight(50)  # Höhe des Buttons "Einfach" auf 50 Pixel setzen
button_medium.setFixedHeight(50)  # Höhe des Buttons "Mittel" auf 50 Pixel setzen
button_hard.setFixedHeight(50)  # Höhe des Buttons "Schwer" auf 50 Pixel setzen

app.setStyleSheet('''
    QPushButton {
        background-color: #50C878;
        border-radius: 10px
    }
    QPushButton:hover {
        background-color: #3CB371;
    }
    QProgressBar {
        background-color: gray;
    }
    ''')
button_medium.setStyleSheet('''
    QPushButton {
        background-color: #FFFF00;
        border-radius: 10px   
    }
    QPushButton:hover {
        background-color: #FFD700;
    }
    ''')
difficulty = 2

button_easy.clicked.connect(QT_button_clicked)
button_medium.clicked.connect(QT_button_clicked)
button_hard.clicked.connect(QT_button_clicked)

layout.addWidget(button_easy)
layout.addWidget(button_medium)
layout.addWidget(button_hard)

widget.setLayout(layout)
window.setCentralWidget(widget)
window.setGeometry(100, 100, 300, 300)

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
                        pymsgbox.alert(str("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!"), "Fehler 01", button="OK")
                elif richtung == 2: # Links
                    check_var = False
                    for i in range(Ship_Size):
                        if x//blocksize - i < 0:
                            check_var = True
                        else:
                            if visual_array[y//blocksize][x//blocksize - i] > 0:
                                check_var = True
                                break
                    if check_var == False:
                        for i in range(Ship_Size):
                            visual_array[y//blocksize][x//blocksize - i] = 5
                            Ships_P1[y//blocksize][x//blocksize - i] = 1
                    else:
                        click_counter = click_counter - 1
                        print("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!")
                        pymsgbox.alert(str("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!"), "Fehler 01", button="OK")
                elif richtung == 3:  # Hoch
                    check_var = False
                    for i in range(Ship_Size):
                        print(y//blocksize-i)
                        if (y//blocksize) - i < 0:
                            print("TEst")
                            check_var = True
                        else:
                            if visual_array[y // blocksize - i][x // blocksize] > 0:
                                check_var = True
                    if check_var == False:
                        for i in range(Ship_Size):
                            visual_array[y // blocksize - i][x // blocksize] = 5
                            Ships_P1[y // blocksize - i][x // blocksize] = 1
                    else:
                        click_counter = click_counter - 1
                        print("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!")
                        pymsgbox.alert(str("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!"), "Fehler 01", button="OK")
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
                        pymsgbox.alert(str("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!"), "Fehler 01", button="OK")
                if click_counter == 10:
                    Ship_Size = 0
            elif visual_array[y//blocksize][x//blocksize] == 4: # Überprüfung Treffer / Daneben
                Ship_Size = 1 #Platzhalter
            elif visual_array[y//blocksize][x//blocksize] == 5: # Platzhalter Schiff Image
                screen.blit(placeholder, rect)
            else:
                destroy_Grid()

def draw_KI_Grid():
    blocksize = 50

    # Layout (A-J & 1-10)
    font = pygame.font.SysFont(None, 25)
    for i in range(10):
        # A-J rechts vom Grid
        text = font.render(chr(ord('A') + i), True, BLACK)
        screen.blit(text, (screen_width - 10 * blocksize - 25, i * blocksize + 10))

        # 1-10 unterhalb des Grids
        text = font.render(str(i + 1), True, BLACK)
        screen.blit(text, (screen_width - i * blocksize - 30, 10 * blocksize))

    # Grid
    for x in range(0, 10*blocksize, blocksize):
        for y in range(0, 10*blocksize, blocksize):
            rect = pygame.Rect(screen_width-x-blocksize, y, blocksize, blocksize)
            if visual_array_KI[y//blocksize][x//blocksize] == 0:   #Normales Feld ohne alles
                pygame.draw.rect(screen, GRAY, rect, 1)
            elif visual_array_KI[y//blocksize][x//blocksize] == 1: #Feld mit Explosion (also getroffen)
                screen.blit(exp_image, rect)
            elif visual_array_KI[y//blocksize][x//blocksize] == 2: #Feld mit Splash (also daneben)
                screen.blit(spl_image, rect)

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
    done_counter = 0

    #5er Schiff
    placed = False
    while placed == False:
        placeable = True
        random_x = random.randint(0, 9)
        random_y = random.randint(0, 9)
        direction = random.randint(1, 4)
        if direction == 1: # Rechts
            for i in range(5):
                if random_x + i > 9:
                    placeable = False
            if placeable == True:
                placed = True
                for j in range(5):
                    Ships_P2[random_y][random_x + j] = 1
        elif direction == 2: # Links
            for i in range(5):
                if random_x - i <= 0:
                    placeable = False
            if placeable == True:
                placed = True
                for j in range(5):
                    Ships_P2[random_y][random_x - j] = 1

        elif direction == 3: # Hoch
            for i in range(5):
                if random_y - i <= 0:
                    placeable = False
            if placeable == True:
                placed = True
                for j in range(5):
                    Ships_P2[random_y - j][random_x] = 1

        elif direction == 4: # Runter
            for i in range(5):
                if random_y + i > 9:
                    placeable = False
            if placeable == True:
                placed = True
                for j in range(5):
                    Ships_P2[random_y + j][random_x] = 1
    done_counter = done_counter + 1
    print(str(done_counter) + "/10 Schiffen gesetzt")

    #2x 4er Schiffe
    for k in range(2):
        done_counter = done_counter + 1
        print(str(done_counter) + "/10 Schiffen gesetzt")
        placed = False
        while placed == False:
            placeable = True
            random_x = random.randint(0, 9)
            random_y = random.randint(0, 9)
            direction = random.randint(1, 4)
            if direction == 1:  # Rechts
                for i in range(4):
                    if random_x + i > 9:
                        placeable = False
                    else:
                        if Ships_P2[random_y][random_x + i] == 1:
                            placeable = False

                if placeable == True:
                    placed = True
                    for j in range(4):
                        Ships_P2[random_y][random_x + j] = 1
            elif direction == 2:  # Links
                for i in range(4):
                    if random_x - i <= 0:
                        placeable = False
                    else:
                        if Ships_P2[random_y][random_x - i] == 1:
                            placeable = False

                if placeable == True:
                    placed = True
                    for j in range(4):
                        Ships_P2[random_y][random_x - j] = 1

            elif direction == 3:  # Hoch
                for i in range(4):
                    if random_y - i <= 0:
                        placeable = False
                    else:
                        if Ships_P2[random_y - i][random_x] == 1:
                            placeable = False

                if placeable == True:
                    placed = True
                    for j in range(4):
                        Ships_P2[random_y - j][random_x] = 1

            elif direction == 4:  # Runter
                for i in range(4):
                    if random_y + i > 9:
                        placeable = False
                    else:
                        if Ships_P2[random_y + i][random_x] == 1:
                            placeable = False

                if placeable == True:
                    placed = True
                    for j in range(4):
                        Ships_P2[random_y + j][random_x] = 1

    # 3x 3er Schiffe
    for k in range(3):
        placed = False
        done_counter = done_counter + 1
        print(str(done_counter) + "/10 Schiffen gesetzt")
        while placed == False:
            placeable = True
            random_x = random.randint(0, 9)
            random_y = random.randint(0, 9)
            direction = random.randint(1, 4)
            if direction == 1:  # Rechts
                for i in range(3):
                    if random_x + i > 9:
                        placeable = False
                    else:
                        if Ships_P2[random_y][random_x + i] == 1:
                            placeable = False

                if placeable == True:
                    placed = True
                    for j in range(3):
                        Ships_P2[random_y][random_x + j] = 1
            elif direction == 2:  # Links
                for i in range(3):
                    if random_x - i < 0:
                        placeable = False
                    else:
                        if Ships_P2[random_y][random_x - i] == 1:
                            placeable = False

                if placeable == True:
                    placed = True
                    for j in range(3):
                        Ships_P2[random_y][random_x - j] = 1

            elif direction == 3:  # Hoch
                for i in range(3):
                    if random_y - i < 0:
                        placeable = False
                    else:
                        if Ships_P2[random_y - i][random_x] == 1:
                            placeable = False

                if placeable == True:
                    placed = True
                    for j in range(3):
                        Ships_P2[random_y - j][random_x] = 1

            elif direction == 4:  # Runter
                for i in range(3):
                    if random_y + i > 9:
                        placeable = False
                    else:
                        if Ships_P2[random_y + i][random_x] == 1:
                            placeable = False

                if placeable == True:
                    placed = True
                    for j in range(3):
                        Ships_P2[random_y + j][random_x] = 1

    # 4x 2er Schiffe
    for k in range(4):
        placed = False
        done_counter = done_counter + 1
        print(str(done_counter) + "/10 Schiffen gesetzt")
        while placed == False:
            placeable = True
            random_x = random.randint(0, 9)
            random_y = random.randint(0, 9)
            direction = random.randint(1, 4)
            if direction == 1:  # Rechts
                for i in range(2):
                    if random_x + i > 9:
                        placeable = False
                    else:
                        if Ships_P2[random_y][random_x + i] == 1:
                            placeable = False

                if placeable == True:
                    placed = True
                    for j in range(2):
                        Ships_P2[random_y][random_x + j] = 1
            elif direction == 2:  # Links
                for i in range(2):
                    if random_x - i < 0:
                        placeable = False
                    else:
                        if Ships_P2[random_y][random_x - i] == 1:
                            placeable = False

                if placeable == True:
                    placed = True
                    for j in range(2):
                        Ships_P2[random_y][random_x - j] = 1

            elif direction == 3:  # Hoch
                for i in range(2):
                    if random_y - i < 0:
                        placeable = False
                    else:
                        if Ships_P2[random_y - i][random_x] == 1:
                            placeable = False

                if placeable == True:
                    placed = True
                    for j in range(2):
                        Ships_P2[random_y - j][random_x] = 1

            elif direction == 4:  # Runter
                for i in range(2):
                    if random_y + i > 9:
                        placeable = False
                    else:
                        if Ships_P2[random_y + i][random_x] == 1:
                            placeable = False

                if placeable == True:
                    placed = True
                    for j in range(2):
                        Ships_P2[random_y + j][random_x] = 1
    print("KI Grid:")
    print(Ships_P2)

def diff_easy():
    möglich = False
    global Getroffen_P2
    while möglich == False:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        if Grid_P2[y][x] == 0:
            möglich = True
            print("Ki schießt auf: ", y, x, "...")
            if Ships_P1[y][x] == 1:
                Grid_P2[y][x] = 1
                Getroffen_P2 = Getroffen_P2 + 1
                print("... Getroffen!")
                visual_array_KI[y][x] = 1
                Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                layout.update()
            elif Ships_P1[y][x] == 0:
                Grid_P2[y][x] = 2
                visual_array_KI[y][x] = 2
                print("... Daneben!")
    # Logik : KI schießt einfach Zufällig auf ein Feld das er noch nicht getroffen hat ohne jegliches Muster oder Algorythmus

def diff_middle():
    möglich = False
    möglich2 = False
    global algorithmus
    global Getroffen_P2
    global save_y
    global save_x
    global im_alg_getroffen
    global save_richtung

    while möglich == False:
        if algorithmus == False:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if Grid_P2[y][x] == 0:
                möglich = True
                print("Ki schießt auf: ", y, x, "...")
                if Ships_P1[y][x] == 1:
                    Grid_P2[y][x] = 1
                    Getroffen_P2 = Getroffen_P2 + 1
                    print("... Getroffen!")
                    algorithmus = True
                    save_x = x
                    save_y = y
                    visual_array_KI[y][x] = 1
                    Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                    layout.update()
                elif Ships_P1[y][x] == 0:
                    Grid_P2[y][x] = 2
                    visual_array_KI[y][x] = 2
                    print("... Daneben!")
                break
        elif algorithmus == True:
            if im_alg_getroffen == True:
                if save_richtung == 1:  #LI
                    if save_x-1 >= 0:
                        if Ships_P2[save_y][save_x-1] == 1:
                            if Grid_P2[save_y][save_x-1] == 0:
                                print("Ki schießt auf: ", save_y, save_x-1, "...")
                                print("... Getroffen!")
                                Getroffen_P2 = Getroffen_P2 + 1
                                Grid_P2[save_y][save_x-1] = 1
                                save_y = save_y
                                save_x = save_x-1
                                visual_array_KI[save_y][save_x] = 1
                                Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                                layout.update()
                                break
                            else:
                                algorithmus = False
                                diff_middle()
                                möglich = True
                        else:
                            if Grid_P2[save_y][save_x-1] == 0:
                                print("Ki schießt auf: ", save_y, save_x-1, "...")
                                print("... Getroffen!")
                                Getroffen_P2 = Getroffen_P2 + 1
                                Grid_P2[save_y][save_x-1] = 1
                                save_y = save_y
                                save_x = save_x - 1
                                visual_array_KI[save_y][save_x] = 1
                                Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                                layout.update()
                                break
                            else:
                                algorithmus = False
                                diff_middle()
                                möglich = True
                    else:
                        algorithmus = False
                        diff_middle()
                        möglich = True
                elif save_richtung == 2:#RE
                    if save_x+1 < 10:
                        if Ships_P2[save_y][save_x+1] == 1:
                            if Grid_P2[save_y][save_x+1] == 0:
                                print("Ki schießt auf: ", save_y, save_x+1, "...")
                                print("... Getroffen!")
                                Getroffen_P2 = Getroffen_P2 + 1
                                Grid_P2[save_y][save_x+1] = 1
                                save_y = save_y
                                save_x = save_x + 1
                                visual_array_KI[save_y][save_x] = 1
                                Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                                layout.update()
                                break
                            else:
                                algorithmus = False
                                diff_middle()
                                möglich = True
                        else:
                            if Grid_P2[save_y][save_x+1] == 0:
                                print("Ki schießt auf: ", save_y, save_x+1, "...")
                                print("... Getroffen!")
                                Getroffen_P2 = Getroffen_P2 + 1
                                Grid_P2[save_y][save_x+1] = 1
                                save_y = save_y
                                save_x = save_x + 1
                                visual_array_KI[save_y][save_x] = 1
                                Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                                layout.update()
                                break
                            else:
                                algorithmus = False
                                diff_middle()
                                möglich = True
                    else:
                        algorithmus = False
                        diff_middle()
                        möglich = True
                elif save_richtung == 3:#HO
                    if save_y-1 >= 0:
                        if Ships_P2[save_y-1][save_x] == 1:
                            if Grid_P2[save_y-1][save_x] == 0:
                                print("Ki schießt auf: ", save_y-1, save_x, "...")
                                print("... Getroffen!")
                                Getroffen_P2 = Getroffen_P2 + 1
                                Grid_P2[save_y-1][save_x] = 1
                                save_y = save_y - 1
                                save_x = save_x
                                visual_array_KI[save_y][save_x] = 1
                                Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                                layout.update()
                                break
                            else:
                                algorithmus = False
                                diff_middle()
                                möglich = True
                        else:
                            if Grid_P2[save_y-1][save_x] == 0:
                                print("Ki schießt auf: ", save_y-1, save_x, "...")
                                print("... Getroffen!")
                                Getroffen_P2 = Getroffen_P2 + 1
                                Grid_P2[save_y-1][save_x] = 1
                                save_y = save_y - 1
                                save_x = save_x
                                visual_array_KI[save_y][save_x] = 1
                                Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                                layout.update()
                                break
                            else:
                                algorithmus = False
                                diff_middle()
                                möglich = True
                    else:
                        algorithmus = False
                        diff_middle()
                        möglich = True
                elif save_richtung == 4:#RU
                    if save_y+1 < 10:
                        if Ships_P2[save_y+1][save_x] == 1:
                            if Grid_P2[save_y-1][save_x] == 0:
                                print("Ki schießt auf: ", save_y+1, save_x, "...")
                                print("... Getroffen!")
                                Getroffen_P2 = Getroffen_P2 + 1
                                Grid_P2[save_y+1][save_x] = 1
                                save_y = save_y + 1
                                save_x = save_x
                                visual_array_KI[save_y][save_x] = 1
                                Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                                layout.update()
                                break
                            else:
                                algorithmus = False
                                diff_middle()
                                möglich = True
                        else:
                            if Grid_P2[save_y+1][save_x] == 0:
                                print("Ki schießt auf: ", save_y+1, save_x, "...")
                                print("... Getroffen!")
                                Getroffen_P2 = Getroffen_P2 + 1
                                Grid_P2[save_y+1][save_x] = 1
                                save_y = save_y + 1
                                save_x = save_x
                                visual_array_KI[save_y][save_x] = 1
                                Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                                layout.update()
                                break
                            else:
                                algorithmus = False
                                diff_middle()
                                möglich = True
                    else:
                        algorithmus = False
                        diff_middle()
                        möglich = True
            elif im_alg_getroffen == False:
                while möglich2 == False:
                    richtung = random.randint(1, 4)
                    print(richtung)
                    #Wenn alle Felder in alle Richtungen blockiert sind:
                    if ((save_x - 1 < 0 or Grid_P2[save_y][save_x - 1] != 0) and  # Links
                        (save_x + 1 >= 10 or Grid_P2[save_y][save_x + 1] != 0) and  # Rechts
                        (save_y - 1 < 0 or Grid_P2[save_y - 1][save_x] != 0) and  # Hoch
                        (save_y + 1 >= 10 or Grid_P2[save_y + 1][save_x] != 0)):  # Runter
                        algorithmus = False
                        diff_middle()
                        möglich = True
                        möglich2 = True
                    if richtung == 1: # Links
                        if save_x-1 >= 0:
                            if Grid_P2[save_y][save_x - 1] == 0:
                                print("Ki schießt auf: ", save_y, save_x-1, "...")
                                möglich2 = True
                                möglich = True
                                if Ships_P1[save_y][save_x-1] == 1:
                                    Grid_P2[save_y][save_x-1] = 1
                                    save_y = save_y
                                    save_x = save_x - 1
                                    visual_array_KI[save_y][save_x] = 1
                                    print("... Getroffen!")
                                    Getroffen_P2 = Getroffen_P2 + 1
                                    im_alg_getroffen = True
                                    save_richtung = 1
                                    Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                                    layout.update()
                                elif Ships_P1[save_y][save_x-1] == 0:
                                    Grid_P2[save_y][save_x - 1] = 2
                                    visual_array_KI[save_y][save_x - 1] = 2
                                    print("... Daneben!")
                                break
                    if richtung == 2: # Rechts
                        if save_x+1 < 10:
                            if Grid_P2[save_y][save_x + 1] == 0:
                                print("Ki schießt auf: ", save_y, save_x+1, "...")
                                möglich2 = True
                                möglich = True
                                if Ships_P1[save_y][save_x+1] == 1:
                                    Grid_P2[save_y][save_x+1] = 1
                                    save_y = save_y
                                    save_x = save_x + 1
                                    visual_array_KI[save_y][save_x] = 1
                                    print("... Getroffen!")
                                    Getroffen_P2 = Getroffen_P2 + 1
                                    im_alg_getroffen = True
                                    save_richtung = 2
                                    Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                                    layout.update()
                                elif Ships_P1[save_y][save_x+1] == 0:
                                    Grid_P2[save_y][save_x + 1] = 2
                                    visual_array_KI[save_y][save_x + 1] = 2
                                    print("... Daneben!")
                                break
                    if richtung == 3: # Hoch
                        if save_y-1 >= 0:
                            if Grid_P2[save_y-1][save_x] == 0:
                                print("Ki schießt auf: ", save_y-1, save_x, "...")
                                möglich2 = True
                                möglich = True
                                if Ships_P1[save_y-1][save_x] == 1:
                                    Grid_P2[save_y-1][save_x] = 1
                                    save_y = save_y - 1
                                    save_x = save_x
                                    visual_array_KI[save_y][save_x] = 1
                                    print("... Getroffen!")
                                    Getroffen_P2 = Getroffen_P2 + 1
                                    im_alg_getroffen = True
                                    save_richtung = 3
                                    Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                                    layout.update()
                                elif Ships_P1[save_y-1][save_x] == 0:
                                    Grid_P2[save_y-1][save_x] = 2
                                    visual_array_KI[save_y - 1][save_x] = 2
                                    print("... Daneben!")
                                break
                    if richtung == 4: # Runter
                        if save_y+1 < 10:
                            if Grid_P2[save_y+1][save_x] == 0:
                                print("Ki schießt auf: ", save_y+1, save_x, "...")
                                möglich2 = True
                                möglich = True
                                if Ships_P1[save_y+1][save_x] == 1:
                                    Grid_P2[save_y+1][save_x] = 1
                                    save_y = save_y+1
                                    save_x = save_x
                                    visual_array_KI[save_y][save_x] = 1
                                    print("... Getroffen!")
                                    Getroffen_P2 = Getroffen_P2 + 1
                                    im_alg_getroffen = True
                                    save_richtung = 4
                                    Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                                    layout.update()
                                elif Ships_P1[save_y+1][save_x] == 0:
                                    Grid_P2[save_y+1][save_x] = 2
                                    visual_array_KI[save_y + 1][save_x] = 2
                                    print("... Daneben!")
                                break
    # Logik: Die KI schießt auf ein Zufälliges Feld bis er etwas getroffen hat danach geht er in eine Zufällige Richtung
    # ausgehend von dem Feld das er getroffen hat und schießt sofern es geht solange in die Richtung weiter bis entweder
    # das Ende erreicht ist, etwas blockiert oder Kein Schiff mehr da ist.

def diff_hard():
    möglich = False
    global Getroffen_P2
    while möglich == False:
        treffwahrscheinlichkeit = random.randint(1, 100)
        ist_richtig = False
        if treffwahrscheinlichkeit < 86: # 85% Chance das er Trifft
            while ist_richtig == False:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                if Ships_P1[y][x] == 1:
                    print("Ki schießt auf: ", y, x, "...")
                    print("... Getroffen!")
                    Getroffen_P2 = Getroffen_P2 + 1
                    ist_richtig = True
                    möglich = True
                    Grid_P2[y][x] = 1
                    visual_array_KI[y][x] = 1
                    Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                    layout.update()
        else: # 25% Chance auf Daneben
            while ist_richtig == False:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                if Ships_P1[y][x] == 0:
                    print("Ki schießt auf: ", y, x, "...")
                    print("... Daneben!")
                    ist_richtig = True
                    möglich = True
                    Grid_P2[y][x] = 2
                    visual_array_KI[y][x] = 2
    # Logik: Die KI hat eine 85% Chance immer ein Feld zu treffen auf der ein Schiff ist am sonsten ist es ein anderes

#Arrays
visual_array = np.zeros((10, 10), dtype=int) #Zur Visuellen Darstellung des Spielers
visual_array_KI = np.zeros((10, 10), dtype=int) #Zur Visuellen Darstellung der KI
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
möglich = False
algorithmus = False
im_alg_getroffen = False
save_x = 0
save_y = 0
save_richtung = 0
Mode = 1
Getroffen_P1 = 0
Getroffen_P2 = 0

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
                        Mode = 2
                        # PyQt6 Teil:
                        # Entfernt die Buttons aus dem Layout nachdem das Spiel begonnen hat
                        layout.removeWidget(button_easy)
                        button_easy.setParent(None)
                        layout.removeWidget(button_medium)
                        button_medium.setParent(None)
                        layout.removeWidget(button_hard)
                        button_hard.setParent(None)
                        layout.update()
                        layout.setContentsMargins(0, -10, 0, -10)
                        layout.setSpacing(5)
                        Spieler_text = QLabel("Spieler Fortschritt")
                        Progress_Player = QProgressBar()
                        Progress_Player.setFixedHeight(20)
                        KI_text = QLabel("KI Fortschritt")
                        Progress_KI = QProgressBar()
                        Progress_KI.setFixedHeight(20)
                        layout.addSpacing(50)
                        layout.addWidget(Spieler_text)
                        layout.addWidget(Progress_Player)
                        layout.addSpacing(50)
                        layout.addWidget(KI_text)
                        layout.addWidget(Progress_KI)
                        layout.addStretch()
                        layout.update()
                    else:
                        print("Es sind noch nicht alle Schiffe platziert")
                        pymsgbox.alert(str("Es sind noch nicht alle Schiffe platziert!"), "Fehler 02", button="OK")

            if Mode == 1: # Schiffsetzung
                index = get_clicked_index(event.pos)
                if index is not None:
                    x = index[0]
                    y = index[1]
                    if Ship_Size != 0:
                        if visual_array[y][x] == 0:
                            visual_array[y][x] = 3
                        else:
                            click_counter = click_counter - 1
                    if click_counter != 10:
                        click_counter = click_counter + 1
                    if click_counter == 2:
                        Ship_Size = 4
                    elif click_counter == 4:
                        Ship_Size = 3
                    elif click_counter == 7:
                        Ship_Size = 2
                    #Wird Ausgeführt BEVOR das ins array geht deswegen wann geschieht es + 1
            elif Mode == 2: # Spielverlauf
                möglich2 = False
                index = get_clicked_index(event.pos)
                print(Getroffen_P2)
                if Getroffen_P1 == 30:
                    print("Spieler 1 hat gewonnen")
                    Mode = 3
                elif Getroffen_P2 == 30:
                    print("Spieler 2 hat gewonnen")
                    Mode = 3

                if index is not None:
                    x = index[0]
                    y = index[1]
                    if Grid_P1[y][x] == 0:
                        möglich2 = True
                        if Ships_P2[y][x] == 1:
                            visual_array[y][x] = 1 # Getroffen
                            Grid_P1[y][x] = 1
                            Getroffen_P1 = Getroffen_P1 + 1
                            Progress_Player.setValue(round(Getroffen_P1 / 30 * 100))
                            layout.update()
                        else:
                            visual_array[y][x] = 2 # Daneben
                            Grid_P1[y][x] = 2
                    else:
                        print("Auf dieses Feld wurde schon geschossen")
                        pymsgbox.alert(str("Auf dieses Feld wurde schon geschossen!"), "Fehler 03", button="OK")

                    if möglich2 == True:
                        if Getroffen_P2 < 30:
                            if difficulty == 1:
                                diff_easy()
                            elif difficulty == 2:
                                diff_middle()
                            elif difficulty == 3:
                                diff_hard()

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
    if Mode == 2:
        draw_KI_Grid()

    def closeEvent(self, event): #Schließevent für beides
        pygame.quit()
        event.accept()

    # Hält das Fenster offen
    pygame.display.flip()
    clock.tick(FPS)

# Schließe alles wenn running = False
pygame.quit()
