#!/usr/bin/env python3.4

########################################
#------------Donjon & Python-----------#
#---------Fonctions généralistes-------#
#--------------------------------------#
#-----------------v1.0-----------------#
#--------------------------------------#
#--------------Laloge Hugo-------------#
#--------------01/03/2014--------------#
########################################

""" Fonctions générales, utiles dans plusieurs parties du programme """

#--------Définition des fonctions------#

def creerTableau(hauteur, largeur, remplir=0):
    tableau = []
    for x in range(hauteur):
        ligne = []
        for y in range(largeur):
            ligne.append(remplir)
        tableau.append(ligne)
    return tableau

def autour(direc, x, y, xMax=9, yMax=9, pas=1):
    """Renvoie des coordonées d'une case autour de celle de départ
Si case en dehors des limites, ne change pas les coordonées et renvoie un False dans la case 2"""
    boolean = True
    if direc == 0 and y > 0:        #Haut
        y -= pas
    elif direc == 1 and x < xMax:   #Droite         0
        x += pas                                  #3 1
    elif direc == 2 and y < yMax:   #Bas            2
        y += pas
    elif direc == 3 and x > 0:      #Gauche
        x -= pas
    else : boolean = False
    return (x, y, boolean)   #Tuple : à gérer comme un tableau, mais pas modifiable

def centrer(fenetre, height, width):
    fenetre.geometry("%dx%d+%d+%d" % (fenetre.winfo_screenwidth()*width/1600, fenetre.winfo_screenheight()*height/900, (fenetre.winfo_screenwidth()-width)/2, (fenetre.winfo_screenheight()-height)/2))

#-----------Boucle principale----------#

if __name__ == '__main__':
    grille = creerTableau(7, 13, 0)
    for y in range(7):
        print(grille[y])
    print('largeur = ', len(grille[0]))
    print('hauteur = ', len(grille))
    print('Contenu de la case 6, 12 :', grille[6][12])
    print('Faire tableau[y][x] pour accéder à la variable')

    print('Case en dessous de (x=5, y=4) :', autour(2, 5, 4))
