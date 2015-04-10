#!/usr/bin/env python3.4

########################################
#------------Donjon & Python-----------#
#---------------Personnage-------------#
#--------------------------------------#
#-----------------v1.0-----------------#
#--------------------------------------#
#------------Tristan Le Saux-----------#
#---------------02/03/2014-------------#
########################################

#-----------Import des modules---------#

from time import sleep
import random

import Audio
import Magasin
import Menu
import __main__
import Fonctions
from Debug import debug
import Coffre

from MoteurGraphique import lancerProjectile

#---------Définition des classes-------#

class Personnage:
    def __init__(self, pv, atk, deff, critDmg, critChc, multOR, attributs, mana):
        self.type = 'Guerrier'
        self.majCarac(pv, atk, deff, critDmg, critChc, multOR, mana)
        self.OR = 0
        # self.attributs = attributs #Dictionnaire (Nain, alzheimer, ne connait pas la douleur, etc...)
        self.Etage = 0
        self.Room = [5, 5]
        self.pos = [6, 3]
        self.dir = 2

    def majCarac(self, pv, atk, deff, critDmg, critChc, multOR, mana):
        """Met à jour les caractéristiques du personnage"""
        self.pv = int(pv+0.5)   #Le 0.5 permet d'arrondir
        self.pvMax = int(pv+.5)
        self.atk = int(atk+.5)
        self.deff = int(deff+.5)
        self.critDmg = int(critDmg+.5)
        self.critChc = int(critChc+.5)
        self.multOR = multOR

    def gagnerOR(self, valeur=-1):
        if valeur == -1:
            valeur = Coffre.gagnerOR(self.Etage)
        self.OR += int(valeur*self.multOR/100 +0.5)
        __main__.motGraph.majOr(self.OR)

    def gagnerPv(self, valeur):
        Audio.playSound('Potion')
        if (self.pv + valeur) > self.pvMax : self.pv = self.pvMax
        else : self.pv += valeur
        __main__.motGraph.jauges[0].majJauge(self.pv, self.pvMax)

    def perdrePv(self, valeur, perceArmure = False):
        Audio.playSound('Hurt')
        if perceArmure : self.pv -= valeur
        else : self.pv -= valeur - int(valeur*self.deff/100)
        if self.pv <= 0 : self.mourir()
        else : __main__.motGraph.jauges[0].majJauge(self.pv, self.pvMax)

    def attaquer(self):
        cible = Fonctions.autour(self.dir, self.pos[0], self.pos[1], 12, 9)
        Audio.playSound('Sword')
        for i in __main__.motGraph.donjon[self.Etage].grille[self.Room[0]][self.Room[1]].entites:
            if i.pos == [cible[0], cible[1]] :
                i.perdrePv((random.random() <= self.critChc/100) * int(self.atk * (self.critDmg-100)/100) + self.atk)

    def special(self):
        None

    def mourir(self):
        Magasin.OR += self.OR
        Audio.stopMusic()
        Audio.playSound('Lose')
        __main__.motGraph.stop()
        Menu.openMenu()

class Barbare(Personnage):
    def __init__(self, pv, atk, deff, critDmg, critChc, multOR, attributs, mana):
        Personnage.__init__(self, pv, atk, deff, critDmg, critChc, multOR, attributs, mana)
        self.type = 'Barbare'
    def majCarac(self, pv, atk, deff, critDmg, critChc, multOR, mana):
        """Met à jour les caractéristiques du personnage"""
        self.pv = int(pv*1.5+.5)
        self.pvMax = int(pv*1.5+.5)
        self.atk = int(atk+.5)
        self.deff = int(deff+.5)
        self.critDmg = int(critDmg+.5)
        self.critChc = int(critChc+.5)
        self.multOR = multOR
    def special(self):
        None

class Magicien(Personnage):
    def __init__(self, pv, atk, deff, critDmg, critChc, multOR, attributs, mana):
        Personnage.__init__(self, pv, atk, deff, critDmg, critChc, multOR, attributs, mana)
        self.type = 'Magicien'
        self.mana = mana
        self.manaMax = mana
    def majCarac(self, pv, atk, deff, critDmg, critChc, multOR, mana):
        """Met à jour les caractéristiques du personnage"""
        self.pv = int(pv*0.8+0.5)
        self.pvMax = int(pv*0.8+.5)
        self.atk = int(atk*0.8+.5)
        self.deff = int(deff+.5)
        self.critDmg = int(critDmg+.5)
        self.critChc = int(critChc+.5)
        self.multOR = multOR
        self.mana = mana
        self.manaMax = mana
    def gagnerMana(self, valeur):
        if self.mana+valeur > self.manaMax : self.mana = self.manaMax
        else : self.mana += valeur
        __main__.motGraph.jauges[1].majJauge(self.mana, self.manaMax)
    def perdreMana(self, valeur):
        if self.mana-valeur < 0 : self.mana = 0
        else : self.mana -= valeur
        __main__.motGraph.jauges[1].majJauge(self.mana, self.manaMax)
    def special(self):
        if self.mana >= 8:
            if random.random() <= self.critChc/100 : degats = int(self.atk * self.critDmg/100)
            else : degats = self.atk
            coord = Fonctions.autour(self.dir, self.pos[0], self.pos[1], 12, 6)
            if lancerProjectile(0, [coord[0], coord[1]], self.dir, degats, True, 'FireBall') : self.perdreMana(8)

class Archer(Personnage):
    def __init__(self, pv, atk, deff, critDmg, critChc, multOR, attributs, mana):
        Personnage.__init__(self, pv, atk, deff, critDmg+10, critChc+10, multOR, attributs, mana)
        self.type = 'Archer'
    def majCarac(self, pv, atk, deff, critDmg, critChc, multOR, mana):
        """Met à jour les caractéristiques du personnage"""
        self.pv = int(pv*0.9+0.5)
        self.pvMax = int(pv*0.9+.5)
        self.atk = int(atk+.5)
        self.deff = int(deff+.5)
        self.critDmg = int(critDmg+10+0.5)
        self.critChc = int(critChc+10+0.5)
        self.multOR = multOR
    def special(self):
        if random.random() <= self.critChc/100 : degats = int(self.atk * self.critDmg/100)
        else : degats = self.atk
        coord = Fonctions.autour(self.dir, self.pos[0], self.pos[1], 12, 6)
        if coord[2] : lancerProjectile(1, [coord[0], coord[1]], self.dir, degats, False, 'Arrow')

class Ninja(Personnage):
    def __init__(self, pv, atk, deff, critDmg, critChc, multOR, attributs, mana):
        Personnage.__init__(self, pv, atk, deff, 100, 0, multOR, attributs, mana)
        self.type = 'Ninja'
    def majCarac(self, pv, atk, deff, critDmg, critChc, multOR, mana):
        """Met à jour les caractéristiques du personnage"""
        self.pv = int(pv*0.9+0.5)
        self.pvMax = int(pv*0.9+.5)
        self.atk = int(atk*1.7+.5)
        self.deff = int(deff+.5)
        self.critDmg = 100
        self.critChc = 0
        self.multOR = multOR
    def special(self):
        None

#--------Définition des fonctions------#

def chargerPerso(num):
    """Charge le personnage avec le numéro de la sauvegarde"""
    None

#-----------Boucle principale----------#

if __name__ == '__main__':
    p = Personnage(100, 10, 10, 10, 10, 1, {})
    print(type(p))
