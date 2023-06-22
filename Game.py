import os.path
import pygame
import numpy as np
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QHBoxLayout, QWidget, QVBoxLayout, QProgressBar, QLabel, QMessageBox, QMenuBar
import math
import sys
import random
import pymsgbox

########################################################################################################################
#                                              Schiffe Versenken by Leon Walter                                        #
########################################################################################################################
# Version: 1.0
#
# TODO: Evtl. 2 Spielermodus? -> Später Nicht genügend Zeit
# TODO: Evtl. Online Multiplayer? -> SPäter Nicht genügend Zeit

# Klasse für einen Button in Pygame
class Button:
    #Initiator (Allgemeine EInstellungen)
    def __init__(self, x, y, width, height, color, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 24)

    #Button Erstellen / dem Fenster hinzufügen
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


    def is_clicked(self, pos): #Wenn Button angeklickt wurde gib position
        return self.rect.collidepoint(pos)

# Funktion für wenn ein button von PyQt6 Gedrückt wurde
def QT_button_clicked():
    global difficulty
    sender = window.sender() # sender = gedrückter button einfach gesagt
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
    # Ausgabe und Schwierigkeitssetzung
    if sender.text() == "Einfach":
        print("Einfach ausgewählt")
        difficulty = 1
    elif sender.text() == "Mittel":
        print("Mittel ausgewählt")
        difficulty = 2
    elif sender.text() == "Schwer":
        print("Schwer ausgewählt")
        difficulty = 3


# Wichtige Variablen
# pygame Farben (meisten davon eigentlich nicht benötigt):
WHITE = pygame.Color("WHITE")
GRAY = pygame.Color("GRAY")
BLACK = pygame.Color("BLACK")
MEERBLAU = pygame.Color(37,59,98)
# Allgemeinere Variablen:
Ship_Size = 5 # Aktuelle Schiffsgröße bei Schiffssetzung (für die Schleifen)
click_counter = 0 #
richtung = 4 #1 Links 2 Rechts 3 Hoch 4 Runter
check_var = False #

#PyQt6
# Grundlegende Dinge Wie die App, das Fenster usw.
app = QApplication(sys.argv)
window = QMainWindow()
window.setWindowTitle("Schwierigkeits Auswahl")
widget = QWidget()
layout = QVBoxLayout(widget)


#Schwierigkeitsbuttons
button_easy = QPushButton("Einfach")
button_medium = QPushButton("Mittel")
button_hard = QPushButton("Schwer")

# Höhe der Buttons setzen
button_easy.setFixedHeight(50)  # Höhe des Buttons "Einfach" auf 50 Pixel setzen
button_medium.setFixedHeight(50)  # Höhe des Buttons "Mittel" auf 50 Pixel setzen
button_hard.setFixedHeight(50)  # Höhe des Buttons "Schwer" auf 50 Pixel setzen

# Gestaltung der Buttons mittels QSS
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

# andere Farbe für Medium Button da er standardmäßig ausgewählt ist
button_medium.setStyleSheet('''
    QPushButton {
        background-color: #FFFF00;
        border-radius: 10px   
    }
    QPushButton:hover {
        background-color: #FFD700;
    }
    ''')

difficulty = 2 # Standard Schwierigkeit Mittel

# Die Funktion für wenn der Button geklickt wurde anbinden
button_easy.clicked.connect(QT_button_clicked)
button_medium.clicked.connect(QT_button_clicked)
button_hard.clicked.connect(QT_button_clicked)

# Buttons zum Widget hinzufügen
layout.addWidget(button_easy)
layout.addWidget(button_medium)
layout.addWidget(button_hard)

# Allgemeine Layout / Widget Einstellungen
widget.setLayout(layout)
window.setCentralWidget(widget)
window.setGeometry(100, 100, 300, 300)

# Zeige das Fenster und Initialisiere PyGame
window.show()
pygame.init()

# Funktion zum Erstellen des Linken (Spieler) Grids
def draw_Grid():
    global click_counter
    global Ship_Size
    global check_var
    global richtung
    blocksize = 50 # Größe der Kästchen 50 angemessen und auf Fenstergröße optimiert WARNUNG: Änderungen NICHT Empfohlen

    # Layout (A-J & 1-10)
    font = pygame.font.SysFont(None, 25) # Scriftart für Texte in Pygame
    #Buchstaben und Zahlen schreiben mit jeweiliger Positionierung
    for i in range(10):
        # A-J rechts vom Grid
        text = font.render(chr(ord('A') + i), True, BLACK)
        screen.blit(text, (10 * blocksize + 20, i * blocksize + 10))

        # 1-10 unterhalb des Grids
        text = font.render(str(i + 1), True, BLACK)
        screen.blit(text, (i * blocksize + 20, 10 * blocksize + 10))

    # Eigentliches Grid wird erstellt
    for x in range(0, 10*blocksize, blocksize):
        for y in range(0, 10*blocksize, blocksize):
            rect = pygame.Rect(x, y, blocksize, blocksize) #Rechteck erstellen

            #Verschiedene Arten von Füllungen für die Kästchen
            if visual_array[y//blocksize][x//blocksize] == 0:   #Normales Feld ohne alles Wenn dementsprechender index im array 0 ist
                pygame.draw.rect(screen, GRAY, rect, 1)
            elif visual_array[y//blocksize][x//blocksize] == 1: #Feld mit Explosion (also getroffen) Wenn dementsprechender index im array 1 ist
                screen.blit(exp_image, rect)
            elif visual_array[y//blocksize][x//blocksize] == 2: #Feld mit Splash (also daneben) Wenn dementsprechender index im array 2 ist
                screen.blit(spl_image, rect)
            elif visual_array[y//blocksize][x//blocksize] == 3: #Schiffssetzung Wenn dementsprechender index im array 0 ist
                visual_array[y//blocksize][x//blocksize] = 0 #Hat seine Gründe weiß nicht warum
                if richtung == 1:   # Rechts                 #Richtungen werden durch User Per Keyboard eingegeben (← ↑ ↓ →)
                    check_var = False
                    for i in range(Ship_Size):
                        if x//blocksize + i >= 10: #Wenn Über Rechten Rand Hinaus
                            check_var = True
                        else:
                            if visual_array[y//blocksize][x//blocksize + i] > 0: #Wenn Feld Nicht Frei ist oder schon beschossen wurde
                                check_var = True
                                break
                    if check_var == False: #Wenn beides oben genannte nicht wahr ist
                        for i in range(Ship_Size):
                            visual_array[y//blocksize][x//blocksize + i] = 5
                            Ships_P1[y//blocksize][x//blocksize + i] = 1
                    else:
                        # Schiffsplatzierung nicht möglich
                        click_counter = click_counter - 1
                        print("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!")
                        pymsgbox.alert(str("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!"), "Fehler 01", button="OK")
                elif richtung == 2: # Links
                    check_var = False
                    for i in range(Ship_Size):
                        if x//blocksize - i < 0: #Wenn über Linken Rand hinaus
                            check_var = True
                        else:
                            if visual_array[y//blocksize][x//blocksize - i] > 0: #Wenn Feld Nicht Frei ist oder schon beschossen wurde
                                check_var = True
                                break
                    if check_var == False: #Wenn beides oben gannannte nicht wahr ist
                        for i in range(Ship_Size):
                            visual_array[y//blocksize][x//blocksize - i] = 5
                            Ships_P1[y//blocksize][x//blocksize - i] = 1
                    else:
                        #Schiffsplatzierung nicht möglich
                        click_counter = click_counter - 1
                        print("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!")
                        pymsgbox.alert(str("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!"), "Fehler 01", button="OK")
                elif richtung == 3:  # Hoch
                    check_var = False
                    for i in range(Ship_Size):
                        if (y//blocksize) - i < 0: #Wenn über Oberen Rand hinaus
                            check_var = True
                        else:
                            if visual_array[y // blocksize - i][x // blocksize] > 0: #Wenn Feld Nicht Frei ist oder schon beschossen wurde
                                check_var = True
                    if check_var == False: # Wenn beides oben gannannte nicht wahr ist
                        for i in range(Ship_Size):
                            visual_array[y // blocksize - i][x // blocksize] = 5
                            Ships_P1[y // blocksize - i][x // blocksize] = 1
                    else:
                        # Schiffsplatzierung nicht möglich
                        click_counter = click_counter - 1
                        print("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!")
                        pymsgbox.alert(str("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!"), "Fehler 01", button="OK")
                elif richtung == 4: # Runter
                    check_var = False
                    for i in range(Ship_Size):
                        if y//blocksize + i >= 10: #Wenn über den unteren Rand hinaus
                            check_var = True
                        else:
                            if visual_array[y//blocksize + i][x//blocksize] > 0: #Wenn Feld Nicht Frei ist oder schon ebschossen wurde
                                check_var = True
                    if check_var == False: #Wenn beides Oben gennannte nicht wahr ist
                        for i in range(Ship_Size):
                            visual_array[y//blocksize + i][x//blocksize] = 5
                            Ships_P1[y//blocksize + i][x//blocksize] = 1
                    else:
                        # Schiffsplatzierung nicht möglich
                        click_counter = click_counter - 1
                        print("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!")
                        pymsgbox.alert(str("Etwas ist in Weg oder das Schiff würde außerhalb des Feldes gehen!"), "Fehler 01", button="OK")
                if click_counter == 10: #Wenn ClickCounter 10 dann Ship_Size auf 0 damit nichts gesetzt werden kann
                    Ship_Size = 0
            elif visual_array[y//blocksize][x//blocksize] == 4: # Überprüfung Treffer / Daneben
                Ship_Size = 1
            elif visual_array[y//blocksize][x//blocksize] == 5: # Schiff Image
                screen.blit(placeholder, rect)
            else: # Nichts davon
                destroy_Grid()

# Funktion zum Erstellen des Rechten (KI) Grids
def draw_KI_Grid():
    blocksize = 50 # s. draw_Grid()

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
            rect = pygame.Rect(screen_width-x-blocksize, y, blocksize, blocksize) #Rechteck zeichnen
            if visual_array_KI[y//blocksize][x//blocksize] == 0:   #Normales Feld ohne alles
                pygame.draw.rect(screen, GRAY, rect, 1)
            elif visual_array_KI[y//blocksize][x//blocksize] == 1: #Feld mit Explosion (also getroffen)
                screen.blit(exp_image, rect)
            elif visual_array_KI[y//blocksize][x//blocksize] == 2: #Feld mit Splash (also daneben)
                screen.blit(spl_image, rect)

# Funktion zum Zerstörren des Linken Grids
def destroy_Grid():
    global visual_array
    visual_array[9][9] = 6
    screen.fill((255, 255, 255))
    pygame.display.flip()
    pygame.display.update()
    #draw_Grid()

# Funktion um herauszufinden wohin du im linken Grid geklickt hast
def get_clicked_index(pos):
    blocksize = 50 # s. draw_Grid()
    for x in range(0, 10*blocksize, blocksize):
        for y in range(0, 10*blocksize, blocksize):
            rect = pygame.Rect(x, y, blocksize, blocksize)
            if rect.collidepoint(pos): # Wenn Rechteck mit Klicken Kollidiert
                return (x // blocksize, y // blocksize) # Gebe X und Y des Geklickten Feldes aus
    return None

#Erstellt Grid mit zufällig platzierten Schiffen
def generate_random_grid():
    done_counter = 0

    #5er Schiffe
    placed = False
    while placed == False: #Solange Schiff nicht platzier ist
        placeable = True
        random_x = random.randint(0, 9)
        random_y = random.randint(0, 9)
        direction = random.randint(1, 4)
        if direction == 1: # Platzierung Nach Rechts
            for i in range(5):
                if random_x + i > 9: # Geht es über den Rand hinaus
                    placeable = False
            if placeable == True: # Ist es Platzierbar
                placed = True
                for j in range(5):
                    Ships_P2[random_y][random_x + j] = 1
        elif direction == 2: # Platzierung Nach Links
            for i in range(5):
                if random_x - i <= 0: # Geht es über den Rand hinaus
                    placeable = False
            if placeable == True: # Ist es platzierbar
                placed = True
                for j in range(5):
                    Ships_P2[random_y][random_x - j] = 1

        elif direction == 3: # Platzierung nach Oben
            for i in range(5):
                if random_y - i <= 0: # Geht es über den Rand?
                    placeable = False
            if placeable == True: # ISt es Platzierbar
                placed = True
                for j in range(5):
                    Ships_P2[random_y - j][random_x] = 1

        elif direction == 4: # Platzierung Nach Unten
            for i in range(5):
                if random_y + i > 9: # Geht es Über den Rand?
                    placeable = False
            if placeable == True: # ISt es platzierbar?
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
        while placed == False: # Solange Schiff nicht platzier ist
            placeable = True
            random_x = random.randint(0, 9)
            random_y = random.randint(0, 9)
            direction = random.randint(1, 4)
            if direction == 1:  # Platzierung Nach Rechts
                for i in range(4):
                    if random_x + i > 9: # geht es über den Rand
                        placeable = False
                    else:
                        if Ships_P2[random_y][random_x + i] == 1: # Ist schon ein Schiff im Weg?
                            placeable = False

                if placeable == True: # ISt es Platzierbar
                    placed = True
                    for j in range(4):
                        Ships_P2[random_y][random_x + j] = 1
            elif direction == 2:  # Platzierung nach Links
                for i in range(4):
                    if random_x - i <= 0: # Geht es über den Rand?
                        placeable = False
                    else:
                        if Ships_P2[random_y][random_x - i] == 1: # Ist schon ein schiff im Weg?
                            placeable = False

                if placeable == True: # Ist es platzierbar?
                    placed = True
                    for j in range(4):
                        Ships_P2[random_y][random_x - j] = 1

            elif direction == 3:  # Platzierung nach Oben
                for i in range(4):
                    if random_y - i <= 0: # Geht es über den Rand
                        placeable = False
                    else:
                        if Ships_P2[random_y - i][random_x] == 1: # Ist schon ein Schiff im Weg?
                            placeable = False

                if placeable == True: # Ist es Platzierbar?
                    placed = True
                    for j in range(4):
                        Ships_P2[random_y - j][random_x] = 1

            elif direction == 4:  # Platzierung nach Unten
                for i in range(4):
                    if random_y + i > 9: # Geht es über den Rand?
                        placeable = False
                    else:
                        if Ships_P2[random_y + i][random_x] == 1: # ISt schon ein Schiff im Weg?
                            placeable = False

                if placeable == True: # Ist es Platzierbar?
                    placed = True
                    for j in range(4):
                        Ships_P2[random_y + j][random_x] = 1

    # 3x 3er Schiffe
    for k in range(3):
        placed = False
        done_counter = done_counter + 1
        print(str(done_counter) + "/10 Schiffen gesetzt")
        while placed == False: # Solange es nicht platzierbar ist?
            placeable = True
            random_x = random.randint(0, 9)
            random_y = random.randint(0, 9)
            direction = random.randint(1, 4)
            if direction == 1:  # Platzierung Nach Rechts
                for i in range(3):
                    if random_x + i > 9: # Geht es über den Rand?
                        placeable = False
                    else:
                        if Ships_P2[random_y][random_x + i] == 1: # Ist ein Schiff im Weg?
                            placeable = False
                if placeable == True: # Ist es platzierbar?
                    placed = True
                    for j in range(3):
                        Ships_P2[random_y][random_x + j] = 1
            elif direction == 2:  # Platzierung Nach Links
                for i in range(3):
                    if random_x - i < 0: # Geht es über den Rand?
                        placeable = False
                    else:
                        if Ships_P2[random_y][random_x - i] == 1: # Ist ein Schiff im Weg?
                            placeable = False
                if placeable == True: # Ist es platzierbar?
                    placed = True
                    for j in range(3):
                        Ships_P2[random_y][random_x - j] = 1

            elif direction == 3:  # Platzierung Nach Oben
                for i in range(3):
                    if random_y - i < 0: # Geht es über den Rand
                        placeable = False
                    else:
                        if Ships_P2[random_y - i][random_x] == 1: # Ist ein Schiff im Weg?
                            placeable = False
                if placeable == True: # Ist es Platzierbar?
                    placed = True
                    for j in range(3):
                        Ships_P2[random_y - j][random_x] = 1

            elif direction == 4:  # Platzierung Nach Unten
                for i in range(3):
                    if random_y + i > 9: # Geht es über den Rand?
                        placeable = False
                    else:
                        if Ships_P2[random_y + i][random_x] == 1: # Ist ein Schiff im Weg?
                            placeable = False
                if placeable == True: # Ist es platzierbar?
                    placed = True
                    for j in range(3):
                        Ships_P2[random_y + j][random_x] = 1

    # 4x 2er Schiffe
    for k in range(4):
        placed = False
        done_counter = done_counter + 1
        print(str(done_counter) + "/10 Schiffen gesetzt")
        while placed == False: # Solange es nicht platzierbar ist
            placeable = True
            random_x = random.randint(0, 9)
            random_y = random.randint(0, 9)
            direction = random.randint(1, 4)
            if direction == 1:  # Platzierung Nach Rechts
                for i in range(2):
                    if random_x + i > 9: # Geht es über den Rand?
                        placeable = False
                    else:
                        if Ships_P2[random_y][random_x + i] == 1: # Ist ein Schiff im Weg?
                            placeable = False
                if placeable == True: # Ist es platzierbar
                    placed = True
                    for j in range(2):
                        Ships_P2[random_y][random_x + j] = 1

            elif direction == 2:  # Platzierung Nach Links
                for i in range(2):
                    if random_x - i < 0: # Geht es über den Rand?
                        placeable = False
                    else:
                        if Ships_P2[random_y][random_x - i] == 1: # Ist ein Schiff im Weg?
                            placeable = False
                if placeable == True: # Ist es platzierbar?
                    placed = True
                    for j in range(2):
                        Ships_P2[random_y][random_x - j] = 1

            elif direction == 3:  # Platzierung Nach Oben
                for i in range(2):
                    if random_y - i < 0: # Geht es über den Rand?
                        placeable = False
                    else:
                        if Ships_P2[random_y - i][random_x] == 1: # Ist ein Schiff im Weg?
                            placeable = False
                if placeable == True: # Ist es platzierbar?
                    placed = True
                    for j in range(2):
                        Ships_P2[random_y - j][random_x] = 1

            elif direction == 4:  # Platzierung Nach Unten
                for i in range(2):
                    if random_y + i > 9: # Geht es über den Rand?
                        placeable = False
                    else:
                        if Ships_P2[random_y + i][random_x] == 1: # Ist ein Schiff im Weg?
                            placeable = False
                if placeable == True: # Ist es platzierbar?
                    placed = True
                    for j in range(2):
                        Ships_P2[random_y + j][random_x] = 1
    # Folgende 2 Zeilen sind zum anzeigen der schiffe im Python Terminal aka Cheating oder Testing
    print("KI Grid:")
    print(Ships_P2)

# Einfache Schwierigkeit
def diff_easy():
    möglich = False
    global Getroffen_P2
    while möglich == False: # Solange es nicht möglich ist das Feld zu beschießen
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        if Grid_P2[y][x] == 0: # Wenn beschossenes Feld nicht bereits beschossen wurde
            möglich = True
            print("Ki schießt auf: ", y, x, "...")
            if Ships_P1[y][x] == 1: # Wenn Getroffen
                Grid_P2[y][x] = 1
                Getroffen_P2 = Getroffen_P2 + 1
                # Alles Visuell / GUI / UI
                print("... Getroffen!")
                visual_array_KI[y][x] = 1
                Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                layout.update()
            elif Ships_P1[y][x] == 0: # Wenn Daneben
                Grid_P2[y][x] = 2
                #Visuell / GUI / UI
                visual_array_KI[y][x] = 2
                print("... Daneben!")
    # Logik : KI schießt einfach Zufällig auf ein Feld das er noch nicht getroffen hat ohne jegliches Muster oder Algorythmus

# Mittlere Schwierigkeit
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
        if algorithmus == False: # Ist dafür zuständig eine Zufällige zahl zu generieren bis er trifft
            print("JA")
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if Grid_P2[y][x] == 0:# Ist das Feld frei?
                möglich = True
                print("Ki schießt auf: ", y, x, "...")
                if Ships_P1[y][x] == 1: # getroffen
                    Grid_P2[y][x] = 1
                    Getroffen_P2 = Getroffen_P2 + 1
                    print("... Getroffen!")
                    print(Ships_P1[y][x])
                    algorithmus = True
                    save_x = x
                    save_y = y
                    visual_array_KI[y][x] = 1
                    Progress_KI.setValue(round(Getroffen_P2 / 30 * 100))
                    layout.update()
                elif Ships_P1[y][x] == 0: # Danebn
                    Grid_P2[y][x] = 2
                    visual_array_KI[y][x] = 2
                    print("... Daneben!")
                    print(Ships_P1[y][x])
                break
        elif algorithmus == True: # Algorithmus
            if im_alg_getroffen == True: # Richtung wurde schon herausgefunden
                if save_richtung == 1:  #Linke/Rechte Richtung
                    if 9-save_x-1 >= 0 and 9-save_x-1 <10 and save_x-1 >= 0: #Geht es außerhalb
                        if Ships_P2[save_y][9-save_x-1] == 1: # getroffen
                            if Grid_P2[save_y][save_x-1] == 0: # Wurde dort schon geschossen
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
                            if Grid_P2[save_y][save_x-1] == 0: # Wurde dort schon geschossen
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
                elif save_richtung == 2:#Rechts/Links
                    if 9-save_x+1 < 10 and 9-save_x+1 >= 0 and save_x+1 < 10: # Geht es außerhalb?
                        if Ships_P2[save_y][9-save_x+1] == 1: # Getroffen
                            if Grid_P2[save_y][save_x+1] == 0: # Wurde auf das Feld schon geschossen?
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
                            if Grid_P2[save_y][save_x+1] == 0: # Wurde auf das Feld schon geschossen
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
                elif save_richtung == 3:#Hoch
                    if save_y-1 >= 0: # Geht es außerhalb
                        if Ships_P2[save_y-1][9-save_x] == 1: # Getroffen
                            if Grid_P2[save_y-1][save_x] == 0: # Wurde das Feld schon beschossen
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
                            if Grid_P2[save_y-1][save_x] == 0: # Wurde das Feld schon beschossen
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
                elif save_richtung == 4:#Runter
                    if save_y+1 < 10: # Geht es auußerhalb
                        if Ships_P2[save_y+1][9-save_x] == 1: # Getroffen
                            if Grid_P2[save_y-1][save_x] == 0: # Wurde das Feld schon beschossen
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
                            if Grid_P2[save_y+1][save_x] == 0: # Wurde das Feld schon beschossen?
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
            elif im_alg_getroffen == False: # Richtung herausfinden
                while möglich2 == False:
                    richtung = random.randint(1, 4)
                    #Wenn alle Felder in alle Richtungen blockiert sind:
                    if ((save_x - 1 < 0 or Grid_P2[save_y][save_x - 1] != 0) and  # Links
                        (save_x + 1 >= 10 or Grid_P2[save_y][save_x + 1] != 0) and  # Rechts
                        (save_y - 1 < 0 or Grid_P2[save_y - 1][save_x] != 0) and  # Hoch
                        (save_y + 1 >= 10 or Grid_P2[save_y + 1][save_x] != 0)):  # Runter
                        algorithmus = False
                        diff_middle()
                        möglich = True
                        möglich2 = True
                    if richtung == 1: # Rechts
                        if 9-save_x-1 >= 0: # Geht es außerhalb
                            if Grid_P2[save_y][save_x - 1] == 0: # schon auf Feld geschossen
                                print("Ki schießt auf: ", save_y, save_x-1, "...")
                                möglich2 = True
                                möglich = True
                                if Ships_P1[save_y][9-save_x-1] == 1: # Getroffen
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
                                elif Ships_P1[save_y][9-save_x-1] == 0: # Daneben
                                    Grid_P2[save_y][save_x - 1] = 2
                                    visual_array_KI[save_y][save_x - 1] = 2
                                    print("... Daneben!")
                                break
                    if richtung == 2: # Links
                        if 9-save_x+1 < 10: # Geht es außerhalb
                            if Grid_P2[save_y][save_x + 1] == 0: # Schon auf das Feld geschossen?
                                print("Ki schießt auf: ", save_y, save_x+1, "...")
                                möglich2 = True
                                möglich = True
                                if Ships_P1[save_y][9-save_x+1] == 1: # Getroffen
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
                                elif Ships_P1[save_y][9-save_x+1] == 0: # Daneben
                                    Grid_P2[save_y][save_x + 1] = 2
                                    visual_array_KI[save_y][save_x + 1] = 2
                                    print("... Daneben!")
                                break
                    if richtung == 3: # Hoch
                        if save_y-1 >= 0: # Geht es außerhalb?
                            if Grid_P2[save_y-1][save_x] == 0: # Schon auf das Feld geschossen?
                                print("Ki schießt auf: ", save_y-1, save_x, "...")
                                möglich2 = True
                                möglich = True
                                if Ships_P1[save_y-1][9-save_x] == 1: # getroffen
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
                                elif Ships_P1[save_y-1][9-save_x] == 0: # Daneben
                                    Grid_P2[save_y-1][save_x] = 2
                                    visual_array_KI[save_y - 1][save_x] = 2
                                    print("... Daneben!")
                                break
                    if richtung == 4: # Runter
                        if save_y+1 < 10: # Geht es außerhalb
                            if Grid_P2[save_y+1][save_x] == 0: # Schon auf das Feld geschossen?
                                print("Ki schießt auf: ", save_y+1, save_x, "...")
                                möglich2 = True
                                möglich = True
                                if Ships_P1[save_y+1][9-save_x] == 1: # getroffen
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
                                elif Ships_P1[save_y+1][9-save_x] == 0: # Daneben
                                    Grid_P2[save_y+1][save_x] = 2
                                    visual_array_KI[save_y + 1][save_x] = 2
                                    print("... Daneben!")
                                break
    # Logik: Die KI schießt auf ein Zufälliges Feld bis er etwas getroffen hat danach geht er in eine Zufällige Richtung
    # ausgehend von dem Feld das er getroffen hat und schießt sofern es geht solange in die Richtung weiter bis entweder
    # das Ende erreicht ist, etwas blockiert oder Kein Schiff mehr da ist.

# Schwere Schwierigkeit
def diff_hard():
    möglich = False
    global Getroffen_P2
    while möglich == False: # Solange es nicht möglich ist auf dieses Feld zu schießen
        treffwahrscheinlichkeit = random.randint(1, 100)
        ist_richtig = False
        if treffwahrscheinlichkeit < 86: # 85% Chance das er Trifft
            while ist_richtig == False:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                if Ships_P1[y][x] == 1: # Ist das beschossene Feld getroffen?
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
                if Ships_P1[y][x] == 0: # Ist das beschossene Feld daneben?
                    print("Ki schießt auf: ", y, x, "...")
                    print("... Daneben!")
                    ist_richtig = True
                    möglich = True
                    Grid_P2[y][x] = 2
                    visual_array_KI[y][x] = 2
    # Logik: Die KI hat eine 85% Chance immer ein Feld zu treffen auf der ein Schiff ist am sonsten ist es ein anderes

#Array Variaben
visual_array = np.zeros((10, 10), dtype=int) #Zur Visuellen Darstellung des Spielers
visual_array_KI = np.zeros((10, 10), dtype=int) #Zur Visuellen Darstellung der KI
Ships_P1 = np.zeros((10, 10), dtype=int)     # Schiffpositionen von Player 1
Ships_P2 = np.zeros((10, 10), dtype=int)
Grid_P1 = np.zeros((10, 10), dtype=int)      # Treffer / Daneben Player 1
Grid_P2 = np.zeros((10, 10), dtype=int)

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

#Pfeil Variablen
arrow_length = 100
arrow_color = BLACK
arrow_thickness = 3
arrow_head_size = 15
arrow_direction = 270
IsInPlaceMode = True

def display_arrow(direction):
    # Berechnet die Position des Pfeiles
    arrow_x = screen_width * 0.75
    arrow_y = screen_height // 2

    # Berechnet den Endpunkt des Pfeiles anhand der Richtung
    angle = math.radians(direction)
    arrow_end_x = arrow_x + arrow_length * math.cos(angle)
    arrow_end_y = arrow_y - arrow_length * math.sin(angle)
    # "Malt" den Pfeil
    pygame.draw.line(screen, arrow_color, (arrow_x, arrow_y), (arrow_end_x, arrow_end_y), arrow_thickness)

    # Berechnet die Punkte des Pfeilkopfes
    angle_left = math.radians(direction + 135)
    arrow_left_x = arrow_end_x + arrow_head_size * math.cos(angle_left)
    arrow_left_y = arrow_end_y - arrow_head_size * math.sin(angle_left)

    angle_right = math.radians(direction - 135)
    arrow_right_x = arrow_end_x + arrow_head_size * math.cos(angle_right)
    arrow_right_y = arrow_end_y - arrow_head_size * math.sin(angle_right)

    # Zeichnet den Pfeilkopf
    pygame.draw.polygon(screen, arrow_color,
                        [(arrow_end_x, arrow_end_y), (arrow_left_x, arrow_left_y), (arrow_right_x, arrow_right_y)])

    # Updated das Display
    pygame.display.flip()

# Variablen die für den Button gebraucht werden
button_width = 200
button_height = 50
button_x = (screen_width - button_width) // 2 + 25 #Positionierung des Buttons in X
button_y = (screen_height - button_height) // 2 #Positionierung des Buttons in Y
button = Button(button_x, button_y, button_width, button_height, (255, 0, 0), "Feld abgeben")

# Bildvariablen
current_dir = os.path.dirname(os.path.abspath(__file__)) #Sollte das Spiel aus irgendeinen Grund nicht Funktionieren und
#  es hängt mit den Bildern zusammen, liegt es Sehr Wahrscheinlich hieran
exp_image = pygame.image.load(current_dir + '\explosion.jpg')
spl_image = pygame.image.load(current_dir + '\splash.jpg')
placeholder = pygame.image.load(current_dir + '\PlaceHolder.png')

while running:
    screen.fill((94,151,250)) #MeerBlau
    if IsInPlaceMode == True:
        display_arrow(arrow_direction)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Wenn Geschlossen Wird
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: #Wenn Maustaste geklickt wurde
            if button is not None: # Wenn Button existiert
                if button.is_clicked(event.pos): #Wenn Button angecklickt wurde
                    button.color = pygame.Color("BLUE")
                    print('Feld abgesendet')
                    print(Ships_P1)
                    if click_counter == 10:
                        destroy_Grid()
                        visual_array = np.zeros((10, 10), dtype=int)
                        button = None # "Löscht" Button
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
                        #Erstellt die Variablen für den Forschritts Balken
                        layout.setSpacing(5)
                        Spieler_text = QLabel("Spieler Fortschritt")
                        Progress_Player = QProgressBar()
                        Progress_Player.setFixedHeight(20)
                        KI_text = QLabel("KI Fortschritt")
                        Progress_KI = QProgressBar()
                        Progress_KI.setFixedHeight(20)
                        #Fügt die Forschritt Balken hinzu
                        layout.addSpacing(50)
                        layout.addWidget(Spieler_text)
                        layout.addWidget(Progress_Player)
                        layout.addSpacing(50)
                        layout.addWidget(KI_text)
                        layout.addWidget(Progress_KI)
                        layout.addStretch()
                        window.setWindowTitle("Aktueller Stand")
                        layout.update()
                    else: # Wenn nicht alle Schiffe platziert sind
                        print("Es sind noch nicht alle Schiffe platziert")
                        pymsgbox.alert(str("Es sind noch nicht alle Schiffe platziert!"), "Fehler 02", button="OK")

            if Mode == 1: # Modus Schiffsetzung
                index = get_clicked_index(event.pos) #Holt sich cen Index des Geklickten Feldes
                if index is not None: # Wenn er nicht Nichts ist
                    x = index[0]
                    y = index[1]
                    if Ship_Size != 0: #Wenn noch Schiffe zu platzieren sind
                        if visual_array[y][x] == 0: #Wenn Feld Frei ist
                            visual_array[y][x] = 3
                        else: #Feld nicht mehr frei
                            click_counter = click_counter - 1
                    if click_counter != 10: #Solange Clickcounter <10 rechne +1
                        click_counter = click_counter + 1
                        print(click_counter)
                    if click_counter == 2: #Wenn 1 5xSchiffe gesetzt wurden
                        Ship_Size = 4
                    elif click_counter == 4: #Wenn 2 4xSchiffe gesetzt wurden
                        Ship_Size = 3
                    elif click_counter == 7: #Wenn 3 3xSchiffe gesetzt wurden
                        Ship_Size = 2
                    # WICHTIG!! Wird Ausgeführt !!BEVOR!! das ins array geht deswegen wann geschieht es + 1
            elif Mode == 2: # Modus Spielverlauf
                IsInPlaceMode = False
                möglich2 = False
                index = get_clicked_index(event.pos) # Holt sich Index des geklickten Feldes
                if Getroffen_P1 == 30: #Hat Spieler 1 Gewonnen?
                    print("Spieler 1 hat gewonnen")
                    pymsgbox.alert(str("Der Spieler hat Gewonnen!"), "Herzlichen Glückwunsch", button="OK")
                    Mode = 3
                elif Getroffen_P2 == 30: #Hat Spieler 2 Gewonnen?
                    print("Spieler 2 hat gewonnen")
                    pymsgbox.alert(str("Die KI hat Gewonnen!"), "Du wurdest geschlagen", button="OK")
                    Mode = 3

                if index is not None: #Falls Index nicht Nichts
                    x = index[0]
                    y = index[1]
                    if Grid_P1[y][x] == 0: #Falls Feld frei / nicht bereits beschossen wurde
                        möglich2 = True
                        if Ships_P2[y][x] == 1: #Wenn Getroffen
                            visual_array[y][x] = 1
                            Grid_P1[y][x] = 1
                            Getroffen_P1 = Getroffen_P1 + 1
                            Progress_Player.setValue(round(Getroffen_P1 / 30 * 100))
                            layout.update()
                        else: #Wenn Daneben
                            visual_array[y][x] = 2
                            Grid_P1[y][x] = 2
                    else: # Wenn Feld bereits beschossen wurde
                        print("Auf dieses Feld wurde schon geschossen")
                        pymsgbox.alert(str("Auf dieses Feld wurde schon geschossen!"), "Fehler 03", button="OK")

                    if möglich2 == True: #Wenn Schuss "erfolgreich" (nicht im sinne getroffen) abgeschossen wurde
                        if Getroffen_P2 < 30: #Wenn KI noch nicht gewonnen hat
                            if difficulty == 1: #Einfach
                                diff_easy()
                            elif difficulty == 2: #Mittel
                                diff_middle()
                            elif difficulty == 3: #Schwer
                                diff_hard()
        #Hotkeys
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT: #Rechtepfeiltaste für Schiffsplatzierung nach Rechts
                print("Rechts")
                richtung = 1
                arrow_direction = 0
            elif event.key == pygame.K_LEFT: #Linkepfeiltaste für Schiffsplatzierung nach Links
                print("Links")
                richtung = 2
                arrow_direction = 180
            elif event.key == pygame.K_UP: #Pfeiltastehoch für Schiffsplatzierung nach Oben
                print("Hoch")
                richtung = 3
                arrow_direction = 90
            elif event.key == pygame.K_DOWN: #Pfeiltasterunter für Schiffsplatzierung nach Unten
                print("Runter")
                richtung = 4
                arrow_direction = 270

    if button is not None: #Wenn Button existiert bringe ihn auf die GUI / UI
        button.draw(screen)
    draw_Grid()
    if Mode == 2: #Spielverlauf Extra Zeichne KI Grid
        draw_KI_Grid()

    def closeEvent(self, event): #Schließevent für beides
        pygame.quit()
        event.accept()

    # Hält das Fenster offen
    pygame.display.flip()
    clock.tick(FPS)

# Schließe alles wenn running = False
pygame.quit()