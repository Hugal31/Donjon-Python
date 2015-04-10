#!/usr/bin/env python3.4

########################################
#------------Donjon & Python-----------#
#---------------Monstres---------------#
#--------------------------------------#
#-----------------v1.0-----------------#
#--------------------------------------#
#---------------02/03/2014-------------#
########################################

#-----------Import des modules---------#

from threading import Thread    #Un thread permet de lancer un script (ex: while 1) sans bloquer le reste du programme
from random import randint
from time import sleep

import __main__
from Debug import debug
from random import random
import Audio
import Fonctions
import MoteurGraphique

#---------Définition des classes-------#

class Monstre(Thread):  #Monstre hérite de Thread
    """Classe abstraite de monstre"""
    def __init__(self, num, attributs, pos, salle):
        Thread.__init__(self)   #On initialise le Thread
        self.num = num
        self.actif = False      #Boolean  qui vérifie que le monstre est à l'écran
        self.vivant = True
        self.salle = salle
        self.nom = attributs['nom']
        self.pv = int(attributs['pv']) * (__main__.numPartie+1) * (self.salle.etage + 1)
        self.dmg = int(attributs['dmg']) * (__main__.numPartie+1) * (self.salle.etage + 1)
        self.deff = int(attributs['deff']) * (__main__.numPartie+1) * (self.salle.etage + 1)
        self.vit = int(attributs['vitesse'])
        self.dir = 3
        self.pos = pos          #Liste de deux cases
        self.pPos = [0, 0]

    def perdrePv(self, valeur, perceArmure=False):
        if perceArmure : self.pv -= valeur
        else : self.pv -= valeur - int(valeur*self.deff/100)
        if self.pv <= 0 and self.vivant:
            self.mourir()
        self.dir = (__main__.perso.dir+2)%4

    def bouger(self):
        coord = Fonctions.autour(self.dir, self.pos[0], self.pos[1],  12, 6)
        if coord[2]:
            obstacle = collision(self.salle, coord[0], coord[1])
            if not obstacle[0] and not obstacle[1] : self.pos = [coord[0], coord[1]]  #Avancer
            elif obstacle[1] : self.attaquer()
            else : self.changerDir()
        else : self.changerDir()

    def attaquer(self):
        __main__.perso.perdrePv(self.dmg)

    def changerDir(self):
        devant = Fonctions.autour(self.dir, self.pos[0], self.pos[1], 12, 6)
        while collision(self.salle, devant[0], devant[1])[0] or not devant[2]:
            self.dir = (randint(1, 3)+self.dir)%4
            devant = Fonctions.autour(self.dir, self.pos[0], self.pos[1], 12, 6)

    def mourir(self):
        self.vivant = False
        self.actif = False
        Audio.playSound('Goblin')
        __main__.perso.gagnerOR()
        #A remplacer par des potions
        __main__.perso.gagnerPv(int(self.dmg/10))
        if __main__.perso.__class__.__name__ == 'Magicien' : __main__.perso.gagnerMana(int(self.dmg/10))

    def run(self):
        """Démarrage de l'IA"""
        self.actif = True
        self.dir = randint(0, 3)
        sleep(self.vit)
        while self.actif and self.vivant:
            if not(self.ia()) : self.bouger()
            sleep(self.vit)
        if self.vivant : Thread.__init__(self)

    def ia(self):
        """IA du monstre"""
        return False


class CaC(Monstre):
    """IA de monstre au CaC"""
    def __init__(self, num, attributs, pos, salle):
        Monstre.__init__(self, num, attributs, pos, salle)
        self.type = 0


class Distance(Monstre):
    def __init__(self, num, attributs, pos, salle):
        Monstre.__init__(self, num, attributs, pos, salle)
        self.typeProj = int(attributs['projectile'])
        self.type = 1

    def ia(self):
        if __main__.perso.pos[0] == self.pos[0]:
            if __main__.perso.pos[1] < self.pos[1] :
                if self.dir != 0 : self.dir = 0
                else : self.attaquer()
            else :
                if self.dir != 2 : self.dir = 2
                else : self.attaquer()
            return True
        elif __main__.perso.pos[1] == self.pos[1]:
            if __main__.perso.pos[0] < self.pos[0] :
                if self.dir != 3 : self.dir = 3
                else : self.attaquer()
            else :
                if self.dir != 1 : self.dir = 1
                else : self.attaquer()
            return True
        else : return False

    def attaquer(self):
        """Attaque le joueur a distance"""
        coord = Fonctions.autour(self.dir, self.pos[0], self.pos[1], 12, 6)
        if coord[2] : MoteurGraphique.lancerProjectile(self.typeProj, [coord[0], coord[1]], self.dir, self.dmg, False, 'Arrow')


class Boss(Monstre):
    def __init__(self, etage, attributs, pos, salle):
        Monstre.__init__(self, etage, attributs, pos, salle)
        self.type = 2


class RoiSlime(Boss):    #Boss de l'étage 1
    def __init__(self, num, attributs, pos, salle):
        Boss.__init__(self, num, attributs, pos, salle)

    def run(self):          #Redéfinition de run pour appliquer un effet à la fin
        """Démarrage de l'IA"""
        self.actif = True
        self.dir = randint(0, 3)
        sleep(self.vit)
        while self.actif and self.vivant:
            if not(self.ia()) : self.bouger()
            sleep(self.vit)
        if self.vivant :
            Thread.__init__(self)
        else : #Faire spawner deux monstres plus petits
            self.salle.entites.append(placerMonstre(0, 0, (self.pos[0], self.pos[1]), self.salle, 1, 0))
            self.salle.entites.append(placerMonstre(0, 0, (self.pos[0]+1, self.pos[1]), self.salle, 1, 0))
            __main__.motGraph.startMob()

#--------Définition des fonctions------#

def collision(salle, x, y):
    obstacle = False
    ennemi = False
    if salle.grille[y][x] != 0 : obstacle = True
    if __main__.perso.pos == [x, y]:
        obtacle = True
        ennemi = True
    for i in salle.entites:
        if i.pos[0] == x and i.pos[1] == y:
            obstacle = True
        break
    return obstacle, ennemi

def placerMonstre(etage, typ, pos, salle, prob=0.9, num=-1, boss=False):
    global index
    if random() <= prob:
        try:    #Au cas où
            if boss:
                fichier = open('Entites/Boss/'+str(etage)+'.txt')
            else:
                if num == -1 : num = int(index[typ][etage][randint(0, len(index[typ][etage])-1)])
                fichier = open('Entites/Monstres/'+str(typ)+'/'+str(num)+'.txt', mode='r', encoding='Utf-8')
            attributs = {}
            ligne = fichier.readline()
            while ligne != '' :
                ligne = ligne.split('=')
                attributs[ligne[0]] = ligne[1]
                ligne = fichier.readline()
            fichier.close()
            if typ == 0 :
                return CaC(num, attributs, pos, salle)
            elif typ == 1:
                return Distance(num, attributs, pos, salle)
            else:
                if etage == 0 : return RoiSlime(etage, attributs, pos, salle)
                debug('Boss remplacé')
                return Boss(etage, attributs, pos, salle)
        except Exception as e:
            debug('Monstre de type ' + str(typ) + ' et de num ' + str(num) + " a l'étage " + str(etage) + ' non généré :' + '\n'
                  + str(type(e)) + ' : ' + str(e))
            return 0
    else : return 0

def indexer():
    """Crée un index pour savoir quels monstres se trouve à tel étage"""
    global index
    for typ in range(2):
        index.append([])
        fichier = open('Entites/Monstres/'+str(typ)+'/index.txt', mode='r', encoding='Utf-8')
        text = ''.join(fichier.readlines())
        fichier.close()
        text = text.split('\n')
        for etage in range(len(text)):
            ligne = text[etage].split(',')
            index[typ].append(ligne)

#-----------Boucle principale----------#

index = []
indexer()

if __name__ == '__main__':
    numPartie = 0
    monstre = placerMonstre(0, 0)
    print(monstre.nom)
