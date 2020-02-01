import os
import sys
import pygame
from pygame.locals import *
from Monopoly import *

selectCaseBas = pygame.image.load("PlateauMonopoly/Cases8bit/select2.png")
selectCaseCote = pygame.transform.rotate(selectCaseBas, 90)
selectCaseCoin = pygame.image.load("PlateauMonopoly/Cases8bit/select3.png")
selectHypo = pygame.image.load("PlateauMonopoly/CartesHypo8bit/Sélection.png")
imgBanniere = pygame.image.load("PlateauMonopoly/Fonds/bannière22.png")
imgBanniere2 = pygame.image.load("PlateauMonopoly/Fonds/bannière3.png")
imgPlateau = pygame.image.load("PlateauMonopoly/Fonds/PlateauMonopoly22.png")
imgBackground = pygame.image.load("PlateauMonopoly/Fonds/background.jpg")
imgPion1 = pygame.image.load("PlateauMonopoly/Pions/Voiture1.png")
imgPion2 = pygame.image.load("PlateauMonopoly/Pions/Bateau1.png")
imgPion3 = pygame.image.load("PlateauMonopoly/Pions/Chien1.png")
imgPion4 = pygame.image.load("PlateauMonopoly/Pions/Chapeau1.png")
imgPion5 = pygame.image.load("PlateauMonopoly/Pions/Fer1.png")
imgPion6 = pygame.image.load("PlateauMonopoly/Pions/Coudre1.png")
imgMaisonBas = pygame.image.load("PlateauMonopoly/Cases8bit/Maisons.png")
imgMaisonGauche = pygame.transform.rotate(imgMaisonBas, -90)
imgMaisonHaut = pygame.transform.rotate(imgMaisonBas, 180)
imgMaisonDroite = pygame.transform.rotate(imgMaisonBas, 90)
imgHotelBas = pygame.image.load("PlateauMonopoly/Cases8bit/Hotels.png")
imgHotelGauche = pygame.transform.rotate(imgHotelBas, -90)
imgHotelHaut = pygame.transform.rotate(imgHotelBas, 180)
imgHotelDroite = pygame.transform.rotate(imgHotelBas, 90)
imgChance = pygame.image.load("PlateauMonopoly/Fonds/Chances.jpg")
imgCommu = pygame.image.load("PlateauMonopoly/Fonds/Communauté.jpg")
imgChanceV = pygame.image.load("PlateauMonopoly/Fonds/ChanceV.jpg")
imgCommuV = pygame.image.load("PlateauMonopoly/Fonds/CommunautéV.jpg")


des = [pygame.image.load("PlateauMonopoly/Dés/Dé1.png"),pygame.image.load("PlateauMonopoly/Dés/Dé2.png"),pygame.image.load("PlateauMonopoly/Dés/Dé3.png"),pygame.image.load("PlateauMonopoly/Dés/Dé4.png"),pygame.image.load("PlateauMonopoly/Dés/Dé5.png"),pygame.image.load("PlateauMonopoly/Dés/Dé6.png")]

def stockimages(images, filepath):
    with open(filepath) as fp:
       line = fp.readline()
       while line:
           images.append(pygame.image.load(line.strip()))
           line = fp.readline()



def stockHypoCoords(hypoCoord):
    x = 22
    x1 = x
    for i in range(0,28):
        if i < 7:
            hypoCoord.append((x1, 32))
            x1 += 130
        elif i == 7:
            x1 = x
            hypoCoord.append((x1, 214))
            x1 += 130
        elif i < 14:
            hypoCoord.append((x1, 214))
            x1 += 130
        elif i == 14:
            x1 = x
            hypoCoord.append((x1, 396))
            x1 += 130
        elif i < 21:
            hypoCoord.append((x1, 396))
            x += 130
        elif i == 21:
            x1 = x
            hypoCoord.append((x1, 578))
            x1 += 130
        elif i < 28:
            hypoCoord.append((x1, 578))
            x += 130




def stockcoords(casesCoord):
    xB = 742
    yG = 765
    xH = 161
    yD = 182
    for i in range(0,40):
        if i == 0:
            casesCoord.append((815, 838))
        elif i < 10:
            casesCoord.append((xB, 838))
            xB -=73
        elif i == 10:
            casesCoord.append((40,838))
        elif i < 20:
            casesCoord.append((40, yG))
            yG-=73
        elif i == 20:
            casesCoord.append((40, 62))
        elif i < 30:
            casesCoord.append((xH, 62))
            xH+=73
        elif i == 30:
            casesCoord.append((815, 62))
        elif i < 40:
            casesCoord.append((815, yD))
            yD+=73
