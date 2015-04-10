#!/usr/bin/env python3.4

########################################
#------------Donjon & Python-----------#
#----------------Crédit----------------#
#--------------------------------------#
#-----------------v1.0-----------------#
#--------------------------------------#
#------------Le Saux Tristan-----------#
#---------------10/05/2014-------------#
########################################

#-----------Import des modules---------#

import pygame
from pygame.locals import KEYDOWN
from tkinter import *
from time import sleep

import Audio

#---------Définition des classes-------#

class Credits():
    def __init__(self):
        Audio.playMusic('Game of Thrones 8-bit',0)
        pygame.init()
        self.titreFond = pygame.font.SysFont('courier',40)
        self.ligneFond = pygame.font.SysFont('courier',28)
        self.creditFen0()
        sleep(6)
        self.creditFen1()
        sleep(6)
        self.creditFen2()
        sleep(6)
        self.creditFen3()
        sleep(6)
        self.creditFen4()
        sleep(6)
        self.creditFen5()
        sleep(6)
        self.creditFen6()
        sleep(6)
        self.creditFen7()
        sleep(6)
        self.creditFen8()
        sleep(6)
        self.creditFen9()
        while pygame.event.wait().type != pygame.locals.KEYDOWN:
            None
        pygame.display.quit()
        Audio.stopMusic()

    def creditFen0(self):
        self.credit = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.credit1 = self.titreFond.render('Inspiré de :',1,(255,255,255))
        self.credit2 = self.ligneFond.render('Rogue Legacy (Cellar Door Games)',1,(255,255,255))
        self.credit3 = self.ligneFond.render('The Binding of Isaac (Edmund McMillen et Florian Himsl)',1,(255,255,255))
        self.credit.blit(self.credit1,(400,100))
        self.credit.blit(self.credit2,(550,250))
        self.credit.blit(self.credit3,(550,350))
        pygame.display.flip()

    def creditFen1(self):
        self.credit = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.credit1 = self.titreFond.render('Avec la participation de :',1,(255,255,255))
        self.credit2 = self.ligneFond.render('FRADOT Geoffrey',1,(255,255,255))
        self.credit3 = self.ligneFond.render('LALOGE Hugo',1,(255,255,255))
        self.credit4 = self.ligneFond.render('LE SAUX Tristan',1,(255,255,255))
        self.credit5 = self.ligneFond.render('Laure',1,(255,255,255))
        self.credit.blit(self.credit1,(400,100))
        self.credit.blit(self.credit2,(550,250))
        self.credit.blit(self.credit3,(550,350))
        self.credit.blit(self.credit4,(550,450))
        self.credit.blit(self.credit5,(550,550))
        pygame.display.flip()


    def creditFen2(self):
        self.credit = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.credit1 = self.titreFond.render("Avec l'aide des professeurs d'ISN :",1,(255,255,255))
        self.credit2 = self.ligneFond.render('Christophe DYL',1,(255,255,255))
        self.credit3 = self.ligneFond.render('Christophe LEJEUNE',1,(255,255,255))
        self.credit.blit(self.credit1,(200,100))
        self.credit.blit(self.credit2,(450,250))
        self.credit.blit(self.credit3,(450,350))
        pygame.display.flip()

    def creditFen3(self):
        self.credit = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.credit1 = self.titreFond.render('Hugo LALOGE',1,(255,255,255))
        self.credit2 = self.ligneFond.render('en tant que chef de projet',1,(255,255,255))
        self.credit3 = self.ligneFond.render('et à la génération procédurale',1,(255,255,255))
        self.credit.blit(self.credit1,(400,100))
        self.credit.blit(self.credit2,(550,250))
        self.credit.blit(self.credit3,(550,350))
        pygame.display.flip()

    def creditFen4(self):
        self.credit = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.titreFond = pygame.font.SysFont('courier',40)
        self.credit1 = self.titreFond.render('Geoffrey FRADOT',1,(255,255,255))
        self.ligneFond = pygame.font.SysFont('courier',28)
        self.credit2 = self.ligneFond.render('pour le moteur graphique',1,(255,255,255))
        self.credit.blit(self.credit1,(400,100))
        self.credit.blit(self.credit2,(550,250))
        pygame.display.flip()

    def creditFen5(self):
        self.credit = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.credit1 = self.titreFond.render('Tristan LE SAUX',1,(255,255,255))
        self.credit2 = self.ligneFond.render('pour le game design',1,(255,255,255))
        self.credit3 = self.ligneFond.render('et le menu',1,(255,255,255))
        self.credit.blit(self.credit1,(400,100))
        self.credit.blit(self.credit2,(550,250))
        self.credit.blit(self.credit3,(550,350))
        pygame.display.flip()

    def creditFen6(self):
        self.credit = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.credit1 = self.titreFond.render('Laure',1,(255,255,255))
        self.credit2 = self.ligneFond.render('pour les améliorations et les objets',1,(255,255,255))
        self.credit.blit(self.credit1,(400,100))
        self.credit.blit(self.credit2,(550,250))
        pygame.display.flip()

    def creditFen7(self):
        self.credit = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.credit1 = self.titreFond.render('Avec des Musiques de Rogue Legacy (Cellar Door Games)',1,(255,255,255))
        self.credit2 = self.ligneFond.render('Gordon McGladdery (A Shell in the Pit)',1,(255,255,255))
        self.credit3 = self.ligneFond.render('Judson Cowan (Tettix)',1,(255,255,255))
        listeMusique = ['Tettix - Rogue Legacy',
                        'A Shell in the Pit - SeaSawHorse ',
                        'Tettix - The Grim Outdoors',
                        'A Shell in the Pit - Trilobyte',
                        'A Shell in the Pit - Narwhal',
                        'Tettix - Broadswide of the Broadsword']
        self.credit4 = self.ligneFond.render('Liste musiques',1,(255,255,255))
        self.credit.blit(self.credit1,(200,100))
        self.credit.blit(self.credit2,(550,250))
        self.credit.blit(self.credit3,(550,350))
        for i in range(len(listeMusique)) :
            self.credit.blit(self.ligneFond.render(listeMusique[i],1,(255,255,255)),(550,450+i*50))
        pygame.display.flip()

    def creditFen8(self):
        self.credit = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.credit1 = self.titreFond.render('Autres musiques',1,(255,255,255))
        listeMusique = ['Darren Korb - Faith of Jevel (Bastion)',
                        'Game of Thrones 8-bit']
        self.credit4 = self.ligneFond.render('Liste musiques',1,(255,255,255))
        self.credit.blit(self.credit1,(200,100))
        for i in range(len(listeMusique)) :
            self.credit.blit(self.ligneFond.render(listeMusique[i],1,(255,255,255)),(550,250+i*50))
        pygame.display.flip()

    def creditFen9(self):
        self.credit = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.credit1 = self.titreFond.render('Nous remercions tout ce qui nous ont aidé,',1,(255,255,255))
        self.credit2 = self.ligneFond.render('Tout ce qui nous ont donné une critique positive,',1,(255,255,255))
        self.credit3 = self.ligneFond.render("Et aussi ceux qui ont participé à l'élaboration de ce",1,(255,255,255))
        self.credit4 = self.ligneFond.render("projet et qui ont permis qu'il atteigne son terme",1,(255,255,255))
        self.credit5 = self.ligneFond.render("Appuyez sur une touche pour quitter",1,(240,240,240))
        self.credit.blit(self.credit1,(200,100))
        self.credit.blit(self.credit2,(200,250))
        self.credit.blit(self.credit3,(200,350))
        self.credit.blit(self.credit4,(200,450))
        self.credit.blit(self.credit5,(200,800))
        pygame.display.flip()

if __name__ == '__main__' : credit = Credits()
