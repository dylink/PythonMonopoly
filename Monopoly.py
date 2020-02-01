#!/usr/bin/python
import os
import sys
from tkinter import *
import socket
import select
import threading
import queue
import pygame
from pygame.locals import *
from utils import *
import random
import time

def textOutline(font, message, fontcolor, outlinecolor):
    base = font.render(message, True, fontcolor)
    outline = font.render(message, False, outlinecolor)
    img = pygame.Surface((outline.get_size()[0]+3,outline.get_size()[1]+3), 18)
    img.blit(outline, (0, 0))
    img.blit(outline, (4, 0))
    img.blit(outline, (0, 4))
    img.blit(outline, (4, 4))
    img.blit(outline, (3, 0))
    img.blit(outline, (0, 3))
    img.blit(outline, (3, 3))
    img.blit(outline, (2, 0))
    img.blit(outline, (0, 2))
    img.blit(outline, (2, 2))
    img.blit(outline, (0, 0))
    img.blit(outline, (1, 0))
    img.blit(outline, (0, 1))
    img.blit(outline, (1, 1))
    img.blit(base, (2, 2))
    img.set_colorkey(0)
    return img



class Propriete:
    def __init__(self, nom = None, proprietaire = None, constructions = None, prix = None):
        self.nom = nom
        self.proprietaire = proprietaire
        self.constructions = constructions
        self.prix = prix

class Info:

    def __init__(self):
        self.nbJoueurs = 0
        self.nomJoueur = []



class Plateau:

    def __init__(self):
        self.posJoueur = [0, 0, 0, 0, 0, 0]
        self.argentJoueur = [0, 0, 0, 0, 0, 0]
        self.propriete = [Propriete("Boulevard de Belleville", 0, 0, 60), Propriete("Rue Lecourbe", 0, 0, 60), Propriete("Rue de Vaugirard", 0, 0, 100),Propriete("Rue de Courcelles", 0, 0, 100), Propriete("Avenue de la République", 0, 0, 120), Propriete("Boulevard de la Villette", 0, 0, 140), Propriete("Avenue de Neuilly", 0, 0, 140), Propriete("Rue de Paradis", 0, 0, 160), Propriete("Avenue Mozart", 0, 0, 180), Propriete("Boulevard Saint-Michel", 0, 0, 180), Propriete("Place Pigalle", 0, 0, 200),Propriete("Avenue Matignon", 0, 0, 220),Propriete("Boulevard Malesherbe", 0, 0, 220), Propriete("Avenue Henri-Martin", 0, 0, 240), Propriete("Faubourg Saint-Honoré", 0, 0, 260), Propriete("Place de la Bourse", 0, 0, 260), Propriete("Rue La Fayette", 0, 0, 280),Propriete("Avenue de Breteuil", 0, 0, 300), Propriete("Avenue Foch", 0, 0, 300),Propriete("Boulevard des Capucines", 0, 0, 320), Propriete("Avenue des Champs-Elysées", 0, 0, 350),Propriete("Rue de la Paix", 0, 0, 400), Propriete("Gare MontParnasse", 0, 0, 200), Propriete("Gare de Lyon", 0, 0, 200), Propriete("Gare du Nord", 0, 0, 200), Propriete("Gare Saint-Lazarre", 0, 0, 200),Propriete("Compagnie de distribution d'électricité", 0, 0, 140), Propriete("Compagnie de distribution des eaux", 0, 0, 150)]
        self.de1 = 0
        self.de2 = 0
        self.tour = 0
        self.tourj = 0



class GUI:

    def __init__(self, client, q):
        stockimages(images, 'images.txt')
        stockimages(images2, 'images2.txt')
        stockimages(cartesHypo, 'images3.txt')
        stockcoords(casesCoord)
        stockHypoCoords(hypoCoord)
        self.info = Info()
        self.plateau = Plateau()
        self.client = client
        self.q = q
        self.lock = threading.RLock()
        self.continuer = True
        self.runGUI = False
        while not self.runGUI:
            if self.client.begin:
                self.runGUI = True
        self.getinfo()
        self.index = self.info.nomJoueur.index(self.client.pseudo)
        self._t = threading.Thread(target=self.getplt, daemon = True)
        self._t.start()
        self.run()

    def run(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        pygame.mixer.music.load('PlateauMonopoly//Sons/Monopoly.mp3')
        pygame.mixer.music.play(-1)
        self._win = pygame.display.set_mode((1600, 900))
        clock = pygame.time.Clock()
        self.background = imgBanniere
        self.banniere = imgBanniere
        self.banniere2 = imgBanniere2
        self.pion1 = imgPion1
        self.pionRect1 = self.pion1.get_rect()
        self.pion2 = imgPion2
        self.pionRect2 = self.pion2.get_rect()
        self.pion3 = imgPion3
        self.pionRect3 = self.pion3.get_rect()
        self.pion4 = imgPion4
        self.pionRect4 = self.pion4.get_rect()
        self.pion5 = imgPion5
        self.pionRect5 = self.pion5.get_rect()
        self.pion6 = imgPion6
        self.pionRect6 = self.pion6.get_rect()
        self.pions = [self.pion1, self.pionRect1], [self.pion2, self.pionRect2],[self.pion3, self.pionRect3], [self.pion4, self.pionRect4],[self.pion5, self.pionRect5],[self.pion6, self.pionRect6]
        self.selectCase = selectCaseBas
        self.caseBasRect = self.selectCase.get_rect()
        self.case = 0
        self.mesProprietes = []
        while self.continuer:
            clock.tick(30)
            with self.lock:
                self.check()
                self.affichePlateau()
        pygame.quit()

    def getPropriete(self):
        self.mesProprietes.clear()
        for i in range(0,28):
            if self.plateau.propriete[i].proprietaire == self.index+1:
                self.mesProprietes.append(self.plateau.propriete[i])


    def getProprieteIndex(self, prop):
        for j in range(0, 28):
            if prop == self.plateau.propriete[j].nom:
                return j


    def displaypos(self, i, y):
        for a in range(0,28):
            if self.plateau.propriete[a].proprietaire == i+1:
                self._win.blit(images2[a], (possCoord[a][0], possCoord[a][1]+y))

    def dispawn(self):
        for i in range(0, self.info.nbJoueurs):
            if i!= self.plateau.tourj:
                self._win.blit(self.pions[i][0], (self.pions[i][1][0]-10,self.pions[i][1][1]-10))

    def displayHypo(self):
        self.getPropriete()
        for i in range(0, len(self.mesProprietes)):
            for j in range(0, 28):
                if self.mesProprietes[i].nom == self.plateau.propriete[j].nom:
                    self._win.blit(cartesHypo[j], hypoCoord[i])
                    pygame.display.flip()


    def selectHypo(self):
        self.displayHypo()
        self.getPropriete()
        choix = 0
        title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Appuyez sur échap pour stopper la sélection.", (255,255,255), (1,1,1))
        self._win.blit(title, (950, 70))
        self._win.blit(selectHypo, hypoCoord[choix])
        pygame.display.flip()
        if len(self.mesProprietes):
            menu = True
        else:
            return -1
        with self.lock:
            while menu:
                event = pygame.event.wait()
                pygame.event.set_blocked(pygame.MOUSEMOTION)
                if event.type == QUIT:
                    self.continuer = False
                else:
                    if event.type == pygame.KEYUP:
                            if event.key == pygame.K_RIGHT:
                                if choix < len(self.mesProprietes)-1:
                                    choix += 1
                                else:
                                    pass
                            if event.key == pygame.K_LEFT:
                                if choix > 0:
                                    choix -= 1
                                else:
                                    pass
                            if event.key == pygame.K_DOWN:
                                if choix + 7 < len(self.mesProprietes):
                                    choix += 7
                                else:
                                    pass
                            if event.key == pygame.K_UP:
                                if choix - 7 >= 0:
                                    choix -= 7
                                else:
                                    pass
                            if event.key == pygame.K_RETURN:
                                return self.getProprieteIndex(self.mesProprietes[choix].nom)
                            elif event.key == pygame.K_ESCAPE:
                                return -1

                self._win.blit(title, (950, 70))
                self.displayHypo()
                self._win.blit(selectHypo, hypoCoord[choix])
                pygame.display.flip()



    def displayHouse(self):
        for i in range(0,22):
            if self.plateau.propriete[i].constructions:
                e = 0
                if i < 5:
                    for j in range(0, self.plateau.propriete[i].constructions):
                        if self.plateau.propriete[i].constructions == 5:
                            self._win.blit(imgHotelBas, (houseCoords[i][0]-37, houseCoords[i][1]-2))
                        else:
                            self._win.blit(imgMaisonBas, (houseCoords[i][0]-e, houseCoords[i][1]))
                            e += 18
                elif i < 11:
                    for j in range(0, self.plateau.propriete[i].constructions):
                        if self.plateau.propriete[i].constructions == 5:
                            self._win.blit(imgHotelGauche, (houseCoords[i][0]-6, houseCoords[i][1]-37))
                        else:
                            self._win.blit(imgMaisonGauche, (houseCoords[i][0], houseCoords[i][1]-e))
                            e += 18
                elif i < 17:
                    for j in range(0, self.plateau.propriete[i].constructions):
                        self._win.blit(imgMaisonHaut, (houseCoords[i][0]+e, houseCoords[i][1]))
                        e += 18
                elif i < 22:
                    for j in range(0, self.plateau.propriete[i].constructions):
                        self._win.blit(imgMaisonDroite, (houseCoords[i][0], houseCoords[i][1]+e))
                        e += 18


    def translate(self, pion, indexCur, x2):
        pygame.event.set_blocked(None)
        x1 = casesCoord[indexCur][0]-40
        y1 = casesCoord[indexCur][1]-50
        cur = indexCur
        next = x2
        if self.plateau.tourj == 0:
            son = pygame.mixer.Sound("PlateauMonopoly/Sons/Voiture.wav")
            son.play()
        elif self.plateau.tourj == 1:
            son = pygame.mixer.Sound("PlateauMonopoly/Sons/Bateau.wav")
            son.play()
        elif self.plateau.tourj == 0:
            son = pygame.mixer.Sound("PlateauMonopoly/Sons/Chien.wav")
            son.play()
        time.sleep(1)
        i = cur
        if cur > next:
            next = 40
        while(i <= next):
            a = casesCoord[i][0]
            b = casesCoord[i][1]
            if i <= 10:
                while x1 > a-30:
                    self._win.blit(imgPlateau, (0,0))
                    self._win.blit(des[self.plateau.de1-1], (200,370))
                    self._win.blit(des[self.plateau.de2-1], (630,370))
                    self.dispawn()
                    x1 -= 5
                    self._win.blit(pion, (x1, y1))
                    pygame.display.flip()
                    pygame.time.delay(5)
            elif i<=20:
                while y1 >= b-50:
                    self._win.blit(imgPlateau, (0,0))
                    self._win.blit(des[self.plateau.de1-1], (200,370))
                    self._win.blit(des[self.plateau.de2-1], (630,370))
                    self.dispawn()
                    y1 -= 5
                    self._win.blit(pion, (x1, y1))
                    pygame.display.flip()
                    pygame.time.delay(5)
            elif i<=30:
                while x1 <= a-30:
                    self._win.blit(imgPlateau, (0,0))
                    self._win.blit(des[self.plateau.de1-1], (200,370))
                    self._win.blit(des[self.plateau.de2-1], (630,370))
                    self.dispawn()
                    x1 += 5
                    self._win.blit(pion, (x1, y1))
                    pygame.display.flip()
                    pygame.time.delay(5)
            elif i<40:
                while y1 <= b-50:
                    self._win.blit(imgPlateau, (0,0))
                    self._win.blit(des[self.plateau.de1-1], (200,370))
                    self._win.blit(des[self.plateau.de2-1], (630,370))
                    self.dispawn()
                    y1 += 5
                    self._win.blit(pion, (x1, y1))
                    pygame.display.flip()
                    pygame.time.delay(5)
            i+=1
            if i == 40 and next == 40:
                a = casesCoord[0][0]
                b = casesCoord[0][1]
                while y1 <= b-50:
                    self._win.blit(imgPlateau, (0,0))
                    self._win.blit(des[self.plateau.de1-1], (200,370))
                    self._win.blit(des[self.plateau.de2-1], (630,370))
                    self.dispawn()
                    y1 += 5
                    self._win.blit(pion, (x1, y1))
                    pygame.display.flip()
                    pygame.time.delay(5)
                pion = pygame.transform.rotate(imgPion1, 0)
                i=0
                next = x2
        pygame.event.set_allowed(pygame.KEYUP)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.event.set_allowed(QUIT)

    def rolldice(self):
        pygame.event.set_blocked(None)
        son = pygame.mixer.Sound("PlateauMonopoly/Sons/RollDice.wav")
        son.play()
        for i in range(0,10):
            self.tourjoueursurface = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 40), 'Au tour de ' + self.info.nomJoueur[self.plateau.tourj] +' ', (255,255,255),(255,0,0))
            time.sleep(0.20)
            d = random.randint(0,5)
            dd = random.randint(0,5)
            self._win.blit(self.tourjoueursurface, (320, 190))
            self._win.blit(des[d-1], (200,370))
            self._win.blit(des[dd-1], (630,370))
            pygame.display.flip()
        self._win.blit(des[self.plateau.de1-1], (200,370))
        self._win.blit(des[self.plateau.de2-1], (630,370))
        pygame.display.flip()
        time.sleep(1)
        pygame.event.set_allowed(pygame.KEYUP)
        pygame.event.set_allowed(pygame.KEYDOWN)
        pygame.event.set_allowed(QUIT)

    def menu_boutons(self, indexCase, str1, str2, title):
        menu=True
        selected="Acheter"

        achat=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), str1, (255,255,0),(255,0,0))
        finTour = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), str2, (255,255,255),(255,0,0))
        self._win.blit(images[indexCase], (300,320))
        self._win.blit(title, (160,230))
        self._win.blit(achat, (320, 280))
        self._win.blit(finTour, (480, 280))
        pygame.display.flip()
        choix = 0
        with self.lock:
            while menu:
                self._win.blit(images[indexCase], (300,320) )
                self._win.blit(title, (160,230))
                self._win.blit(achat, (320, 280))
                self._win.blit(finTour, (480, 280))
                pygame.display.flip()
                event = pygame.event.wait()
                if event.type == QUIT:
                    self.continuer = False
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_LEFT:
                        if choix == 0:
                            pass
                        else:
                            choix -= 1
                    elif event.key==pygame.K_RIGHT:
                        if choix == 1:
                            pass
                        else:
                            choix += 1
                    if event.key==pygame.K_RETURN:
                        if choix == 1:
                            return 1
                        elif choix == 0:
                            return 0

                if choix == 0:
                    selected="Acheter"
                elif choix == 1:
                    selected="Fin du tour"
                if selected=="Acheter":
                    achat=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), str1, (255,255,0),(255,0,0))
                else:
                    achat=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), str1, (255,255,255),(255,0,0))
                if selected=="Fin du tour":
                    finTour=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), str2, (255,255,0),(255,0,0))
                else:
                    finTour = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), str2, (255,255,255),(255,0,0))


    def finDuTour(self):
        finTour=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Fin du tour", (255,255,0),(255,0,0))
        self._win.blit(finTour, (400, 280))
        pygame.display.flip()
        event = pygame.event.wait()
        if event.key==pygame.K_RETURN:
            return


    def menu_choix(self, indexCase):
        menu=True
        selected="Vendre"
        title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Que voulez-vous faire?", (255,255,255),(255,0,0))
        finTour = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Fin du tour", (255,255,255),(255,0,0))
        construire = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Construire", (255,255,255),(255,0,0))
        vendre = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Vendre", (255,255,0),(255,0,0))
        faillite= textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Faillite", (255,255,255),(255,0,0))
        self._win.blit(title, (330,230))
        self._win.blit(vendre, (300, 280))
        self._win.blit(construire, (400, 280))
        self._win.blit(finTour, (520, 280))
        self._win.blit(faillite, (400, 310))
        pygame.display.flip()
        choix = 0
        with self.lock:
            while menu:
                self._win.blit(title, (330,230))
                self._win.blit(vendre, (300, 280))
                self._win.blit(construire, (400, 280))
                self._win.blit(finTour, (520, 280))
                self._win.blit(faillite, (400, 310))
                pygame.display.flip()
                event = pygame.event.wait()
                if event.type == QUIT:
                    self.continuer = False
                    return
                if event.type==pygame.KEYUP:
                    if event.key==pygame.K_LEFT:
                        if choix == 0:
                            pass
                        else:
                            choix -= 1
                    elif event.key==pygame.K_RIGHT:
                        if choix == 3:
                            pass
                        else:
                            choix += 1
                    if event.key==pygame.K_RETURN:
                        if choix == 1:
                            return 1
                        elif choix == 0:
                            return 0
                        elif choix == 2:
                            return 2
                        elif choix == 3:
                            return 3

                if choix == 0:
                    selected="Vendre"
                elif choix == 1:
                    selected="Constuire"
                elif choix == 2:
                    selected="Fin du tour"
                elif choix == 3:
                    selected="Faillite"

                title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Que voulez-vous faire?", (255,255,255),(255,0,0))
                if selected=="Fin du tour":
                    finTour=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Fin du tour", (255,255,0),(255,0,0))
                else:
                    finTour = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Fin du tour", (255,255,255),(255,0,0))
                if selected=="Constuire":
                    construire=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Construire", (255,255,0),(255,0,0))
                else:
                    construire = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Construire", (255,255,255),(255,0,0))
                if selected=="Vendre":
                    vendre=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Vendre", (255,255,0),(255,0,0))
                else:
                    vendre = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Vendre", (255,255,255),(255,0,0))
                if selected=="Faillite":
                    faillite=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Faillite", (255,255,0),(255,0,0))
                else:
                    faillite = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Faillite", (255,255,255),(255,0,0))

    def affichePlateau(self):
        self.caseBasRect.center = casesCoord[self.case][0], casesCoord[self.case][1]
        self._win.blit(imgBackground, (900,0))
        self._win.blit(imgPlateau, (0,0))
        self._win.blit(self.selectCase, self.caseBasRect)
        self._win.blit(images[self.case], (300,320))
        self.bannieres()
        self.displayHouse()
        self.displayer()
        self._win.blit(des[self.plateau.de1-1], (200,370))
        self._win.blit(des[self.plateau.de2-1], (630,370))
        pygame.display.flip()

    def bannieres(self):
        y=-150
        for i in range(0, self.info.nbJoueurs):
            y+=150
            self.pseudoJoueursurface = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 30), self.info.nomJoueur[i], (255,255,255),(255,0,0))
            self.argentJoueursurface = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 30), str(self.plateau.argentJoueur[i]) + '€', (255,255,0),(1,1,1))
            self._win.blit(self.banniere, (900, y))
            if i == self.plateau.tourj:
                self._win.blit(self.banniere2, (900, y))
            self._win.blit(self.pseudoJoueursurface, (930, y+20))
            self._win.blit(self.argentJoueursurface, (1460, y+20))
            self.displaypos(i, y)

    def displayer(self):
        self.pions[0][1] = casesCoord[self.plateau.posJoueur[0]][0]-30, casesCoord[self.plateau.posJoueur[0]][1]-40
        self.pions[1][1] = casesCoord[self.plateau.posJoueur[1]][0]-30, casesCoord[self.plateau.posJoueur[1]][1]-39
        self.pions[2][1] = casesCoord[self.plateau.posJoueur[2]][0]-30, casesCoord[self.plateau.posJoueur[2]][1]-37
        self.pions[3][1] = casesCoord[self.plateau.posJoueur[3]][0]-30, casesCoord[self.plateau.posJoueur[3]][1]-41
        self.pions[4][1] = casesCoord[self.plateau.posJoueur[4]][0]-30, casesCoord[self.plateau.posJoueur[4]][1]-42
        self.pions[5][1] = casesCoord[self.plateau.posJoueur[5]][0]-30, casesCoord[self.plateau.posJoueur[5]][1]-36
        for i in range(0, self.info.nbJoueurs):
            self._win.blit(self.pions[i][0], (self.pions[i][1][0]-10,self.pions[i][1][1]-10))

    def check(self):
        event = pygame.event.wait()
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        if event.type == QUIT:
            self.continuer = False
        else:
            if event.type == pygame.KEYUP:
                if self.case < 10:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                        self.case += 1
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                        if self.case == 0:
                            self.case = 39
                        else:
                            self.case -=1
                elif self.case < 20:
                    if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.case+=1
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        self.case-=1
                elif self.case < 30:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_DOWN:
                        self.case -= 1
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                        self.case +=1
                elif self.case < 40:
                    if event.key == pygame.K_UP or event.key == pygame.K_LEFT:
                        self.case-=1
                    if event.key == pygame.K_DOWN or event.key == pygame.K_RIGHT:
                        if self.case == 39:
                            self.case = 0
                        else:
                            self.case+=1
        if self.case == 0 or self.case == 10 or self.case == 20 or self.case == 30:
            self.selectCase = selectCaseCoin
        elif self.case < 10 or 20 < self.case < 30:
            self.selectCase = selectCaseBas
        elif self.case < 20 or 30 < self.case < 40:
            self.selectCase = selectCaseCote

    def getinfo(self):
        cmd, arg = self.q.get()
        if cmd == 'info':
            datas = arg.split(' ', 1)[1]
            data = datas.split('/', 72)
            for i in range(0, len(data)):
                if i == 0:
                    self.info.nbJoueurs = int(data[i])
                else:
                    self.info.nomJoueur.append(data[i])

    def getplt(self):
        posCourante = []
        while self.continuer:
            for i in range(0, len(self.plateau.posJoueur)):
                posCourante.append(self.plateau.posJoueur[i])
            cmd, arg = self.q.get()
            if cmd == 'fin':
                pseudo = arg.split(" ",1)[1]
                title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), pseudo + " a fait faillite! La partie est terminée!", (255,255,255),(255,0,0))
                self._win.blit(title, (300,200))
                pygame.display.flip()
                self.client._sock.close()
                self.continuer = False
            if cmd == 'data':
                y = -150
                datas = arg.split(' ', 1)[1]
                self.getpltaux(datas)
                self.attribue()
                self.bannieres()
                self.rolldice()
                self.translate(self.pions[self.plateau.tourj][0], posCourante[self.plateau.tourj], self.plateau.posJoueur[self.plateau.tourj])
                self.affichePlateau()
                posCourante = []
            self.Game()

    def getpltaux(self, datas):
        e = 0
        data = datas.split('/', 72)
        for i in range(0, 72):
            if i < 6:
                self.plateau.posJoueur[i] = int(data[i])
            elif 5 < i < 12:
                self.plateau.argentJoueur[i-6] = int(data[i])
            elif 11 < i < 68:
                if not i%2:
                    self.plateau.propriete[e].proprietaire = int(data[i])
                else:
                    self.plateau.propriete[e].constructions = int(data[i])
                    e+=1
            elif i == 68:
                self.plateau.de1 = int(data[i])
            elif i == 69:
                self.plateau.de2 = int(data[i])
            elif i == 70:
                self.plateau.tour = int(data[i])
            elif i == 71:
                self.plateau.tourj = int(data[i])

    def sendplt(self):
        e = 0
        data = ""
        for i in range(0, 72):
            if i < 6:
                data += (str(self.plateau.posJoueur[i]))
                data += ('/')
            elif 5 < i < 12:
                data += (str(self.plateau.argentJoueur[i-6]))
                data += ('/')
            elif 11 < i < 68:
                if not i%2:
                    data += (str(self.plateau.propriete[e].proprietaire))
                    data += ('/')
                else:
                    data += (str(self.plateau.propriete[e].constructions))
                    data += ('/')
                    e+=1
            elif i == 68:
                data += (str(self.plateau.de1))
                data += ('/')
            elif i == 69:
                data += (str(self.plateau.de2))
                data += ('/')
            elif i == 70:
                data += (str(self.plateau.tour))
                data += ('/')
            elif i == 71:
                data += (str(self.plateau.tourj))
        self.client.send(('PLT ' + data))

    def attribue(self):
        typeCase = type(Propriete())
        for i in range(0,len(self.plateau.propriete)):
            for j in range(0,len(cases)):
                if isinstance(cases[j], typeCase):
                    if self.plateau.propriete[i].nom == cases[j].nom:
                        cases[j] = self.plateau.propriete[i]

    def getPrice(self, index):
        e = 0
        for i in range(0, len(self.plateau.propriete)):
            if self.plateau.propriete[i].nom == cases[index].nom:
                if cases[index].nom.startswith('Gare'):
                    if cases[5].proprietaire == cases[index].proprietaire:
                      e += 1
                    if cases[15].proprietaire == cases[index].proprietaire:
                      e += 1
                    if cases[25].proprietaire == cases[index].proprietaire:
                      e += 1
                    if cases[35].proprietaire == cases[index].proprietaire:
                      e += 1
                    return prixcst[len(prixcst)-1][e-1]
                elif cases[index].nom.startswith('Compagnie'):
                    if cases[12].proprietaire == cases[index].proprietaire:
                        e +=1
                    if cases[28].proprietaire == cases[index].proprietaire:
                        e += 1
                    if e == 1:
                        return (self.plateau.de1 + self.plateau.de2) * 4
                    else:
                        return (self.plateau.de1 + self.plateau.de2) * 10
                return prixcst[i][self.plateau.propriete[i].constructions]


    def prixpourcst(self, index):
        if index < 5:
            return 50
        elif index < 11:
            return 100
        elif index < 17:
            return 150
        else:
            return 200



    def procedure(self, indexCase):
        if len(self.mesProprietes):
            choix = 0
            while choix != 2:
                choix = self.menu_choix(indexCase)
                if choix == 0:
                    selected = self.selectHypo()
                    while selected != -1:
                        self.affichePlateau()
                        self.attribue()
                        if self.plateau.propriete[selected].nom.startswith("Gare") or self.plateau.propriete[selected].nom.startswith("Compagnie"):
                            self.plateau.argentJoueur[self.index] += int(self.plateau.propriete[selected].prix/2)
                            self.plateau.propriete[selected].proprietaire = 0
                            self.affichePlateau()
                        else:
                            title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Que voulez-vous vendre?", (255,255,255),(255,0,0))
                            vente = self.menu_boutons(0, "Propriété", "Construction", title)
                            if vente == 0:
                                self.plateau.argentJoueur[self.index] += int((self.plateau.propriete[selected].prix/2)) + int((self.plateau.propriete[selected].constructions * (self.prixpourcst(selected)/2)))
                                self.plateau.propriete[selected].proprietaire = 0
                                self.plateau.propriete[selected].constructions = 0
                                self.affichePlateau()
                                break
                            elif vente == 1:
                                if self.plateau.propriete[selected].constructions:
                                    self.plateau.argentJoueur[self.index] += int(self.prixpourcst(selected)/2)
                                    self.plateau.propriete[selected].constructions -= 1
                                    self.affichePlateau()
                                else:
                                    pass
                            if not len(self.mesProprietes):
                                choix = 2
                        selected = self.selectHypo()
                if choix == 1:
                    selected = self.selectHypo()
                    if self.plateau.propriete[selected].nom.startswith("Gare") or self.plateau.propriete[selected].nom.startswith("Compagnie"):
                        break
                    self.affichePlateau()
                    while selected != -1:
                        if self.plateau.propriete[selected].nom.startswith("Gare") or self.plateau.propriete[selected].nom.startswith("Compagnie"):
                            break
                        self.affichePlateau()
                        self.attribue()
                        if self.plateau.propriete[selected].constructions == 5:
                            break
                        if self.plateau.argentJoueur[self.index] < self.prixpourcst(selected):
                            title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Vous n'avez pas assez d'argent!", (255,255,255),(255,0,0))
                            self._win.blit(title, (230,200))
                            pygame.display.flip()
                        else:
                            self.plateau.argentJoueur[self.index] -= self.prixpourcst(selected)
                            self.plateau.propriete[selected].constructions += 1
                            self.affichePlateau()
                        selected = self.selectHypo()
                if choix == 3:
                    self.client.send(('FIN ' + self.client.pseudo))
                    self.affichePlateau()
                    title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Vous avez perdu!", (255,255,255),(255,0,0))
                    self._win.blit(title, (300,200))
                    pygame.display.flip()
                    self.continuer = False
                    return

                self.affichePlateau()
        else:
            self.finDuTour()

    def totalPossede(self):
        total = 0
        self.getPropriete()
        for i in range(0, len(self.mesProprietes)):
            total += self.mesProprietes[i].prix/2
            total += int((self.plateau.propriete[self.getProprieteIndex(self.mesProprietes[i].nom)].constructions * (self.prixpourcst(self.getProprieteIndex(self.mesProprietes[i].nom))/2)))
        total += self.plateau.argentJoueur[self.index]
        return int(total)



    def Game(self):
        indexCase = self.plateau.posJoueur[self.index]
        typeCase = type(Propriete())
        self.getPropriete()
        if self.plateau.tourj == self.index:
            if self.plateau.posJoueur[self.index] - self.plateau.de1 - self.plateau.de2 < 0 and self.plateau.posJoueur[self.index] != 0 and self.plateau.tour > 0:
                self.plateau.argentJoueur[self.index] += 200
            if isinstance(cases[indexCase], typeCase):
                if not cases[indexCase].proprietaire:
                    self.affichePlateau()
                    title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Voulez-vous acheter " + cases[indexCase].nom + " pour " + str(cases[indexCase].prix) + "€?", (255,255,255),(255,0,0))
                    choix = self.menu_boutons(indexCase, "Acheter ("+str(cases[indexCase].prix)+"€)", "Refuser", title)
                    if choix == 0:
                        if self.plateau.argentJoueur[self.index] >= cases[indexCase].prix:
                            son = pygame.mixer.Sound("PlateauMonopoly/Sons/KaChing.wav")
                            son.play()
                            cases[indexCase].proprietaire = self.index+1
                            self.plateau.argentJoueur[self.index] -= cases[indexCase].prix
                            self.getPropriete()
                        else:
                            self.affichePlateau()
                            title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Vous n'avez pas assez d'argent!", (255,255,255),(255,0,0))
                            self._win.blit(title, (230,200))
                            pygame.display.flip()
                            self.procedure(indexCase)
                    self.affichePlateau()
                    self.procedure(indexCase)
                    if self.plateau.tourj < self.info.nbJoueurs-1:
                        self.plateau.tourj += 1
                    elif self.plateau.de1 == self.plateau.de2:
                        pass
                    else:
                        self.plateau.tour += 1
                        self.plateau.tourj = 0
                    self.sendplt()
                elif cases[indexCase].proprietaire == self.index+1:
                    title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Vous êtes chez vous!", (255,255,255),(255,0,0))
                    self._win.blit(title, (330,160))
                    pygame.display.flip()
                    self.procedure(indexCase)
                    if self.plateau.tourj < self.info.nbJoueurs-1:
                        self.plateau.tourj += 1
                    elif self.plateau.de1 == self.plateau.de2:
                        pass
                    else:
                        self.plateau.tour += 1
                        self.plateau.tourj = 0
                    self.sendplt()
                else:
                    title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Vous devez "+str(self.getPrice(indexCase))+"€ à "+self.info.nomJoueur[cases[indexCase].proprietaire-1], (255,255,255),(255,0,0))
                    self._win.blit(title, (330,160))
                    pygame.display.flip()
                    if self.plateau.argentJoueur[self.index] < self.getPrice(indexCase):
                        if self.totalPossede() < self.getPrice(indexCase):
                            self.client.send(('FIN ' + self.client.pseudo))
                            self.affichePlateau()
                            title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Vous avez perdu!", (255,255,255),(255,0,0))
                            self._win.blit(title, (300,200))
                            pygame.display.flip()
                            self.continuer = False
                            return
                        while self.plateau.argentJoueur[self.index] < self.getPrice(indexCase):
                            self.procedure(indexCase)
                    self.plateau.argentJoueur[self.index] -= self.getPrice(indexCase)
                    self.plateau.argentJoueur[cases[indexCase].proprietaire-1] += self.getPrice(indexCase)
                    self.procedure(indexCase)
                    if self.plateau.tourj < self.info.nbJoueurs-1:
                        self.plateau.tourj += 1
                    elif self.plateau.de1 == self.plateau.de2:
                        pass
                    else:
                        self.plateau.tour += 1
                        self.plateau.tourj = 0
                    self.sendplt()
            elif cases[indexCase] == "allez prison":
                self.plateau.posJoueur[self.index] = 10
                self.procedure(indexCase)
                if self.plateau.tourj < self.info.nbJoueurs-1:
                    self.plateau.tourj += 1
                elif self.plateau.de1 == self.plateau.de2:
                    pass
                else:
                    self.plateau.tour += 1
                    self.plateau.tourj = 0
                self.affichePlateau()
                self.sendplt()
            elif cases[indexCase] == "prison":
                self.plateau.posJoueur[self.index] = 30
                self.procedure(indexCase)
                if self.plateau.tourj < self.info.nbJoueurs-1:
                    self.plateau.tourj += 1
                elif self.plateau.de1 == self.plateau.de2:
                    pass
                else:
                    self.plateau.tour += 1
                    self.plateau.tourj = 0
                time.sleep(1)
                self.affichePlateau()
                self.affichePlateau()
                self.sendplt()
            elif cases[indexCase] == 'depart':
                self.plateau.argentJoueur[self.index] += 400
                self.procedure(indexCase)
                if self.plateau.tourj < self.info.nbJoueurs-1:
                    self.plateau.tourj += 1
                elif self.plateau.de1 == self.plateau.de2:
                    pass
                else:
                    self.plateau.tour += 1
                    self.plateau.tourj = 0
                self.sendplt()
            elif cases[indexCase] == 'impôts':
                if self.plateau.argentJoueur[self.index] < 200:
                    if self.totalPossede() < 200:
                        self.client.send(('FIN ' + self.client.pseudo))
                        self.affichePlateau()
                        title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Vous avez perdu!", (255,255,255),(255,0,0))
                        self._win.blit(title, (300,200))
                        pygame.display.flip()
                        self.continuer = False
                        return
                    while self.plateau.argentJoueur[self.index] < 200:
                        self.procedure(indexCase)
                self.plateau.argentJoueur[self.index] -= 200
                self.procedure(indexCase)
                if self.plateau.tourj < self.info.nbJoueurs-1:
                    self.plateau.tourj += 1
                elif self.plateau.de1 == self.plateau.de2:
                    pass
                else:
                    self.plateau.tour += 1
                    self.plateau.tourj = 0
                self.sendplt()
            elif cases[indexCase] == 'taxe':
                if self.plateau.argentJoueur[self.index] < 100:
                    if self.totalPossede() < 100:
                        self.client.send(('FIN ' + self.client.pseudo))
                        self.affichePlateau()
                        title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Vous avez perdu!", (255,255,255),(255,0,0))
                        self._win.blit(title, (300,200))
                        pygame.display.flip()
                        self.continuer = False
                        return
                    while self.plateau.argentJoueur[self.index] < 100:
                        self.procedure(indexCase)
                if self.plateau.tourj < self.info.nbJoueurs-1:
                    self.plateau.tourj += 1
                elif self.plateau.de1 == self.plateau.de2:
                    pass
                else:
                    self.plateau.tour += 1
                    self.plateau.tourj = 0
                self.sendplt()
            elif cases[indexCase] == 'chance':
                with self.lock:
                    pygame.event.set_blocked(pygame.KEYDOWN)
                    prix = random.randint(-200,200)
                    if prix >= 0:
                        price = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Vous avez gagné " + str(prix) + "€!", (255,255,255), (1,1,1))
                    if prix < 0:
                        price = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Vous avez perdu "+ str(abs(prix))+ "€!", (255,255,255), (1,1,1))
                    title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Appuyez sur entrée pour dévoiler.", (255,255,255), (1,1,1))
                    self._win.blit(imgChance, (230, 350))
                    self._win.blit(title, (280, 300))
                    pygame.display.flip()
                    event = pygame.event.wait()
                    while(event.key != pygame.K_RETURN):
                        event = pygame.event.wait()
                    self._win.blit(imgChanceV, (230, 350))
                    self._win.blit(price, (280, 500))
                    pygame.display.flip()
                    event = pygame.event.wait()
                    while(event.key != pygame.K_RETURN):
                        event = pygame.event.wait()
                if prix < 0 and abs(prix) > self.plateau.argentJoueur[self.index]:
                    self.plateau.argentJoueur[self.index] = 0
                else:
                    self.plateau.argentJoueur[self.index] += prix
                self.affichePlateau()
                self.procedure(indexCase)
                if self.plateau.tourj < self.info.nbJoueurs-1:
                    self.plateau.tourj += 1
                elif self.plateau.de1 == self.plateau.de2:
                    pass
                else:
                    self.plateau.tour += 1
                    self.plateau.tourj = 0
                self.sendplt()
            elif cases[indexCase] == "Communauté":
                with self.lock:
                    pygame.event.set_blocked(pygame.KEYDOWN)
                    prix = random.randint(-200,200)
                    if prix >= 0:
                        price = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Vous avez gagné " + str(prix) + "€!", (255,255,255), (1,1,1))
                    if prix < 0:
                        price = textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 20), "Vous avez perdu "+ str(abs(prix))+ "€!", (255,255,255), (1,1,1))
                    title=textOutline(pygame.font.Font('PlateauMonopoly/Font/MainFont.otf', 25), "Appuyez sur entrée pour dévoiler.", (255,255,255), (1,1,1))
                    self._win.blit(imgCommu, (230, 350))
                    self._win.blit(title, (280, 300))
                    pygame.display.flip()
                    event = pygame.event.wait()

                    while(event.key != pygame.K_RETURN):
                        event = pygame.event.wait()
                    self._win.blit(imgCommuV, (230, 350))
                    self._win.blit(price, (400, 500))
                    pygame.display.flip()
                    event = pygame.event.wait()
                    while(event.key != pygame.K_RETURN):
                        event = pygame.event.wait()
                if prix < 0 and abs(prix) > self.plateau.argentJoueur[self.index]:
                    self.plateau.argentJoueur[self.index] = 0
                else:
                    self.plateau.argentJoueur[self.index] += prix
                self.affichePlateau()
                self.procedure(indexCase)
                if self.plateau.tourj < self.info.nbJoueurs-1:
                    self.plateau.tourj += 1
                elif self.plateau.de1 == self.plateau.de2:
                    pass
                else:
                    self.plateau.tour += 1
                    self.plateau.tourj = 0
                self.sendplt()
            else:
                self.procedure(indexCase)
                if self.plateau.tourj < self.info.nbJoueurs-1:
                    self.plateau.tourj += 1
                elif self.plateau.de1 == self.plateau.de2:
                    pass
                else:
                    self.plateau.tour += 1
                    self.plateau.tourj = 0
                self.sendplt()



class Client:
    def __init__(self, q):
        lstpseud = ""
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.connect()
        try:
            self._sock.connect((self.host, int(self.port)))
        except socket.error as e:
            return
        s, _, _ = select.select([self._sock], [], [])
        msg = self._sock.recv(1024).decode().strip()
        if len(msg) > 3:
            lstpseud = msg.split(" ", 1)[1]
        self.login()
        while self.pseudo in lstpseud:
            self.login()
        self._q = q
        self.begin = False
        self._t = threading.Thread(target=self.recv, daemon=True)
        self._run = True
        print("Attente des autres joueurs...")
        self._t.start()

    def send(self, msg):
        self._sock.send((msg + '\n').encode())

    def sendpseudo(self, evt=None):
        self.pseudo = self.log.get()
        self._sock.send(("PSD " + self.pseudo + '\n').encode())
        self.Login.destroy()

    def recv(self):
        while self._run:
            s, _, _ = select.select([self._sock], [], [])
            msg = self._sock.recv(1024).decode().strip()
            if msg.startswith('PLT'):
                self._q.put(('data', msg))
            if msg.startswith('INF'):
                self._q.put(('info', msg))
                print("La partie va commencer...")
                time.sleep(4)
                self.begin = True
            if msg.startswith('FIN'):
                self._q.put(('fin', msg))


    def login(self):
        self.Login = Tk()
        self.Login.wm_attributes("-topmost", 1)
        self.Login.title("Connexion")
        label = Label(self.Login, text="Pseudo")
        label.grid(row=0, column =0)
        self.log = Entry(self.Login)
        self.log.grid(row=0, column=1)
        self.log.bind('<Return>', self.sendpseudo)
        self.log.focus()
        button = Button(self.Login, text="Log In", command = self.sendpseudo)
        button.grid(row=2, column=1)
        self.Login.mainloop()

    def connect(self):
        def bouton(tk):
            self.host = entry.get()
            self.port = entry2.get()
            tk.destroy()
        tk = Tk()
        tk.title("Connexion")
        label = Label(tk, text="Host")
        label.grid(row=0, column =0)
        entry = Entry(tk)
        entry.grid(row=0, column=1)
        label2 = Label(tk, text="Port")
        label2.grid(row=1, column =0)
        entry2 = Entry(tk, textvariable="Host")
        entry2.grid(row=1, column=1)
        button = Button(tk, text="Connect/Host", command = lambda: bouton(tk) )
        button.grid(row=2, column=1)
        tk.mainloop()



class Monopoly:
    def __init__(self):
        self.q = queue.Queue()
        self.client = Client(self.q)
        self.gui = GUI(self.client, self.q)


if __name__ == '__main__':
    cases = ["depart", Propriete("Boulevard de Belleville", 0, 0, 60), "Communauté", Propriete("Rue Lecourbe", 0, 0, 60), "impôts",  Propriete("Gare MontParnasse", 0, 0, 200), Propriete("Rue de Vaugirard", 0, 0, 100), "chance", Propriete("Rue de Courcelles", 0, 0, 100), Propriete("Avenue de la République", 0, 0, 120), "prison", Propriete("Boulevard de la Villette", 0, 0, 140), Propriete("Compagnie de distribution d'électricité", 5, 0, 140), Propriete("Avenue de Neuilly", 0, 0, 140), Propriete("Rue de Paradis", 0, 0, 160), Propriete("Gare de Lyon", 0, 0, 200), Propriete("Avenue Mozart", 0, 0, 180), "Communauté", Propriete("Boulevard Saint-Michel", 0, 0, 180), Propriete("Place Pigalle", 0, 0, 200), "parc gratuit", Propriete("Avenue Matignon", 0, 0, 220), "chance", Propriete("Boulevard Malesherbe", 0, 0, 220), Propriete("Avenue Henri-Martin", 0, 0, 240), Propriete("Gare du Nord", 0, 0, 200), Propriete("Faubourg Saint-Honoré", 0, 0, 260), Propriete("Place de la Bourse", 0, 0, 260), Propriete("Compagnie de distribution des eaux", 0, 0, 150), Propriete("Rue La Fayette", 0, 0, 280), "allez prison", Propriete("Avenue de Breteuil", 0, 0, 300), Propriete("Avenue Foch", 0, 0, 300), "Communauté",Propriete("Boulevard des Capucines", 0, 0, 320), Propriete("Gare Saint-Lazarre", 0, 0, 200), "chance", Propriete("Avenue des Champs-Elysées", 0, 0, 350), "taxe", Propriete("Rue de la Paix", 0, 0, 400)]

    prixcst=[[2,10,30,90,160,250],[4,20,60,180,320,450],[6,30,90,270,400,550],[6,30,90,270,400,550],[8,40,100,300,450,600],[10,50,150,450,625,750],[10,50,150,450,625,750],[12,60,180,500,700,900],[14,70,200,550,750,950],[14,70,200,550,750,950],[16,80,220,600,800,1000],[18,90,250,700,875,1050],[18,90,250,700,875,1050],[20,100,300,750,925,1100],[22,110,330,800,975,1150],[22,110,330,800,975,1150],[24,120,360,850,1025,1200],[26,130,390,900,1100,1275],[26,130,390,900,1100,1275],[28,150,450,1000,1200,1400],[35,175,500,1100,1300,1500],[50,200,600,1400,1700,2000],[25,50,100,200]]

    possCoord = [[1088, 108], [1088, 74], [1126, 108], [1126, 74], [1126, 40], [1164, 108], [1164, 74], [1164, 40],  [1202, 108], [1202, 74], [1202, 40], [1239, 108], [1239, 74], [1239, 40], [1276, 108], [1276, 74],[1276, 40], [1312, 108], [1312, 74], [1312, 40], [1349, 108], [1349, 74], [1386, 109], [1386, 78],[1386, 47],[1386, 16],  [1421, 108], [1421, 74]]

    houseCoords = [[761, 783], [615, 783], [396, 783], [250, 783], [177, 783], [103, 759], [103, 613], [103, 540], [103, 394], [103, 248], [103, 175], [127, 102], [273, 102], [346, 102], [492, 102], [565, 102], [711, 102], [784, 126], [784, 199], [784, 345], [784, 564], [784, 710]]

    images = []
    images2 = []
    casesCoord = []
    hypoCoord = []
    cartesHypo = []
    Monopoly()
