#!/usr/bin/env python3.4

########################################
#------------Donjon & Python-----------#
#-----------------Debug----------------#
#--------------------------------------#
#-----------------v1.0-----------------#
#--------------------------------------#
#---------------03/03/2014-------------#
########################################

""" Options de debogage """

debugMode = False    #Mode par defaut

def debug(text ='Debug'):
    """Effectue un print"""
    global debugMode
    if debugMode : print(str(text))

def step(num = ''):
    """Demande confirmation avant de continuer l'execution. Faire attention avec les Threads"""
    global debugMode
    if debugMode : input('STEP ' + str(num))

def switchDebug(event):
    """Passe du mode debug au mode normal et inversement"""
    global debugMode
    debugMode = not debugMode

def afficherCarte(etage):
    """Affiche la carte de l'étage en cour"""
    global debugMode
    if debugMode:
        print('----------')
        grille = []
        for y in range(10):
            ligne = []
            for x in range(10):
                if etage.grille[y][x]:
                    if etage.grille[y][x].__class__.__name__ == 'SalleBoss' : ligne.append('B')
                    elif x == 5 and y == 5 : ligne.append('D')
                    else : ligne.append('1')
                else: ligne.append('0')
            grille.append(ligne)
        for y in range(10):
            print(''.join(grille[y]))
