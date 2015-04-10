

########################################
#------------Donjon & Python-----------#
#--------Génération de personnage------#
#--------------------------------------#
#-----------------v0.1-----------------#
#--------------------------------------#
#--------------Laloge Hugo-------------#
#--------------25/02/2014--------------#
########################################

#-----------Import des modules---------#

from random import randint

from Personnage import Personnage, Barbare, Magicien, Archer, Ninja
from Magasin import stat

#--------Définition des fonctions------#

def genererPerso():
    """Renvoie une liste de 3 personnages aléatoires (attention : supprimer les non-utilisés)"""
    listeClasse = ['Guerrier', 'Barbare', 'Magicien', 'Archer', 'Ninja']
    listePerso = []
    for i in range(3):
        classe = listeClasse[randint(0, len(listeClasse)-1)]
        if classe == 'Guerrier':
            listePerso.append(Personnage(stat['pv'], stat['atk'], stat['deff'], stat['critDmg'], stat['critChc'], stat['multOR'], {}, 0))
        elif classe == 'Barbare':
            listePerso.append(Barbare(stat['pv'], stat['atk'], stat['deff'], stat['critDmg'], stat['critChc'], stat['multOR'], {}, 0))
        elif classe == 'Magicien':
            listePerso.append(Magicien(stat['pv'], stat['atk'], stat['deff'], stat['critDmg'], stat['critChc'], stat['multOR'], {}, stat['mana']))
        elif classe == 'Archer':
            listePerso.append(Archer(stat['pv'], stat['atk'], stat['deff'], stat['critDmg'], stat['critChc'], stat['multOR'], {}, 0))
        elif classe == 'Ninja':
            listePerso.append(Ninja(stat['pv'], stat['atk'], stat['deff'], stat['critDmg'], stat['critChc'], stat['multOR'], {}, 0))
    return listePerso

#--------Définition des variables------#



#-----------Boucle principale----------#
