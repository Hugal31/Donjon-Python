#!/usr/bin/env python3

########################################
#------------Donjon & Python-----------#
#---------Test des textures pack-------#
#--------------------------------------#
#-----------------v1.0-----------------#
#--------------------------------------#
#---------------25/02/2014-------------#
########################################

#-----------Import des modules---------#

import pygame
from pygame.locals import *
from tkinter import Tk

LENGTH = 13
HEIGHT = 7
N_ELEM = 6

from MoteurGraphique import chargerTextures, chargerTile, block, iEntite

#---------Définition des classes-------#

class Tile:
    """Tile qui change de valeur quand on clique dessus"""
    def __init__(self):
        global block
        self.valeur = 0
        self.texture = block[0]['case']
    def majTexure(self, etage):
        global tiles
        self.texture = tiles[etage][self.valeur]

#--------Définition des fonctions------#


def grille(x, y):
    return (x*32 + 32, y*32 +32)


def rafraichir():
    global fenetre, etage, fond, block, grille
    fenetre.blit(fond[etage], grille(-1, -1))
    for y in range(HEIGHT):
        for x in range(LENGTH):
            grilleTiles[y][x].majTexure(etage)
            fenetre.blit(grilleTiles[y][x].texture, grille(x, y))
    pygame.display.flip()

def texture(pack):
    global fond
    chargerTextures(texturePack)
    for etage in range(5):
        fond.append(chargerTile(texturePack, etage, 'sol'))

def changeValue(pos, pas):
    global grilleTiles
    x = (pos[0] - 32)//32
    y = (pos[1] - 32)//32
    if x >= 0 and x < LENGTH and y >=0 and y < HEIGHT :
        grilleTiles[y][x].valeur = (grilleTiles[y][x].valeur+pas) % N_ELEM

def enregistrer():
    """Enregistre la salle dans un fichier"""
    global grilleTiles
    try:
        nom = int(input('Entrez un numéro : '))
        text = ''
        for y in range(HEIGHT):
            for x in range(LENGTH):
                text += str(grilleTiles[y][x].valeur)
            text += '\n'
        fichier = open('Salles\\'+str(nom)+'.txt', mode='w', encoding='Utf-8')
        fichier.write(text)
        fichier.close()
    except : pass

def ouvrir():
    """Ouvre un fichier paterne"""
    global grille
    try:
        fichier = open('Salles/' + input('Entrez un nom de fichier : ') + '.txt', mode='r', encoding='Utf-8')
        text = fichier.readlines()
        fichier.close()
        for y in range(HEIGHT):
            for x in range(LENGTH):
                grilleTiles[y][x].valeur = int(text[y][x])
        rafraichir()
    except : pass

def reset():
    global grilleTiles
    for y in range(HEIGHT):
        for x in range(LENGTH):
            grilleTiles[y][x].valeur = 0
    rafraichir()

#--------Définition des variables------#

texturePack = 'Default'
tiles = []
etage = 0
continuer = True

#-----------Boucle principale----------#

print("""Generateur de salle
Appuez sur O pour ouvrir une salle
Appuez sur S pour enregistre la salle
Appuez sur R pour réinitialiser la grille
Flèche haut et bas pour changer d'étage""")

fenetre = pygame.display.set_mode((480,288), RESIZABLE)
fond = []
texture(texturePack)

for etage in range(5):
    tilesEtage = [block[etage]['case'],
                  block[etage]['rocher'],
                  block[etage]['trou'],
                  block[etage]['coffre'],
                  iEntite[0][0][2],
                  iEntite[1][0][2]]
    tiles.append(tilesEtage)

grilleTiles = []
for y in range(7):
    grilleTiles.append([])
    for x in range(13):
        grilleTiles[y].append(Tile())

etage = 0

rafraichir()
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        if event.type == KEYDOWN:
            if event.key == K_UP:
                if etage < 4:etage += 1
            elif event.key == K_DOWN:
                if etage > 0:etage -= 1
            elif event.key == K_F5:
                texture(texturePack)
            elif event.key == K_s : enregistrer()
            elif event.key == K_o : ouvrir()
            elif event.key == K_r : reset()

        elif event.type ==  MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] : changeValue(pygame.mouse.get_pos(), 1)
            elif pygame.mouse.get_pressed()[2] : changeValue(pygame.mouse.get_pos(), -1)

        rafraichir()
