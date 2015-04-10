#!/usr/bin/env python3.4

########################################
#------------Donjon & Python-----------#
#-----------Moteur Graphique-----------#
#--------------------------------------#
#-----------------v1.0-----------------#
#--------------------------------------#
#------------Fradot Geoffrey-----------#
#---------------25/02/2014-------------#
########################################

#-----------Import des modules---------#

import pygame
from pygame.locals import *
from math import *
from os import listdir
from time import sleep

import threading
import GenerationDonjon
from Debug import debug, afficherCarte, debugMode
import Coffre
import __main__
import Audio

#---Définition des variables globales--#

block = []
iEntite = []
iBoss = []
image = []
iProj = []

#------------Moteur graphique----------#

class MoteurGraphique():
    def __init__(self):
        global perso, debugMode
        perso = __main__.perso
        pygame.init()
        pygame.key.set_repeat(30, 60) #Défini le temps entre deux évènements
        debug('MoteurGraphique.__init__')
        self.fenetre = pygame.display.set_mode((784,320)) #Défini la taille de la fenêtre
        pygame.display.set_caption("Donjons&Python")
        self.texture = __main__.texturePack
        self.projectile = []#Liste de projectiles
        self.iPerso = []#Images du personnage
        self.mPos = [0,0]
        self.marche = 0
        self.cpt = 0
        self.t1 = pygame.time.get_ticks()
        self.posEpee = [0,0]
        for i in range(4): #Chargement de la texture du personnage
          iMPerso = []
          for j in range(3):
            iMPerso.append(chargerSprite(self.texture, "Personnage/"+perso.type, str(i)+str(j)))
          self.iPerso.append(iMPerso)

        self.donjon = GenerationDonjon.genererDonjon(__main__.nombreEtage) #Chargement du contenu du donjon
        chargerTextures(self.texture) #Chargement des textures

        pygame.draw.rect(self.fenetre, [0, 0, 0], [0, 0, 784, 320], 0) #Affiche les contrôles
        font = pygame.font.SysFont('constantia', 28)
        text = font.render("Se déplacer", 1, (255,255,255))
        text1 = font.render("Ctrl:      Attaquer au corps à corps", 1, (255,255,255))
        text2 = font.render("Alt:       Faire une attaque spéciale", 1, (255,255,255))
        self.fenetre.blit(text,(120, 30))
        self.fenetre.blit(text1,(30, 130))
        self.fenetre.blit(text2,(30, 230))
        self.fenetre.blit(image[4], (10, 10))
        pygame.display.flip()
        while pygame.event.wait().type != pygame.locals.KEYDOWN: #On attend que le personnage appui sur une touche pour reprendre le programme
            None

        afficherCarte(self.donjon[perso.Etage])
        self.epee = image[3]
        self.creerPiece()
        self.continuer = True
        self.jauges = []


    #---------Boucle principale--------#

    def run(self):
        pygame.draw.rect(self.fenetre, [0, 0, 0], [0, 0, 621, 32], 0)
        self.fenetre.blit(self.iPerso[perso.dir][0], (perso.pos[0]*32+32, perso.pos[1]*32+64))
        self.jauges.append(Jauge(self.fenetre, [255, 0, 0], 1, " ", [206, 20], [0,0]))
        self.majOr(perso.OR)
        if perso.type == 'Magicien':
            self.jauges.append(Jauge(self.fenetre, [0, 0, 255], 2, " ", [206, 20], [240,0]))
            self.jauges[1].majJauge(perso.mana, perso.manaMax)
        self.jauges[0].majJauge(perso.pv, perso.pvMax)
        debug('MoteurGraphique.run()')
        Audio.stageMusic(perso.Etage)
        self.startMob() #Initialise les monstres
        self.afficherPiece()

        while(self.continuer):
            for event in pygame.event.get(): #On propose au joueur d'agir en appuyant sur une touche
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        self.tryBougerPerso(1,0,1)
                    elif event.key == K_LEFT:
                        self.tryBougerPerso(-1,0,3)
                    elif event.key == K_UP:
                        self.tryBougerPerso(0,-1,0)
                    elif event.key == K_DOWN:
                        self.tryBougerPerso(0,1,2)
                    elif event.key == K_F6 and debugMode:
                        perso.mourir()
                    elif event.key == K_F1 and debugMode:
                        for i in self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites:
                            i.perdrePv(100000)
                    elif event.key == K_F2 and debugMode:
                        perso.perdrePv(5)
                    elif event.key == K_F3 and debugMode:
                        perso.gagnerPv(5)
                    elif event.key == K_F7 and debugMode:
                        if len(self.projectile) < 1:
                            self.projectile.append(Projectile(1, [perso.pos[0]+posi(perso.dir, 0), perso.pos[1]+posi(perso.dir, 1)], perso.dir, 100, 10))
                            self.projectile[len(self.projectile)-1].start()
                    elif event.key == K_LCTRL:
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        self.attaquer()
                        pygame.event.set_allowed(pygame.KEYDOWN)
                    elif event.key == K_LALT:
                        pygame.event.set_blocked(pygame.KEYDOWN)
                        perso.special()
                        self.wait(300)
                        pygame.event.set_allowed(pygame.KEYDOWN)
                    elif event.key == K_F10:
                        self.mort(perso)
                elif event.type == QUIT:
                    self.continuer = 0

            for i in self.projectile: #Supprime les projectiles inactifs
                if not i.ok:
                    self.projectile.remove(i)
            self.afficherPiece() #Affiche la pièce

        sleep(6)
        pygame.display.quit()
        #pygame.quit()
        print('moteur stop')

    def creerPiece(self):
        global perso
        self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].decouvert = True #Permet à la pièce découverte d'être affichée sur la carte
        self.piece = []

        if perso.Etage != 0 and perso.Room == [5,5]:
            self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].grille[3][6] = 4

        for x in range (13): #Facilite l'affichage des blocs de la pièce
          case = []
          for y in range (7):
            if self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].grille[y][x] == 0:
                case.append('case')
            elif self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].grille[y][x] == 1:
                case.append('rocher')
            elif self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].grille[y][x] == 2:
                case.append('trou')
            elif self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].grille[y][x] == 3:
                case.append('coffre')
            elif self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].grille[y][x] == 4:
                case.append('entree')
            elif self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].grille[y][x] == 5:
                case.append('sortie')
          self.piece.append(case)

        self.porte = []
        for i in range (4):
          self.porte.append(self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].porte[i])

        self.boss = (self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].__class__.__name__ == 'SalleBoss')

        self.affMap()#Affiche la carte

    def afficherPiece(self):
        global perso
        self.fenetre.blit(block[perso.Etage]['sol'],(0, 32))

        for x in range(13): #On affiche les blocs
            for y in range(7):
                if self.piece[x][y] != 'case':
                    self.fenetre.blit(block[perso.Etage][self.piece[x][y]],(px(x), py(y)))

        if self.porte[0]: #On affiche les portes
            self.fenetre.blit(block[perso.Etage]['case'],(224, 32))
        if self.porte[1]:
            self.fenetre.blit(block[perso.Etage]['case'],(448, 160))
        if self.porte[2]:
            self.fenetre.blit(block[perso.Etage]['case'],(224, 288))
        if self.porte[3]:
            self.fenetre.blit(block[perso.Etage]['case'],(0, 160))

        self.majEntites() #On affiche les monstres

        if self.posEpee != [0, 0]: #On affiche l'arme du personnage s'il y a lieu
            self.fenetre.blit(self.epee, (self.posEpee[0], self.posEpee[1]))

        self.fenetre.blit(self.iPerso[perso.dir][self.marche], (px(perso.pos[0])+self.mPos[0], py(perso.pos[1])+self.mPos[1]))

        for i in self.projectile: #On affiche les projectiles
            self.fenetre.blit(i.type, (px(i.pos[0])+i.mPos[0], py(i.pos[1])+i.mPos[1]))
        pygame.display.flip()

    def tryBougerPerso(self, dx, dy, p):
        global perso
        if perso.dir == p:
            pos = [perso.pos[0]+dx, perso.pos[1]+dy]
            if (pos[0] == 6 and pos[1] == -1 and self.porte[0]) or (pos[0] == 13 and pos[1] == 3 and self.porte[1]) or (pos[0] == 6 and pos[1] == 7 and self.porte[2]) or (pos[0] == -1 and pos[1] == 3 and self.porte[3]):
                self.bougerPiece(self.piece, self.porte, -dx, -dy)
            elif perso.pos[0]+dx < 13 and perso.pos[1]+dy > -1 and perso.pos[1]+dy < 7 and perso.pos[0]+dx > -1:#si le perso peut avancer
              case = self.piece[perso.pos[0]+dx][perso.pos[1]+dy]
              mob = 0
              for i in self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites:
                  if i.pos[0] == perso.pos[0]+dx and i.pos[1] == perso.pos[1]+dy:
                      mob = 1
              if  case != 'rocher' and case != 'trou' and (not mob or case == 'coffre'):
                  self.bougerPerso(dx, dy, 1)

        if self.piece[perso.pos[0]][perso.pos[1]] == 'coffre': #Récupère le contenu du coffre
            self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].grille[perso.pos[1]][perso.pos[0]] = 0
            self.piece[perso.pos[0]][perso.pos[1]] = 'case'
            self.fenetre.blit(block[perso.Etage]['case'], (px(perso.pos[0]), px(perso.pos[1])))
            perso.gagnerOR(Coffre.gagnerOR(perso.Etage))
            self.majOr(perso.OR)

        if perso.pos[0] == 6 and perso.pos[1] == 3 and perso.Room == [5,5] and perso.Etage != 0 and perso.dir == p: #Descend d'un étage si le personnage est sur un escalier
            self.bougerEtage()
            perso.Etage = perso.Etage-1
            perso.Room = [self.donjon[perso.Etage].posBoss[1], self.donjon[perso.Etage].posBoss[0]]
            self.startMob()
            self.creerPiece()
            self.afficherPiece()
            Audio.stageMusic(perso.Etage)
        elif perso.pos[0] == 6 and perso.pos[1] == 3 and self.piece[6][3] == 'sortie' and perso.dir == p: #Monte d'un étage si le personnage est sur un escalier
            if perso.Etage != 4:
               self.bougerEtage()
               perso.Etage = perso.Etage+1
               perso.Room = [5,5]
               self.startMob()
               self.creerPiece()
               self.afficherPiece()
               afficherCarte(self.donjon[perso.Etage])
               Audio.stageMusic(perso.Etage)
            else: #Ferme la fenêtre si le personnage fini le jeu
                self.stop()

        perso.dir = p

    def bougerPerso(self, dx, dy, cp):
        global perso
        for i in range(3): #Execute l'animation de la marche du personnage
            for j in range(11):
                self.wait(8)
                self.mPos = [dx*(i*11+j), dy*(i*11+j)]
                self.marche = i #Image du personnage à utiliser (pieds droit ou pieds gauche)
        self.mPos = [0, 0] #Petite position intermédiaire du personnage (entre 0 et 32)
        pygame.draw.rect(self.fenetre, [200, 200, 200], [484+(perso.Room[1]*15+perso.pos[0])*2, 36+(perso.Room[0]*9+perso.pos[1])*2, 2, 2], 0)
        perso.pos = [perso.pos[0]+dx, perso.pos[1]+dy]
        pygame.draw.rect(self.fenetre, [255, 0, 0], [484+(perso.Room[1]*15+perso.pos[0])*2, 36+(perso.Room[0]*9+perso.pos[1])*2, 2, 2], 0)

    def bougerPiece(self, prPiece, prPorte, dx, dy):
        global perso
        prRoom = perso.Room
        prBoss = self.boss
        self.bougerPerso(-dx, -dy, 0)

        for i in self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites:
            i.actif = False

        perso.Room = [perso.Room[0]-dy, perso.Room[1]-dx]
        self.creerPiece()

        if self.boss: #Si le personnage entre dans une salle de boss
            Audio.bossMusic(perso.Etage)
        elif prBoss: #Si le personnage sors d'une salle de boss
            Audio.stageMusic(perso.Etage)

        for i in range (289+dx*dx*192):
            t1 = pygame.time.get_ticks()
            self.fenetre.blit(block[perso.Etage]['sol'],(i*dx, 32+i*dy)) #affiche le fond
            self.fenetre.blit(block[perso.Etage]['sol'],((i-480)*dx, 32+(i-288)*dy))

            for x in range(13):#On affiche les blocs des deux pièces
                for y in range(7):
                    if prPiece[x][y] != 'case':
                        self.fenetre.blit(block[perso.Etage][prPiece[x][y]],(px(x)+i*dx, py(y)+i*dy))
                    if self.piece[x][y] != 'case':
                        self.fenetre.blit(block[perso.Etage][self.piece[x][y]],(px(x)+(-240*(1+dx)+240*(-1+dx)+i)*dx, py(y)+(-144*(1+dy)+144*(-1+dy)+i)*dy))

            for j in self.donjon[perso.Etage].grille[prRoom[0]][prRoom[1]].entites: #On affiche les mobs de la pièce précédente
                if prBoss:
                    self.fenetre.blit(iBoss[perso.Etage][j.dir][0], (px(j.pos[0])+i*dx, py(j.pos[1])+i*dy))
                else:
                    self.fenetre.blit(iEntite[j.type][j.num][j.dir], (px(j.pos[0])+i*dx, py(j.pos[1])+i*dy))

            for j in self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites: #On affiche les mobs de la pièce suivante
                if self.boss:
                    self.fenetre.blit(iBoss[perso.Etage][j.dir][0], (px(j.pos[0])+(-240*(1+dx)+240*(-1+dx)+i)*dx, py(j.pos[1])+(-144*(1+dy)+144*(-1+dy)+i)*dy))
                else:
                    self.fenetre.blit(iEntite[j.type][j.num][j.dir], (px(j.pos[0])+(-240*(1+dx)+240*(-1+dx)+i)*dx, py(j.pos[1])+(-144*(1+dy)+144*(-1+dy)+i)*dy))

            if prPorte[0]:#affiche les portes de la première pièce
                self.fenetre.blit(block[perso.Etage]['case'],(224+i*dx, 32+i*dy))
            if prPorte[1]:
                self.fenetre.blit(block[perso.Etage]['case'],(448+i*dx, 160+i*dy))
            if prPorte[2]:
                self.fenetre.blit(block[perso.Etage]['case'],(224+i*dx, 288+i*dy))
            if prPorte[3]:
                self.fenetre.blit(block[perso.Etage]['case'],(0+i*dx, 160+i*dy))

            if self.porte[0]:#affiche les portes de la deuxième pièce
                self.fenetre.blit(block[perso.Etage]['case'],(224+(i-480)*dx, 32+(i-288)*dy))
            if self.porte[1]:
                self.fenetre.blit(block[perso.Etage]['case'],(448+(i-480)*dx, 160+(i-288)*dy))
            if self.porte[2]:
                self.fenetre.blit(block[perso.Etage]['case'],(224+(i-480)*dx, 288+(i-288)*dy))
            if self.porte[3]:
                self.fenetre.blit(block[perso.Etage]['case'],(0+(i-480)*dx, 160+(i-288)*dy))

            self.fenetre.blit(self.iPerso[perso.dir][0], (px(perso.pos[0])+dx*i, py(perso.pos[1])+dy*i))#affiche le perso

            for j in self.projectile:#On affiche les projectiles
                self.fenetre.blit(j.type, (px(j.pos[0])+j.mPos[0]+dx*i, py(j.pos[1])+j.mPos[1]+dy*i))

            pygame.draw.rect(self.fenetre, [0, 0, 0], [0, 0, 621, 32], 0) #On affiche le contour du donjon
            pygame.draw.rect(self.fenetre, [0, 0, 0], [480, 32, 304, 320], 0)
            pygame.draw.rect(self.fenetre, [140, 50, 0], [481, 33, 301, 181], 4)
            self.majOr(perso.OR)

            for i in self.jauges: #On affiche les jauges
                i.affJauge()
            pygame.display.flip()

            t2 = pygame.time.get_ticks() #Limite la vitesse de la boucle à 3 ms/tour
            while t2 < t1+3:
                t2 = pygame.time.get_ticks()

        self.projectile = []
        self.affMap()
        perso.pos = [6+7*dx, 3+4*dy]
        self.startMob()
        self.bougerPerso(-dx, -dy, 0)

    def bougerEtage(self):
        global perso
        for i in self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites: #Desactive les monstres de la pièce
            i.actif = False
        for i in range(180): #Execute l'animation du changement d'étage
            piece = pygame.transform.rotate(block[perso.Etage]['sol'], i)
            self.fenetre.blit(piece, (sin(i)*240, cos(i)*288))
            pygame.draw.rect(self.fenetre, [0, 0, 0], [0, 0, 784, 32], 0)
            pygame.draw.rect(self.fenetre, [0, 0, 0], [480, 32, 304, 320], 0)
            pygame.draw.rect(self.fenetre, [140, 50, 0], [481, 33, 301, 181], 4)
            self.majOr(perso.OR)
            for i in self.jauges:
                i.affJauge()

            pygame.display.flip()
            pygame.time.delay(2) #Attend 2 ms

    def attaquer(self):
        global perso
        self.epee = pygame.transform.rotate(image[3], -(perso.dir+1)*90) #Tourne l'épée dans le sens du personnage
        posX = posi(perso.dir, 0)
        posY = posi(perso.dir, 1)

        for j in range(90):
            self.wait(2)
            self.epee = pygame.transform.rotate(image[3], -(perso.dir+1)*90+j)
            #self.posEpee = [(perso.pos[0]+1)*32+posX*(j*(1-2*i)+2+i*20), (perso.pos[1]+2)*32+posY*(j*(1-2*i)+i*20)]
            self.posEpee = [px(perso.pos[0])-posY*16+sin(j*0.01745)*16*(posX+posY), py(perso.pos[1])+posX*16+sin(j*0.01745)*16*(-posX+posY)] #j*0.01745: conversion degré/radian
            #La fonction rotate() fait tourner l'image par rapport à son centre, la formule utilisée permet de faire tourner l'épée par rapport à sa base

        self.posEpee = [0,0]
        perso.attaquer()

    def mort(self, entite): #Fontion non utilisée
        global perso
        if type(entite) == type(perso):
            image = self.iPerso[perso.dir][0]
        else:
            image = iEntite[entite.type][entite.num][entite.dir]

        for i in range(90):
            iCreature = pygame.transform.rotate(image, i)
            self.fenetre.blit(block[perso.Etage]['case'], (entite.pos[0]*32+32, entite.pos[1]*32+64))
            self.fenetre.blit(iCreature, (entite.pos[0]*32+32, entite.pos[1]*32+64))
            pygame.display.flip()
            self.wait(10)

    def startMob(self):
        self.entite = self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites
        self.posMob = []
        self.pPosMob = []
        self.marcheMob = [] #Images de marche des monstres
        for i in self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites:
            try: #les monstres mettent du temps à comprendre qu'ils sont false
                i.start()
                pos = []
                pPos = []
                marcheMob = 0
                for j in range(2):
                    pos.append(i.pos[j])
                    pPos.append(0)
                self.posMob.append(pos)
                self.pPosMob.append(pPos)
                self.marcheMob.append(marcheMob)
            except:
                None

    def majEntites(self):
        for i in range(len(self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites)): #On supprime les monstres morts
            if self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites[i].actif == False:
                type = self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites[i].type
                del self.posMob[i]
                del self.pPosMob[i]
                del self.marcheMob[i]
                del self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites[i]
                #self.mort(entite)
                if type == 2:
                    pygame.time.delay(5000)
                    print(self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites)
                if self.boss and self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites == []:
                    self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].grille[3][6] = 5
                    self.piece[6][3] = 'sortie'
                break

        j = 0
        for i in self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites: #Affiche les monstres
            if (self.posMob[j][0]*32+self.pPosMob[j][0] != i.pos[0]*32) or (self.posMob[j][1]*32+self.pPosMob[j][1] != i.pos[1]*32):
                t2 = pygame.time.get_ticks()
                if t2 >= self.t1+10: #Affiche la pièce pendant 10 ms avant de reprendre la suite du programme
                    self.t1 = pygame.time.get_ticks()
                    self.pPosMob[j] = [self.pPosMob[j][0]+posi(i.dir, 0), self.pPosMob[j][1]+posi(i.dir, 1)]
                    if (abs(self.pPosMob[j][0]) <= 11 and self.pPosMob[j][1] == 0) or (self.pPosMob[j][0] == 0 and abs(self.pPosMob[j][1]) <= 11): #On détermine la marche du mob
                        self.marcheMob[j] = 0
                    elif (abs(self.pPosMob[j][0]) <= 22 and self.pPosMob[j][1] == 0) or (self.pPosMob[j][0] == 0 and abs(self.pPosMob[j][1]) <= 22):
                        self.marcheMob[j] = 1
                    else:
                        self.marcheMob[j] = 2
            else:
                self.posMob[j] = [i.pos[0], i.pos[1]]
                self.pPosMob[j] = [0, 0]
                self.marcheMob[j] = 0

            if (self.posMob[j][0] < i.pos[0]-1) or (self.posMob[j][1] < i.pos[1]-1) or (self.posMob[j][0] > i.pos[0]+1) or (self.posMob[j][1] > i.pos[1]+1):
                self.posMob[j] = i.pos
                self.pPosMob[j] = [0,0]
                self.marcheMob[j] = 0

            if i.type == 2: #Les boss sont de type 2 et les monstres normaux de type 1 ou 2
                self.fenetre.blit(iBoss[perso.Etage][i.dir][self.marcheMob[j]], (px(self.posMob[j][0])+self.pPosMob[j][0], py(self.posMob[j][1])+self.pPosMob[j][1]))
            else:
                self.fenetre.blit(iEntite[i.type][i.num][i.dir], (px(self.posMob[j][0])+self.pPosMob[j][0], py(self.posMob[j][1])+self.pPosMob[j][1]))
            j = j+1

    def majOr(self, argent):
        pygame.draw.rect(self.fenetre, [0, 0, 0], [480, 0, 141, 32], 0)
        self.fenetre.blit(image[0],(480, 0))
        font = pygame.font.SysFont('constantia', 28)
        text = font.render(":  "+str(argent), 1, (255,220,50))
        self.fenetre.blit(text,(508, 0))

    def affMap(self):
        pygame.draw.rect(self.fenetre, [0, 0, 0], [480, 32, 304, 320], 0)
        pygame.draw.rect(self.fenetre, [140, 50, 0], [481, 33, 301, 181], 4)

        for x2 in range(10): #position de la pièce
            for y2 in range(10): #position de la pièce
                for x in range(13): #position du bloc dans la pièce
                    for y in range (7):
                        point = 0
                        mur = 0
                        coffre = [0, 0, 0]
                        try:
                            if self.donjon[perso.Etage].grille[y2][x2].decouvert: #Vérifie que la pièce est découverte pour l'afficher
                                if self.donjon[perso.Etage].grille[y2][x2].grille[y][x] < 4:
                                    point = self.donjon[perso.Etage].grille[y2][x2].grille[y][x]*65
                                if self.donjon[perso.Etage].grille[y2][x2].grille[y][x] == 3:
                                    point = 0
                                    coffre = [55, 20, -150]
                            else:
                                mur = 200
                        except:
                            mur = 200
                        pygame.draw.rect(self.fenetre, [200-mur-point+coffre[0], 200-mur-point+coffre[1], 200-mur-point+coffre[2]], [484+(15*x2+x)*2, 36+(9*y2+y)*2, 2, 2], 0)

    def stop(self): #Arrête le moteur graphique
        debug('MoteurGraphique.stop()')
        for i in self.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites:
            i.actif = False

        self.projectile = None
        self.donjon = None
        self.continuer = False

    def wait(self, time): #Affiche la pièce en arrêtant le reste du programme pendant time ms
        t1 = pygame.time.get_ticks()
        t2 = t1
        while t2 <= t1+time:
            self.afficherPiece()
            t2 = pygame.time.get_ticks()

#---------Définition des classes-------#

class Jauge():
    def __init__(self, fenetre, rgb, icon, ligne, size, pos):
        self.fenetre = fenetre
        self.rgb = rgb
        self.size = size
        self.icon = icon
        self.ligne = ligne
        self.pos = pos
        self.font = pygame.font.SysFont('constantia', size[1])
        self.text = self.font.render(ligne, 1, (rgb[0],rgb[1],rgb[2]))
        self.reste = 1

    def majJauge(self, nb, nbMax):
        self.posText = self.pos[0]+32+(self.size[0]-len(str(nb)+" / "+str(nbMax))*8)/2
        self.text = self.font.render(str(nb)+" / "+str(nbMax), 1, (self.rgb[0],self.rgb[1],self.rgb[2]))
        self.reste = nb/nbMax
        self.affJauge()

    def affJauge(self):
        pygame.draw.rect(self.fenetre, [0, 0, 0], [self.pos[0], self.pos[1], 238, 32], 0)
        pygame.draw.rect(self.fenetre, [self.rgb[0]*0.6, self.rgb[1]*0.6, self.rgb[2]*0.6], [self.pos[0]+32, self.pos[1]+6, self.size[0]*self.reste, self.size[1]], 0)
        pygame.draw.rect(self.fenetre, [self.rgb[0], self.rgb[1], self.rgb[2]], [self.pos[0]+32, self.pos[1]+6, self.size[0], self.size[1]], 2)
        self.fenetre.blit(image[self.icon], (self.pos[0], self.pos[1]))
        self.fenetre.blit(self.text, (self.posText, self.pos[1]+6))

class Projectile(threading.Thread):
    def __init__(self, typ, pos, dir, degats, pene):
        threading.Thread.__init__(self)
        self.typ = typ
        self.type = pygame.transform.rotate(iProj[typ], -dir*90) #Image du projectile
        self.vitesse = 3 #Vitesse du projectile
        self.dir = [posi(dir, 0), posi(dir, 1)]
        self.pos = pos #Position du projectile
        self.mPos = [0, 0] #Petite position intermédaire (entre 0 et 32)
        self.degats = degats
        self.pene = pene
        self.ok = True #Le projectile est actif

    def run(self):
        while(self.ok):
            self.mPos = [self.mPos[0]+self.dir[0], self.mPos[1]+self.dir[1]]

            t1 = pygame.time.get_ticks()
            t2 = t1
            while t2 <= t1+self.vitesse: #On fait une pause dépendant de la vitesse
                t2 = pygame.time.get_ticks()

            if self.mPos[0] >= 32: #Si la petite position atteint 32, on incrémente la position global
                self.mPos[0] = 0
                self.pos[0] = self.pos[0]+1
            elif self.mPos[0] <= -32:
                self.mPos[0] = 0
                self.pos[0] = self.pos[0]-1
            if self.mPos[1] >= 32:
                self.mPos[1] = 0
                self.pos[1] = self.pos[1]+1
            elif self.mPos[1] <= -32:
                self.mPos[1] = 0
                self.pos[1] = self.pos[1]-1

            if self.pos == [perso.pos[0], perso.pos[1]]:  #Le projectile touche le personnage
                perso.perdrePv(self.degats)
                self.ok = False

            for i in __main__.motGraph.donjon[perso.Etage].grille[perso.Room[0]][perso.Room[1]].entites: #Si une entité est touché par le projectile elle subit des dégats
                if self.pos == i.pos:
                    i.perdrePv(self.degats)
                    self.ok = False

            if self.pos[0] < 0 or self.pos[0] > 12 or self.pos[1] < 0 or self.pos[1] > 6 or (__main__.motGraph.piece[self.pos[0]][self.pos[1]] == 'rocher' and self.typ == 1):
                self.ok = False #Si le projectile rencontre un obstacle, il est détruit

#--------Définition des fonctions------#

def lancerProjectile(type, pos, dir, degats, pene, sound):
    if len(__main__.motGraph.projectile) <= 3:
        __main__.motGraph.projectile.append(Projectile(type, pos, dir, degats, False))
        __main__.motGraph.projectile[-1].start()
        Audio.playSound(sound)
        return True
    else:
        return False

def chargerTextures(pack):
    try:
        global block, image, iEntite
        if perso.type == 'Magicien':
            epee = 'baton'
        elif perso.type == 'Barbare':
            epee = 'hache'
        elif perso.type == 'Ninja':
            epee = 'kunai'
        elif perso.type == 'Archer':
            epee = 'fleche'
        else:
            epee = 'epee'
    except:
        epee = 'epee'
        print('bug perso')

    lTextures = ['case', 'rocher', 'trou', 'coffre', 'entree', 'sortie', 'sol']
    lImages = ['piece', 'coeur', 'magie', epee, 'directionel']
    lProjectiles = ['bouleDeFeu', 'fleche']

    for i in lImages:
        image.append(chargerImage(pack, i))

    for i in lProjectiles:
        iProj.append(chargerImage(pack, i))

    for etage in range(5):
        eBlock = {}
        for i in lTextures:
            eBlock[i] = chargerTile(pack, etage, i)
        block.append(eBlock)

    for i in range(2):
        tEntite = []
        for j in range(len(listdir('Entites/Monstres/'+str(i)))-1):
            pEntite = []
            for k in range(4):
                pEntite.append(chargerSprite(pack, "Monstres/"+str(i), str(j)+"/"+str(k)))
            tEntite.append(pEntite)
        iEntite.append(tEntite)

    for i in range(5):
        pBoss = []
        for j in range(4):
            mBoss = []
            for k in range(3):
                mBoss.append(chargerSprite(pack, "Boss/"+str(i), str(j)+str(k)))
            pBoss.append(mBoss)
        iBoss.append(pBoss)

def chargerTile(pack, etage, nom): #Dossier relatif aux blocs
    try:
        return pygame.image.load("TexturePack/"+pack+"/Tiles/"+str(etage)+"/"+nom+".gif").convert_alpha()
    except:
        return pygame.image.load("TexturePack/Default/Tiles/"+str(etage)+"/"+nom+".gif").convert_alpha()

def chargerSprite(pack, typ, nom): #Dossier relatif aux entités
    try:
        return pygame.image.load("TexturePack/"+pack+"/Sprites/"+typ+"/"+nom+".gif").convert_alpha()
    except:
        return pygame.image.load("TexturePack/Default/Sprites/"+typ+"/"+nom+".gif").convert_alpha()

def chargerImage(pack, nom): #Les différentes images
    try:
        return pygame.image.load("TexturePack/"+pack+"/Images/"+nom+".gif").convert_alpha()
    except:
        return pygame.image.load("TexturePack/Default/Images/"+nom+".gif").convert_alpha()

def posi(dir, axe):#Donne le déplacement en x et en y en fonction de l'orientation
    if dir == 0:
        pos = [0, -1]
    elif dir == 1:
        pos = [1, 0]
    elif dir == 2:
        pos = [0, 1]
    elif dir == 3:
        pos = [-1, 0]
    return pos[axe]

def px(x): #Simplifie le code
    return (x+1)*32
def py(y):
    return (y+2)*32
def abs(nb): #Valeur absolue
    if nb < 0:
        nb = -nb
    return nb
