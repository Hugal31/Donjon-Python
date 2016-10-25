#!/usr/bin/env python3

########################################
#------------Donjon & Python-----------#
#--------------------------------------#
#-----------------v1.0-----------------#
#--------------------------------------#
#---------------03/03/2014-------------#
########################################

#---Définition des variables globales--#

#-------Options-------#

texturePack = 'Default'
savePath = None

#-Instances de classe-#

menu = None
motGraph = None
perso = None

#-----Statistiques----#

nombreEtage = 5
numPartie = 0

#-----------Import des modules---------#

import pygame
from pygame.locals import *
from tkinter import *
from tkinter.ttk import Combobox
from os import listdir

import Menu
import Audio
import Sauvegarde
import Fonctions
import Credit
from Debug import debug, step, switchDebug
from Options import FenOptions

#---------Définition des classes-------#

class FenSave:
    """Fenetre de sélection des sauvegardes"""
    def __init__(self, charger):
        self.root = Tk()
        Fonctions.centrer(self.root, 80, 72)
        self.charger = charger  #Boolean qui indique si la fenètres est en mode charger ou non
        self.box = Listbox(self.root, height=3)
        self.button = Button(self.root, text='Sélectionner', command=self.selectionner)
        for i in range(3):
            self.box.insert(END, 'Sauvegarde ' + str(i+1))
        self.box.pack()
        self.button.pack()
        self.root.mainloop()
    def selectionner(self):
        global savePath, root
        if True:
            savePath = 'Saves/Player' + str(int(self.box.curselection()[0]) + 1) + '.txt'
            self.root.destroy()
            if self.charger : Sauvegarde.charger(savePath)
            else :
                self.warner = Tk()
                Label(self.warner, text='Êtes vous sûr ? La sauvegarde sera ecrasée !', bg='Red').pack()
                Button(self.warner, text='Ecraser la sauvegarde', command=self.warner.quit).pack(fill=X)
                Button(self.warner, text='Annuler', command=self.annuler).pack(fill=X)
                Fonctions.centrer(self.warner, 73, 222)
                self.warner.mainloop()
                self.warner.destroy()
            root.destroy()
            debug("Step1")
            Menu.openMenu()
        #except :
         #   debug("BUG")
    def annuler(self):
        self.warner.destroy()
        self.root.quit()
        self.warner.quit()

#--------Définition des fonctions------#

def newGame():
    FenSave(False)

def loadGame():
    FenSave(True)

def chargerConfig():
    global texturePack
    fichierConfig = open('Saves/Config.txt')
    config = fichierConfig.readlines()
    fichierConfig.close()
    Audio.volumeGlobal = int(config[0])
    Audio.volumeMusic = int(config[1])
    Audio.volumeSound = int(config[2])
    Audio.setVolumeMusic()
    texturePack = config[3]

def sauverConfig():
    global texturePack
    fichierConfig = open('Saves/Config.txt', mode='w')
    fichierConfig.write(str(Audio.volumeGlobal) + '\n'
                        + str(Audio.volumeMusic) + '\n'
                        + str(Audio.volumeSound) + '\n'
                        + texturePack)
    fichierConfig.close()

def ouvrirOption():
    try:
        fenOption.run()
    except:
        fenOption = FenOptions()

#-----------Boucle principale----------#

# try:
chargerConfig()
# except Exception as e:
    # debug('Config non trouvé')
    # debug(str(type(e)) + ' ' + str(e))

Audio.playMusic('Rogue Legacy - Main Theme', -1)

root = Tk()
Fonctions.centrer(root, 400, 289)
imageFond = PhotoImage(file='Images/Logo.gif')
fond = Label(root, image=imageFond)
fond.pack(fill='both', expand='yes')
root.title('Donjon & Python')
Button(fond, text='Nouvelle Partie', command = newGame).place(relx=.5, rely=.3, anchor=CENTER)
Button(fond, text='Charger une partie', command = loadGame).place(relx=.5, rely=.4, anchor=CENTER)
Button(fond, text='Options', command = ouvrirOption).place(relx=.5, rely=.5, anchor=CENTER)
Button(fond, text='Crédits', command = Credit.Credits).place(relx=.5, rely=.6, anchor=CENTER)
Button(fond, text='Quitter', command = root.destroy).place(relx=.5, rely=.7, anchor=CENTER)
root.mainloop()
sauverConfig()

step('FINAL')
Audio.stopMusic()
