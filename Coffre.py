#!/usr/bin/env python3.4

########################################
#------------Donjon & Python-----------#
#----------------Coffres---------------#
#--------------------------------------#
#-----------------v1.0-----------------#
#--------------------------------------#
#---------------11/01/2014-------------#
########################################

#-----------Import des modules---------#

from random import randint, random

import __main__

#--------Définition des fonctions------#

def placerCoffre(prob=0.5):
    if random() <= prob : return True
    else: return False

def gagnerOR(etage, montant=-1):
    if montant == -1:
        return randint(10, 100) * 2**etage * (__main__.numPartie+1)
