#!/usr/bin/env python3.4

########################################
#------------Donjon & Python-----------#
#----------------Musiques--------------#
#--------------------------------------#
#-----------------v1.0-----------------#
#--------------------------------------#
#------------Le Saux Tristan-----------#
#---------------30/03/2014-------------#
########################################

#-----------Import des modules---------#

from pygame import mixer

#--------Définition des fonctions------#

def playMusic(nom, boucle=0):
    """Joue une musique un certain nombre de fois"""
    if not mixer.get_init() : mixer.init()
    mixer.music.load('Musiques/' + nom + '.ogg')
    mixer.music.play(boucle)

def stopMusic():
    """Arrête la musique"""
    if not mixer.get_init() : mixer.init()
    mixer.music.stop()

def playSound(nom):
    """Joue un son une fois"""
    global volumeGlobal, volumeSons
    if not mixer.get_init() : mixer.init()
    son = mixer.Sound('Sons/' + nom + '.ogg')
    son.set_volume(float(volumeGlobal)*float(volumeSound)/10000)
    son.play()

def setVolumeMusic():
    global volumeGlobal, volumeMusique
    if not mixer.get_init() : mixer.init()
    mixer.music.set_volume(float(volumeGlobal)*float(volumeMusic)/10000)

def stageMusic(etage):
    if not mixer.get_init() : mixer.init()
    global listeMusiqueEtage
    playMusic(listeMusiqueEtage[etage], -1)

def bossMusic(etage):
    if not mixer.get_init() : mixer.init()
    global listeMusiqueBoss
    try :
        playMusic(listeMusiqueBoss[etage], -1)
    except : None


#--------Définition des variables------#

volumeGlobal = 100
volumeMusic = 100
volumeSound = 100

listeMusiqueEtage = ['Rogue Legacy - Forest', 'Rogue Legacy - Trilobyte', 'Darren Korb - Faith of Jevel', 'Rogue Legacy - Narwhal', 'Rogue Legacy - Dungeon']
listeMusiqueBoss = ['Rogue Legacy - Skin off My Teeth (Forest Boss)']

#-----------Boucle principale----------#

if __name__ == '__main__':
    musique = input('Entrez un titre de musique : ')
    playMusic(musique, 0)
    input('Terminer ?')
