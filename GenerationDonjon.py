

########################################
#------------Donjon & Python-----------#
#---------Génération procédurale-------#
#--------------------------------------#
#-----------------v1.0-----------------#
#--------------------------------------#
#--------------Laloge Hugo-------------#
#--------------24/02/2014--------------#
########################################

#-----------Import des modules---------#

from random import random, randint
from os import listdir

from Coffre import *
from Fonctions import creerTableau, autour
from Monstres import placerMonstre
from Debug import debug, debugMode

#---------Définition des classes-------#

class Etage:
    """Un étage du donjon, contenant 30 à 50 salles"""
    def __init__(self, etage):
        debug('Etage'+ str(etage) + '...')
        self.etage = etage      #Numéro de l'étage
        self.grille = creerTableau(10, 10, False)
        self.generer()
        self.creerPortes()
        debug('Etage ' + str(self.etage) +' terminé')
    def generer(self):
        global nombrePaterne
        self.grille[5][5] = Salle(0, self.etage) #[5][5] représente l'entrée de l'étage
        nombreSalle = randint(30, 50)
        salleBoss = True                    #Il reste une salle du boss à placer
        for n in range(nombreSalle):
        #--Séléction de la salle à générer--#
            while 1:
                x = randint(0, 9)           #Position du "curseur" sur l'étage
                y = randint(0, 9)
                if self.grille[y][x] == False:
                    contact = False         #Boolean qui vérifie que la salle possède une voisine
                    for d in range(3):
                        coord = autour(d, x, y)
                        if self.grille[coord[1]][coord[0]] != False and coord[2] : contact=True
                    if contact : break
        #--------Création de la salle-------#
            if salleBoss and random() < n/nombreSalle:  #Chance d'avoir la salle du boss (a baisser ?)
                    self.grille[y][x] = SalleBoss(self.etage)
                    salleBoss = False
                    self.posBoss = (x, y)
            else:
                self.grille[y][x] = Salle(randint(1, nombrePaterne), self.etage)   #Remplacer 20 par salle max
    def creerPortes(self):
        """Actualise les booleens de portes de chaque salle"""
        for y in range(10):
            for x in range(10):
                if self.grille[y][x]:
                    for dir in range(4):
                        coord = autour(dir, x, y)
                        if (coord[2]) and self.grille[coord[1]][coord[0]]:
                            self.grille[y][x].porte[dir] = True

class Salle:
    """Une salle basique"""
    def __init__(self, num, etage):
        #Num représente le numéro du paterne
        self.etage = etage
        self.grille = creerTableau(7, 13, 0)    #Tableau des "Obstacles"
        self.entites = [] #Liste des entités (monstres, pièges, ...)
        self.porte = [False, False, False, False]
        self.decouvert = False
        if self.__class__.__name__ == 'SalleBoss':
            fichier = open('Salles/SallesBoss/'+str(self.etage)+'.txt', mode='r', encoding='Utf-8')
        else:
            fichier = open('Salles/'+str(num)+'.txt', mode='r', encoding='Utf-8')
        self.creer(fichier)
        fichier.close()

    def creer(self, fichier):
        text = fichier.readlines()
        for y in range(7):
            for x in range(13):
                if int(text[y][x]) < 3: self.grille[y][x] = int(text[y][x])
                elif int(text[y][x]) == 3:
                    if placerCoffre():
                        self.grille[y][x] = 3
                elif int(text[y][x]) == 4 or int(text[y][x]) == 5:
                    monstre = placerMonstre(self.etage, int(text[y][x])-4, [x,y], self)
                    if monstre:
                        self.entites.append(monstre)

class SalleBoss(Salle):
    """Une salle de boss"""
    def __init__(self, etage):
        Salle.__init__(self, -1, etage)
        boss = placerMonstre(self.etage, 2, [5,5], self, 1, 0, True)
        self.entites.append(boss)

#--------Définition des fonctions------#

def genererDonjon(etageMax):
    """Demande le nombre d'étage maximum. Renvoie une liste d'étage"""
    global nombrePaterne
    nombrePaterne = len(listdir('Salles'))-2   #On enlève le dossier SallesBoss et "0.txt"
    debug('Nombre de paterne : ' + str(nombrePaterne))
    listeEtage = []
    for i in range(etageMax):
        listeEtage.append(Etage(i))
    debug('Génération Terminé')
    return listeEtage

#--------Définition des variables------#

nombrePaterne = 0

#-----------Boucle principale----------#

if __name__ == '__main__':      #Pour tester
    listeEtage = genererDonjon(5)
    if listeEtage[1].grille[3][4]:
        print('Contenu en 1,1 de la salle x=4, y=3 du deuxième etage :', listeEtage[1].grille[3][4].grille[1][1])

#A faire :
#Chance exponnetielle/logarithmique de la salle du boss (le plus loin possible)
