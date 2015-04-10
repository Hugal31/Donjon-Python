#!/usr/bin/env python3.4

########################################
#------------Donjon & Python-----------#
#-------------Menu principal-----------#
#--------------------------------------#
#-----------------v0.9-----------------#
#--------------------------------------#
#---------------30/03/2014-------------#
########################################

#-----------Import des modules---------#

from tkinter import Tk, Button, LabelFrame, Label

import __main__
import Magasin
import Audio
import GenerationPersonnage
import Sauvegarde
from Debug import debug
from MoteurGraphique import MoteurGraphique
#from GenerationPersonnage import genererPerso


#---------Définition des classes-------#

class Menu(Tk):
    def __init__(self):
        global FMagasin
        Tk.__init__(self)
        self.title('Donjon & Python')
        self.magasin = Magasin.Magasin(self)
        self.magasin.grid(row=0, column=0)
        Button(self, text='Jouer', command=self.play, height=2, width=20).grid(row=1, column=1)
        Button(self,text='Options', command=__main__.ouvrirOption, height=2, width=9).grid(row=1, column=2)
        self.framePerso = LabelFrame(self, text='Selection du personnage', width=30)
        self.framePerso.grid(row=0, column=1, columnspan=2)
        self.OR = Label(self, background='Yellow', height=2, width=70)
        self.OR.grid(row=1, column=0)
        self.majOR()
        self.remplirFramePerso()
    def run(self):
        Audio.playMusic('Rogue Legacy - Castle', -1)
        self.majPerso()
        self.mainloop()
        Sauvegarde.sauvegarder(__main__.savePath)
    def majPerso(self):
        for i in range(3):
            self.listeBox[i].maj()
    def majOR(self):
        self.OR.config(text="Pièce d'or : " + str(Magasin.OR))
    def remplirFramePerso(self):
        listePerso = GenerationPersonnage.genererPerso()
        self.listeBox = []
        for i in range(len(listePerso)):
            self.listeBox.append(BoxPerso(self.framePerso, listePerso[i], i))
            self.listeBox[i].pack()
    def play(self):
        if __main__.perso:
            Sauvegarde.sauvegarder(__main__.savePath)
            self.destroy()
            __main__.motGraph = MoteurGraphique()
            # try:    #Les thread entrainent parfois des problèmes d'inconsistance dans pygame
            __main__.motGraph.run()
            __main__.motGraph = None
            # except Exception as e :
                # debug(type(e), e)

class BoxPerso(LabelFrame):
    def __init__(self, boss, personnage, numero):
        LabelFrame.__init__(self, boss, text=personnage.type)
        self.pv = Label(self)
        self.pv.pack()
        self.atk = Label(self)
        self.atk.pack()
        self.deff = Label(self)
        self.deff.pack()
        self.critChc = Label(self)
        self.critChc.pack()
        Button(self, text='Choisir', command=self.choisir).pack()
        self.personnage = personnage
        self.maj()
    def maj(self):
        statObjet = {}
        statObjet['pv'] = 0
        statObjet['dmg'] = 0
        statObjet['deff'] = 0
        statObjet['critDmg'] = 0
        statObjet['critChc'] = 0
        statObjet['multOr'] = 0
        statObjet['mana'] = 0
        if __main__.menu :
            for typ in __main__.menu.magasin.listComboBox:
                if typ.get() != '':
                    for stat in typ.listObjets[typ.get()].stat: #On récupère les stats des objets sélectionnés
                        statObjet[stat] += typ.listObjets[typ.get()].stat[stat]
        self.personnage.majCarac(Magasin.stat['pv'] + statObjet['pv'],
                                 Magasin.stat['atk'] + statObjet['dmg'],
                                 Magasin.stat['deff'] + statObjet['deff'],
                                 Magasin.stat['critDmg'] + statObjet['critDmg'],
                                 Magasin.stat['critChc'] + statObjet['critChc'],
                                 Magasin.stat['multOR'] + statObjet['multOr'],
                                 Magasin.stat['mana'] + statObjet['mana'])
        self.pv.config(text='Pv : ' + str(self.personnage.pv), width=30)
        self.atk.config(text='Attaque : ' + str(self.personnage.atk))
        self.deff.config(text='Armure : ' + str(self.personnage.deff))
        self.critChc.config(text='Chance de critique : ' + str(self.personnage.critChc))
    def choisir(self):
        __main__.perso = self.personnage

#--------Définition des fonctions------#

def openMenu():
    __main__.perso = None   #On supprime le personnage
    __main__.menu = None    #On reset le menu
    __main__.menu = Menu()
    __main__.menu.run()

#-----------Boucle principale----------#

if __name__ == '__main__':
    openMenu()
