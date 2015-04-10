#!/usr/bin/env python3.4

########################################
#------------Donjon & Python-----------#
#----------------Magasin---------------#
#--------------------------------------#
#-----------------v0.2-----------------#
#--------------------------------------#
#-----------------Laure----------------#
#---------------04/04/2014-------------#
########################################

#-----------Import des modules---------#

from tkinter import Tk, LabelFrame, Button, Label, PhotoImage, LEFT, RIGHT, X
from tkinter.ttk import Combobox
from os import listdir

import __main__

#---------Définition des classes-------#

#listeStat = [[nom, nomAmel, max, prix par niveau, icone]]

class Magasin(LabelFrame):
    def __init__(self, boss):
        #Magasin d'améliorations (cadre)
        LabelFrame.__init__(self, boss, text='Magasin')
        frameAmel = LabelFrame(self, text='Amelioration')
        frameAmel.pack(side='left')

        #Cadre objets
        frameObjets = LabelFrame(self, text='Objets')
        frameObjets.pack(side='right')

        #Statistiques possibles pour les améliorations (contenu)
        #listeStat = [[nom, nomAmel, max, prix par niveau, icone]]
        listeStat = [['Points de vie', 'pv', 50, 75, 5, 'pv'],
                     ['Dégats', 'atk', 75, 75, 5, 'atk'],
                     ['Mana', 'mana', 50, 50, 5, 'mana'],
                     ['Armure (%)', 'deff', 25, 15, 1, 'deff'],
                     ['Dégats critiques (%)', 'critDmg', 20, 50, 5, 'critDmg'],
                     ['Chance de critique (%)', 'critChc', 10, 40, 5, 'critChc'],
                     ["Multiplicateur d'or (%)", 'multOR', 20, 100, 10, 'multOR']]
        chargerImages()
        for i in range(len(listeStat)):
            Amel(frameAmel, listeStat[i][0], listeStat[i][1], listeStat[i][2], listeStat[i][3], listeStat[i][4], listeStat[i][5]).pack(fill=X)

        #Magasin d'objets (contenu)
        self.listComboBox = []
        for typ in range(len(listdir('Objets'))):
            Label(frameObjets, text=listdir('Objets')[typ]).pack()
            self.listComboBox.append(ComboboxObjet(frameObjets, listdir('Objets')[typ]))
            self.listComboBox[typ].pack()

class Amel(LabelFrame):
    def __init__(self, boss, nom, amelioration, maximum, prix, up, logo):
        """
        amelioration (str) : Nom de l'amélioration du bouton
        maximum (int) : Maximum de fois que l'on peut augmenter l'amélioration
        prix (int) : Prix de l'amélioration par niveau
        up (int) : Montant de point apporté par l'amélioration
        """
        global imagesMag
        self.amel = amelioration
        self.max = maximum
        self.prix = prix
        self.up = up
        LabelFrame.__init__(self,  boss)
        Label(self, image=imagesMag[logo]).pack(side=LEFT)
        Label(self, text=nom, width=18).pack(side=LEFT)
        self.button = Button(self, command=self.acheter, width = 6)
        self.level = Label(self, width=5)
        self.total = Label(self, width=11)
        self.total.pack(side=RIGHT)
        self.level.pack(side=RIGHT)
        self.button.pack(side=RIGHT)
        self.maj()
    def maj(self):
        global amel, stat
        self.button.config(text=(str((amel[self.amel]+1)*self.prix) + ' PO'))
        self.level.config(text=str(amel[self.amel]) + '/' + str(self.max))
        self.total.config(text='Total : ' + str(stat[self.amel]))
    def acheter(self):
        global stat, OR, amel
        if ((OR >= (amel[self.amel]+1)*self.prix) and (amel[self.amel] < self.max)):
            OR -= (amel[self.amel]+1)*self.prix   #A changer
            stat[self.amel] += self.up
            amel[self.amel] += 1
            self.maj()
            __main__.menu.majPerso()
            __main__.menu.majOR()

class ComboboxObjet(Combobox):
    def __init__(self, boss, repertoire):
        contenu = listdir('Objets/' + repertoire)
        self.listObjets = {}
        listStrObjets = []
        for nom in contenu:
            self.listObjets[nom[:-4]] = Objet(repertoire, nom)  #Le [:-4] permet de supprimer le ".txt"
            listStrObjets.append(nom[:-4])
        Combobox.__init__(self, boss, values = listStrObjets, state='readonly')
        # self.current(0)
        #BIND changement

class Objet:
    def __init__(self, typ, nom):
        fichier = open('Objets/' + typ + '/' + nom)
        self.stat = {}
        for ligne in fichier.readlines():
            self.stat[ligne.split('=')[0]] = int(ligne.split('=')[1][:-1])

def chargerImages():
    global imagesMag
    for i in ['pv', 'atk', 'mana', 'deff', 'multOR', 'critDmg', 'critChc']:
        try:
            imagesMag[i] = PhotoImage(file='TexturePack/'+__main__.texturePack+'/Images/'+i+'.gif')
        except:
            imagesMag[i] = PhotoImage(file='TexturePack/Default/Images/'+i+'.gif')

#--------Définition des variables------#

imagesMag = {}

amel = {}
amel['pv'] = 0
amel['atk'] = 0
amel['mana'] = 0
amel['deff'] = 0
amel['critDmg'] = 0
amel['critChc'] = 0
amel['multOR'] = 0
stat = {}
OR = 0
#OR = 100000000

def maj():
    stat['pv'] = 80 + amel['pv'] * 5
    stat['atk'] = 10 + amel['atk'] * 5
    stat['mana'] = 100 + amel['mana'] * 10
    stat['deff'] = 0 + amel['deff']
    stat['critDmg'] = 150 + amel['critDmg'] * 5
    stat['critChc'] = 0 + amel['critChc'] * 5
    stat['multOR'] = 100 + amel['multOR'] * 10    #En %


#-----------Boucle principale----------#

maj()

if __name__ == '__main__':
    root = Tk()
    magasin = Magasin(root)
    magasin.pack()
    root.mainloop()
