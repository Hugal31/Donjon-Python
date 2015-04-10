#!/usr/bin/env python3.4

########################################
#------------Donjon & Python-----------#
#----------------Options---------------#
#--------------------------------------#
#-----------------v1.0-----------------#
#--------------------------------------#
#---------------28/07/2014-------------#
########################################

#-----------Import des modules---------#

from tkinter import *
from tkinter.ttk import Combobox
from os import listdir

import Audio
from Debug import switchDebug
from __main__ import texturePack

#---------Définition des classes-------#

class FenOptions:
    def __init__(self):
        self.root=Tk()
        self.root.title('Donjon & Python-Option')
        self.root.bind('<F12>', switchDebug)
        #--------Barres de volume------#
        self.varVolumeGlobal = IntVar()
        self.varVolumeGlobal.set(Audio.volumeGlobal)
        self.varVolumeMusique = IntVar()
        self.varVolumeMusique.set(Audio.volumeMusic)
        self.varVolumeSons = IntVar()
        self.varVolumeSons.set(Audio.volumeSound)
        self.scaleVolumeGlobal = Scale(self.root,from_=0,
                                        to=100,resolution=1,
                                        orient=HORIZONTAL,
                                        length=300,width=20,
                                        label="Volume principal",
                                        tickinterval=20,
                                        variable=self.varVolumeGlobal,
                                        command = self.setVolumeGlobal)
        self.scaleVolumeMusique = Scale(self.root,from_=0,
                                        to=100,resolution=1,orient=HORIZONTAL,
                                        length=300,
                                        width=20,
                                        label="Volume Musique",
                                        tickinterval=20,
                                        variable=self.varVolumeMusique,
                                        command = self.setVolumeMusique)
        self.scaleVolumeSons = Scale(self.root,
                                        from_=0,
                                        to=100,
                                        resolution=1,
                                        orient=HORIZONTAL,
                                        length=300,
                                        width=20,
                                        label="Volume Bruitages",
                                        tickinterval=20,
                                        variable=self.varVolumeSons,
                                        command = self.setVolumeSons)
        self.scaleVolumeGlobal.set(Audio.volumeGlobal)
        self.scaleVolumeMusique.set(Audio.volumeMusic)
        self.scaleVolumeSons.set(Audio.volumeSound)
        self.scaleVolumeGlobal.pack(padx=10,pady=10)
        self.scaleVolumeMusique.pack(padx=10,pady=10)
        self.scaleVolumeSons.pack(padx=10,pady=10)
        #-----Sélection des textures----#
        Label(self.root, text='Texture Pack :').pack()
        self.box = Combobox(self.root, values=listdir('TexturePack'), state='readonly')
        self.box.bind('<<ComboboxSelected>>', self.selectionnerPack)
        self.box.current(0)
        self.box.pack()
    def selectionnerPack(self, event) :
        global texturePack
        texturePack = self.box.get()
    def run(self):
        self.root.mainloop()
        Audio.volumeGlobal = volume
        Audio.setVolumeMusic()
    def setVolumeGlobal(self, volume):
        Audio.volumeGlobal = volume
        Audio.setVolumeMusic()
    def setVolumeMusique(self, volume):
        Audio.volumeMusic = volume
        Audio.setVolumeMusic()
    def setVolumeSons(self, volume):
        Audio.volumeSound = volume
