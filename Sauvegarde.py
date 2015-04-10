#!/usr/bin/env python3.4

########################################
#------------Donjon & Python-----------#
#--------------Sauvegarde--------------#
#--------------------------------------#
#-----------------v1.0-----------------#
#--------------------------------------#
#--------------Laloge Hugo-------------#
#---------------10/04/2014-------------#
########################################

#-----------Import des modules---------#

import __main__
import Magasin

#--------Définition des fonctions------#

#---Partie chargement---#
def charger(savePath):
    fichier = open(savePath, mode='r')
    text = ''.join(fichier.readlines())
    fichier.close()
    save = decrypter(text)
    dico = separer(save)
    Magasin.OR = int(dico['OR'])
    __main__.numPartie = int(dico['numPartie'])
    for i in Magasin.amel:
        Magasin.amel[i] = int(dico[i])
    Magasin.maj()

def decrypter(text):
    code = '0101010'
    decrypte = ''
    for i in range(0, len(text), 7):
        char = ''
        for j in range(7):
            char += str(int(text[i+j]) ^ int(code[j]))
        decrypte += chr(int(char, 2))
    return decrypte

def separer(text):
    """Transforme un text en dictionnaire"""
    text = text.split('\n')
    dico = {}
    for i in range(len(text)-1):    #-1 car la dèrnière ligne est "\n"
        ligne = text[i].split('=')
        dico[ligne[0]] = ligne[1]
    return dico

#---Partie sauvegarde--#
def sauvegarder(savePath):
    text = ''
    text += ('numPartie=' + str(__main__.numPartie) + '\n')
    for i in Magasin.amel:
        text += (i + '=' + str(Magasin.amel[i]) + '\n')
    text += ('OR=' + str(Magasin.OR) + '\n')
    #Objets
    text = crypter(text)
    fichier = open(savePath, mode='w')
    fichier.write(text)
    fichier.close()

def crypter(text):
    """Crypte un text avec une clef"""
    code = '0101010'   #La clef est 42
    crypte = ''     #Texte final
    for i in range(len(text)):
        char = convertir(text[i])
        for j in range(7):
            crypte += str(int(char[j]) ^ int(code[j]))
    return crypte

def convertir(char):
    """Renvoie le code binaire d'un caractère à 7 chiffres"""
    chiffre = str(bin(ord(char)))   #On converti en str pour pouvoir controler la longueur
    binaire = ''
    for i in range(9 - len(chiffre)):
        binaire += '0'
    binaire += chiffre[2:]      #On ne compte pas le "0b" de chiffre
    return binaire
#-----------Boucle principale----------#

if __name__ == '__main__':
    numPartie = 0
    #charger('Saves\\Player1.txt')
    sauvegarder('Saves\\Player1.txt')
