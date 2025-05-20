import pygame

def surbrillance_avec_texte(screen, rect, image, texte_surface, teinte=(100, 255, 100), alpha=80):
    """
    Affiche un bouton avec du texte et applique une surbrillance si la souris le survole.
    """
    screen.blit(image, rect.topleft)
    screen.blit(texte_surface, (rect.left + (rect.width - texte_surface.get_width()) // 2,
                                 rect.top + (rect.height - texte_surface.get_height()) // 2))
    x, y = pygame.mouse.get_pos()
    if rect.collidepoint(x, y):
        calque = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        masque = pygame.mask.from_surface(image)
        masque_surface = masque.to_surface(setcolor=(*teinte, alpha), unsetcolor=(0, 0, 0, 0))
        calque.blit(masque_surface, (0, 0))
        screen.blit(calque, rect.topleft)

def affichagemenu(screen, longueur, largeur):
    """
    Affiche le menu principal avec deux boutons : 'VS Ordi' et 'Ordi VS Ordi'.
    """
    screen.fill((255, 255, 255))
    image = pygame.image.load("Images/Background.png").convert_alpha()
    image = flouter_surface(image)
    image = pygame.transform.scale(image, (longueur, largeur))
    screen.blit(image, (0, 0))

    font = pygame.font.Font('Polices/CrayonHandRegular2016Demo.ttf', 50)
    text = pygame.image.load("Images/Tc.png").convert_alpha()
    text_img = pygame.transform.scale(text, (longueur * 3 // 4, largeur // 4))
    screen.blit(text_img, ((longueur - text_img.get_width()) // 2, largeur // 12))

    bouton_img = pygame.image.load("Images/bouton.png").convert_alpha()
    bouton_lo, bouton_la = longueur // 3, largeur // 6
    bouton_img = pygame.transform.scale(bouton_img, (bouton_lo, bouton_la))

    a = longueur // 2 - bouton_img.get_width() // 2
    b = largeur * 5 // 12

    bouton1_rect = pygame.Rect(a, b, bouton_lo, bouton_la)
    bouton2_rect = pygame.Rect(a, b + b // 3 + bouton_la, bouton_lo, bouton_la)

    text2 = font.render('VS Ordi', True, "white")
    text3 = font.render('Ordi VS Ordi', True, "white")

    surbrillance_avec_texte(screen, bouton1_rect, bouton_img, text2)
    surbrillance_avec_texte(screen, bouton2_rect, bouton_img, text3)

    return bouton1_rect, bouton2_rect

def flouter_surface(surface, niveau=2):
    """
    Applique un effet de flou à une surface.
    """
    taille = surface.get_size()
    petite = pygame.transform.smoothscale(surface, (taille[0] // niveau, taille[1] // niveau))
    return pygame.transform.smoothscale(petite, taille)

def fond_ecran(screen, longueur, largeur):
    """
    Affiche le fond d'écran principal.
    """
    image = pygame.image.load("Images/Background2.png").convert_alpha()
    image = pygame.transform.scale(image, (longueur, largeur))
    screen.blit(image, (0, 0))

def contourrouge(screen, longueur, largeur):
    """
    Affiche un contour rouge autour de l'écran.
    """
    image = pygame.image.load("Images/contour_rouge.png").convert_alpha()
    image = pygame.transform.scale(image, (longueur, largeur))
    screen.blit(image, (0, 0))

def contourbleu(screen, longueur, largeur):
    """
    Affiche un contour bleu autour de l'écran.
    """
    image = pygame.image.load("Images/contour_bleu.png").convert_alpha()
    image = pygame.transform.scale(image, (longueur, largeur))
    screen.blit(image, (0, 0))

def makequadrillage(screen, longueur, largeur):
    """
    Affiche un quadrillage 3x3 au centre de l'écran.
    """
    taille_case = min(longueur, largeur) // 4
    taille_grille = taille_case * 3
    origine_x = (longueur - taille_grille) // 2
    origine_y = (largeur - taille_grille) // 2

    quadrillage_image = pygame.image.load("Images/quadrillage.png").convert_alpha()
    quadrillage_image = pygame.transform.scale(quadrillage_image, (taille_grille, taille_grille))
    screen.blit(quadrillage_image, (origine_x, origine_y))

def affiche_grille(screen, longueur, largeur, tableau):
    """
    Affiche les symboles 'X' et 'O' sur la grille en fonction du tableau.
    """
    taille_case = min(longueur, largeur) // 4
    taille_grille = taille_case * 3
    origine_x = (longueur - taille_grille) // 2
    origine_y = (largeur - taille_grille) // 2

    taille_image = int(taille_case * 0.6)
    marge = (taille_case - taille_image) // 2

    croix = pygame.image.load("Images/croix.png").convert_alpha()
    rond = pygame.image.load("Images/rond.png").convert_alpha()
    croix = pygame.transform.scale(croix, (taille_image, taille_image))
    rond = pygame.transform.scale(rond, (taille_image, taille_image))

    for ligne in range(3):
        for col in range(3):
            x = origine_x + col * taille_case + marge
            y = origine_y + ligne * taille_case + marge

            if tableau[ligne][col] == "X":
                screen.blit(croix, (x, y))
            elif tableau[ligne][col] == "O":
                screen.blit(rond, (x, y))

def surbrillance_case_vide(screen, longueur, largeur, tableau, croix_path, teinte=(255, 50, 50), alpha=100):
    taille_case = min(longueur, largeur) // 4  
    taille_grille = taille_case * 3  
    origine_x = (longueur - taille_grille) // 2
    origine_y = (largeur - taille_grille) // 2

    taille_image = int(taille_case * 0.6)
    marge = (taille_case - taille_image) // 2

    croix = pygame.image.load(croix_path).convert_alpha()
    croix = pygame.transform.scale(croix, (taille_image, taille_image))

    x_souris, y_souris = pygame.mouse.get_pos()

    for ligne in range(3):
        for col in range(3):
            x_case = origine_x + col * taille_case
            y_case = origine_y + ligne * taille_case
            rect_case = pygame.Rect(x_case, y_case, taille_case, taille_case)

            if rect_case.collidepoint(x_souris, y_souris) and tableau[ligne][col] is None:
                teinte_croix = croix.copy()
                teinte_croix.fill((*teinte, alpha), special_flags=pygame.BLEND_RGBA_MULT)

                screen.blit(teinte_croix, (x_case + marge, y_case + marge))

def get_case_cliquee(longueur, largeur, pos_souris):
    """
    Retourne la case cliquée (ligne, colonne) ou None si le clic est hors de la grille.
    """
    x, y = pos_souris
    taille_case = min(longueur, largeur) // 4
    taille_grille = taille_case * 3
    origine_x = (longueur - taille_grille) // 2
    origine_y = (largeur - taille_grille) // 2

    for ligne in range(3):
        for col in range(3):
            x_case = origine_x + col * taille_case
            y_case = origine_y + ligne * taille_case
            rect = pygame.Rect(x_case, y_case, taille_case, taille_case)

            if rect.collidepoint(x, y):
                return ligne, col

    return None

def jouer_si_possible(tableau, pos, joueur):
    """
    Modifie la case du tableau si elle est vide.
    Renvoie True si le coup est joué, False sinon.
    """
    if pos is not None:
        ligne, col = pos
        if tableau[ligne][col] is None:
            tableau[ligne][col] = "X" if joueur == 1 else "O"
            return True
    return False

def affichagevotretour(screen,longueur,largeur, joueur):
    font = pygame.font.Font('Polices/CrayonHandRegular2016Demo.ttf', 80)

    if joueur == 1 :
        text = font.render('A votre tour', True, (255,68,56,255))
    else :
        text = font.render('A votre tour', True, (82,113,255,255))

    a = longueur // 2 - text.get_width() // 2
    b = largeur // 30
    
    screen.blit(text,(a,b))

def fin_du_jeu(tableau):
    for i in tableau:
        if i == ["O", "O", "O"]:
            return True, "O"
        elif i == ["X", "X", "X"]:
            return True, "X"
    for i in range(len(tableau)):
        if tableau[0][i] == tableau[1][i] == tableau[2][i] and tableau[0][i] in ["X", "O"]:
            return True, tableau[0][i]
    if tableau[0][0] == tableau[1][1] == tableau[2][2] and tableau[0][0] in ["X", "O"]:
        return True, tableau[0][0]
    if tableau[0][2] == tableau[1][1] == tableau[2][0] and tableau[0][2] in ["X", "O"]:
        return True, tableau[0][2]

    # Match nul si toutes les cases sont remplies sans gagnant
    if all(cell is not None for row in tableau for cell in row):
        return True, None

    return False, None

def creer_filtre_flou(surface, rect=None, niveau=4):
    if rect:
        zone = surface.subsurface(rect).copy()
    else:
        zone = surface.copy()

    taille = zone.get_size()
    petite = pygame.transform.smoothscale(zone, (taille[0]//niveau, taille[1]//niveau))
    flou = pygame.transform.smoothscale(petite, taille)
    return flou

def affichage_fin_du_jeu(screen, jgagnant, joueur, longueur, largeur):
    """
    Affiche le message de fin de jeu en fonction du gagnant.
    """
    zone_rect = pygame.Rect(0, 0, longueur, largeur)
    filtre = creer_filtre_flou(screen, rect=zone_rect, niveau=6)
    screen.blit(filtre, zone_rect.topleft)

    font = pygame.font.Font('Polices/CrayonHandRegular2016Demo.ttf', 80)

    if jgagnant is None:
        text = font.render("Match nul !", True, (120, 120, 120))
    elif jgagnant == joueur:
        text = font.render("Vous avez gagné !", True, (255, 68, 56) if joueur == "X" else (82, 113, 255))
    else:
        text = font.render("L'ordinateur a gagné !", True, (255, 68, 56) if jgagnant == "X" else (82, 113, 255))

    screen.blit(text, ((longueur - text.get_width()) // 2, (largeur - text.get_height()) // 2))

def affichage_fin_du_jeu_ordi(screen, jgagnant, joueur, longueur, largeur):
    zone_rect = pygame.Rect(0, 0, longueur, largeur)
    filtre = creer_filtre_flou(screen, rect=zone_rect, niveau=6)
    screen.blit(filtre, zone_rect.topleft)

    font = pygame.font.Font('Polices/CrayonHandRegular2016Demo.ttf', 80)

    if jgagnant == joueur and joueur == "X":
        text = font.render("L'ordinateur 2 a gagné !", True, (255, 68, 56, 255))
    elif jgagnant == joueur and joueur == "O":
        text = font.render("L'ordinateur 1 a gagné  !", True, (82, 113, 255, 255))
    elif jgagnant == "O" and jgagnant != joueur:
        text = font.render("L'ordinateur 1 a gagné !", True, (82, 113, 255, 255))
    elif jgagnant == "X" and jgagnant != joueur:
        text = font.render("L'ordinateur 1 gagné !", True, (255, 68, 56, 255))
    else:
        # Cas par défaut si aucune des conditions ci-dessus n'est satisfaite
        text = font.render("Match nul", True, (120, 120, 120))
    print(jgagnant)
    screen.blit(text, ((longueur - text.get_width()) // 2, (largeur - text.get_height()) // 2))