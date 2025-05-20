from Fonctions import *
from TicTacToe import *
import pygame
import random

pygame.init()
screen = pygame.display.set_mode((0, 0))
longueur, largeur = screen.get_width(), screen.get_height()
Game = True
Menu = True
Manuel = False
Automatique = False
grille_jeu = grille()  # Instance de la classe grille
fin = False
timer = 0  # Timer pour gérer les délais
delai = 1000  # Délai en millisecondes (1 seconde)

# Initialisation des objets nécessaires
graph = grapheB()

while Game:
    while Menu:
        affichagemenu(screen, longueur, largeur)
        joueur1 = random.randint(0, 1)  # Détermine si le joueur humain commence
        joueur_symbole = "X" if joueur1 == 1 else "O"
        ordi1_symbole = "O" if joueur_symbole == "X" else "X"
        ordi2_symbole = joueur_symbole
        ordi1 = ordi(graph, symb=ordi1_symbole)
        ordi2 = ordi(graph, symb=ordi2_symbole)
        tour = 1 if joueur1 == 1 else 0
        grille_jeu = grille()
        ordi1.update_curseur(grille_jeu)
        ordi2.update_curseur(grille_jeu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Menu = False
                Game = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Menu = False
                    Game = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                bouton_lo, bouton_la = longueur // 3, largeur // 6
                a = longueur // 2 - bouton_lo // 2
                b = largeur * 5 // 12

                if a <= x <= a + bouton_lo:
                    if b <= y <= b + bouton_la:
                        Menu = False
                        Manuel = True
                    elif b + b // 3 + bouton_la <= y <= b + b // 3 + (2 * bouton_la):
                        Menu = False
                        Automatique = True

        pygame.display.flip()

    while Manuel:
        fond_ecran(screen, longueur, largeur)
        makequadrillage(screen, longueur, largeur)
        affiche_grille(screen, longueur, largeur, grille_jeu.g)

        if fin:
            affichage_fin_du_jeu(screen, grille_jeu.verif_winner(), joueur_symbole, longueur, largeur)
            if pygame.time.get_ticks() - timer >= delai:
                fin = False
                Manuel = False
                Menu = True
                grille_jeu = grille()
                ordi1.update_curseur(grille_jeu)
        else:
            if tour == 1:  # Tour du joueur humain
                if joueur1 == 1:
                    contourrouge(screen, longueur, largeur)
                    surbrillance_case_vide(screen, longueur, largeur, grille_jeu.g, "Images/croix.png")
                else:
                    contourbleu(screen, longueur, largeur)
                    surbrillance_case_vide(screen, longueur, largeur, grille_jeu.g, "Images/rond.png")
                affichagevotretour(screen, longueur, largeur, joueur1)

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        pos = pygame.mouse.get_pos()
                        case = get_case_cliquee(longueur, largeur, pos)
                        if case is not None:
                            try:
                                grille_jeu = grille_jeu.ajout_symbole(joueur_symbole, case[1], case[0])
                                ordi1.update_curseur(grille_jeu)
                                tour = 0
                            except IndexError:
                                pass
                    if event.type == pygame.QUIT:
                        Manuel = False
                        Game = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        Manuel = False
                        Menu = True
                        grille_jeu = grille()
            else:  # Tour de l'ordinateur
                if pygame.time.get_ticks() - timer >= delai:
                    timer = pygame.time.get_ticks()
                    if joueur_symbole == "X":
                        contourbleu(screen, longueur, largeur)
                    else:
                        contourrouge(screen, longueur, largeur)
                    grille_jeu = ordi1.choix()  # Utilise directement la grille retournée par ordi1.choix()
                    ordi1.update_curseur(grille_jeu)
                    tour = 1

        if (grille_jeu.verif_winner() is not None or all(cell is not None for row in grille_jeu.g for cell in row)) and not fin:
            timer = pygame.time.get_ticks()
            fin = True

        pygame.display.flip()

    while Automatique:
        fond_ecran(screen, longueur, largeur)
        makequadrillage(screen, longueur, largeur)
        affiche_grille(screen, longueur, largeur, grille_jeu.g)

        if fin:
            affichage_fin_du_jeu_ordi(screen, grille_jeu.verif_winner(), joueur1, longueur, largeur)
            if pygame.time.get_ticks() - timer >= delai:
                fin = False
                Automatique = False
                Menu = True
                grille_jeu = grille()
                ordi1.update_curseur(grille_jeu)
                ordi2.update_curseur(grille_jeu)
        else:
            if tour == 0:  # Tour de l'ordinateur avec le symbole "X"
                if pygame.time.get_ticks() - timer >= delai:
                    timer = pygame.time.get_ticks()
                    contourrouge(screen, longueur, largeur)
                    if ordi1.symb == "X":
                        grille_jeu = ordi1.choix()
                        ordi1.update_curseur(grille_jeu)
                        ordi2.update_curseur(grille_jeu)
                    else:
                        grille_jeu = ordi2.choix()
                        ordi1.update_curseur(grille_jeu)
                        ordi2.update_curseur(grille_jeu)
                    tour = 1  # Passe au tour de l'autre ordinateur
            else:  # Tour de l'ordinateur avec le symbole "O"
                if pygame.time.get_ticks() - timer >= delai:
                    timer = pygame.time.get_ticks()
                    contourbleu(screen, longueur, largeur)
                    if ordi1.symb == "O":
                        grille_jeu = ordi1.choix()
                        ordi1.update_curseur(grille_jeu)
                        ordi2.update_curseur(grille_jeu)
                    else:
                        grille_jeu = ordi2.choix()
                        ordi1.update_curseur(grille_jeu)
                        ordi2.update_curseur(grille_jeu)
                    tour = 0  # Passe au tour de l'ordinateur avec "X"

        if (grille_jeu.verif_winner() is not None or all(cell is not None for row in grille_jeu.g for cell in row)) and not fin:
            timer = pygame.time.get_ticks()
            fin = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Automatique = False
                Game = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                Automatique = False
                Menu = True
                grille_jeu = grille()
                ordi1.update_curseur(grille_jeu)
                ordi2.update_curseur(grille_jeu)

        pygame.display.flip()

pygame.quit()