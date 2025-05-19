"""
Module TicTacToe
----------------
Ce module implémente le jeu du Tic-Tac-Toe (morpion) en utilisant des classes pour représenter la grille, le graphe des états du jeu, et un joueur automatique (ordinateur).

Classes principales :
---------------------
- grille :
    Représente une grille de jeu 3x3. Permet d'ajouter un symbole, de vérifier le gagnant, de générer les grilles possibles, et de comparer des grilles.
    Méthodes principales :
        - __init__(self, t=None) : Initialise la grille vide ou à partir d'une grille existante.
        - a_qui_le_tour(self) : Retourne le symbole du joueur dont c'est le tour ('X' ou 'O').
        - ajout_symbole(self, symb, x, y) : Retourne une nouvelle grille avec le symbole ajouté aux coordonnées (x, y).
        - verif_winner(self) : Vérifie s'il y a un gagnant sur la grille.
        - getNouvellesGrillesPossibles(self) : Retourne la liste des nouvelles grilles possibles après le coup du joueur courant.
        - __eq__, __hash__, __str__, __repr__ : Pour la comparaison, l'affichage et l'utilisation dans des ensembles/dictionnaires.

- grapheB (hérite de GrapheD) :
    Représente le graphe des états du jeu, où chaque sommet est une grille. Génère toutes les grilles possibles et calcule les attracteurs (stratégies gagnantes).
    Méthodes principales :
        - __init__(self) : Initialise le graphe avec la grille de départ et construit le graphe des états.
        - creation_tte_les_grilles(self) : Génère toutes les grilles possibles et les transitions.
        - creation_des_attracteurs(self) : Calcule les attracteurs pour chaque joueur.

- ordi :
    Implémente un joueur automatique qui choisit le meilleur coup selon les attracteurs calculés.
    Méthodes principales :
        - __init__(self, G, symb="X") : Initialise l'ordinateur avec le graphe et le symbole du joueur.
        - extension_chemin_rec(self, grille) : Cherche récursivement les chemins menant à la victoire.
        - extension_chemin(self, chemin) : Étend un chemin jusqu'à la victoire.
        - choix(self) : Retourne le meilleur coup à jouer selon la stratégie gagnante ou nulle.
        - update_curseur(self, grille) : Met à jour la position courante de l'ordinateur.

Dépendances :
-------------
- Jeux_a_deux_joueur (pour GrapheD et calculeAttracteur)
- random (pour les choix aléatoires)
"""

from Jeux_a_deux_joueur import GrapheD, calculeAttracteur
import random


class grille :
    """
    Classe représentant une grille de jeu de Tic-Tac-Toe (morpion).

    Attributs :
    -----------
    g : list[list[str|None]]
        Grille 3x3 contenant les symboles 'X', 'O' ou None pour une case vide.

    """

    def __init__(self, t=None):
        """
        Initialise une grille de Tic-Tac-Toe vide ou à partir d'une grille existante.

        Paramètres
        ----------
        t : list[list[str|None]], optionnel
            Grille existante à copier. Si None, crée une grille vide.
        """
        if t is None:
            self.g = [[None for _ in range(3)] for _ in range(3)]
        else:
            self.g = [row[:] for row in t]  
    
    def a_qui_le_tour(self) :
        """
        Détermine à qui c'est le tour de jouer ('X' ou 'O').

        Retourne
        -------
        str
            'X' si c'est au tour de X, 'O' sinon.
        """
        d = {"X" : 0, "O": 0}
        for r in self.g :
            for c in r :
                if not c is None :
                    d[c] += 1
        if d["X"] == d["O"] :    
            return "X"
        elif d["X"] > d["O"] :
            return "O"
        else :
            raise ValueError(f"{d}, {self}")
    
    def __str__(self) :
        """
        Retourne une représentation textuelle de la grille.

        Retourne
        -------
        str
            Grille formatée ligne par ligne.
        """
        txt = ""
        for ligne in self.g :
            txt += str(ligne) + "\n"
        return txt
    
    def ajout_symbole(self, symb, x, y) :
        """
        Retourne une nouvelle grille avec le symbole ajouté aux coordonnées (x, y).

        Paramètres
        ----------
        symb : str
            'X' ou 'O'.
        x : int
            Colonne (0, 1 ou 2).
        y : int
            Ligne (0, 1 ou 2).

        Retourne
        -------
        grille
            Nouvelle grille avec le symbole ajouté.

        Exceptions
        ----------
        IndexError
            Si la case est déjà occupée.
        """
        new_g = grille(self.g)
        if self.g[y][x] is None :
            new_g.g[y][x] = symb
            return new_g
        else :
            raise IndexError(f"les coordonées données sont déjà occupées par {self.g[y][x]}")
    
    def verif_winner(self) :
        """
        Vérifie s'il y a un gagnant sur la grille (lignes, colonnes, diagonales).

        Retourne
        -------
        str ou None
            'X' si X a gagné, 'O' si O a gagné, None sinon.
        """
        #verif colonnes
        for i in range(3) :
            colonne = [self.g[j][i] for j in range(3)]
            if colonne == ["X", "X", "X"] :
                return "X"
            elif colonne == ["O"]*3 :
                return "O"
    
        #verif lignes
        for i in range(3) :
            if self.g[i] == ["X", "X", "X"] :
                return "X"
            elif self.g[i] == ["O"]*3 :
                return "O"
        #verif diag
        diag1 = [self.g[i][i] for i in range(3)]
        diag2 = [self.g[i][2-i] for i in range(3)]
        if diag1 == ["X", "X", "X"] or diag2 == ["X", "X", "X"]:
                return "X"
        elif diag1 == ["O"]*3 or diag2 == ["O"]*3 :
                return "O"
        return None
        
    def getNouvellesGrillesPossibles(self):
        """
        Retourne la liste des nouvelles grilles possibles après le coup du joueur courant.

        Retourne
        -------
        list[grille]
            Liste des grilles résultant de tous les coups possibles.
        """
        joueur = self.a_qui_le_tour()
        nouvelles_grilles = []
        for y in range(3):
            for x in range(3):
                if self.g[y][x] is None:
                    try:
                        nouvelle_grille = self.ajout_symbole(joueur, x, y)
                        nouvelles_grilles.append(nouvelle_grille)
                    except IndexError:
                        continue
        return nouvelles_grilles
    
    def __eq__(self, other):
        """
        Compare deux grilles pour l'égalité.

        Paramètres
        ----------
        other : grille
            Autre grille à comparer.

        Retourne
        -------
        bool
            True si les grilles sont identiques, False sinon.
        """
        if not isinstance(other, grille):
            return False
        return self.g == other.g

    def __hash__(self):
        """
        Rend la grille utilisable dans des ensembles ou comme clé de dictionnaire.

        Retourne
        -------
        int
            Hash de la grille.
        """
        # Convertir la grille (liste de listes) en un tuple de tuples pour être hashable
        return hash(tuple(tuple(row) for row in self.g))
    
    def __repr__(self):
        """
        Retourne une représentation compacte de la grille pour le debug.

        Retourne
        -------
        str
            Représentation compacte de la grille.
        """
        txt = ""
        for i, ligne in enumerate(self.g):
            txt += " | ".join(c if c is not None else " " for c in ligne)
            if i < 2:
                txt += " -> "
        return f"{txt}" 

class grapheB(GrapheD) :
    """
    Classe représentant un graphe biparti des états du jeu de Tic-Tac-Toe.
    Chaque sommet est une grille, et les arêtes représentent les coups possibles.
    Les sommets sont répartis en deux ensembles selon le joueur dont c'est le tour (S1 et S2).
    Les attracteurs permettent d'identifier les stratégies gagnantes pour chaque joueur.
    """
    def __init__(self) :
        """
        Initialise le graphe biparti avec la grille de départ, les ensembles de sommets,
        les attracteurs et construit le graphe des états du jeu.
        """
        g0 = grille()
        self.sommet = g0
        self.S1 = set()
        self.S1.add(g0)
        self.S2 = set()
        self.adj= {g0 : set()}
        self.attracteur1 = set()
        self.attracteur2 = set()
        self.creation_tte_les_grilles()
        self.creation_des_attracteurs()
    
    def creation_tte_les_grilles(self) :
        """
        Génère récursivement toutes les grilles possibles à partir de la grille initiale,
        construit les transitions (arêtes) et répartit les grilles dans les ensembles S1/S2
        selon le joueur dont c'est le tour.
        Marque les grilles terminales dans les attracteurs correspondants.
        """
        grilles_suiv = [list(self.adj)[0]]
        partie_graphe = self.S2
        while len(grilles_suiv) > 0 :
            grille_actuelle = grilles_suiv.pop(0)
            nouvelles_grilles = grille_actuelle.getNouvellesGrillesPossibles()
            for g in nouvelles_grilles :
                partie_graphe = self.S1 if g.a_qui_le_tour() == "X" else self.S2
                #ajout grille à la partie correspondant au joueur qui joue
                if g not in partie_graphe :
                    partie_graphe.add(g)
                #on regarde si la grille est terminale
                winner = g.verif_winner()
                if not winner is None :
                    if winner == "X" :
                        self.attracteur1.add(g)
                    else :
                        self.attracteur2.add(g)
                else : #sinon on l'ajoute au point du graphe à étendre
                    if g not in self.adj :
                        grilles_suiv.append(g)
                #on ajoute la grille au graphe
                try :
                    self.ajouter_arc(grille_actuelle, g)
                except :
                    print(g)
                    print(grille_actuelle)
                    raise KeyError
            
    
    def creation_des_attracteurs(self) :
        """
        Calcule les attracteurs (stratégies gagnantes) pour chaque joueur à partir du graphe construit.
        """
        graphe = GrapheD()
        graphe.adj = self.adj
        self.attracteur1 = calculeAttracteur(graphe, self.S1, self.attracteur1)
        self.attracteur2 = calculeAttracteur(graphe, self.S2, self.attracteur2)

    
class ordi :
    """
    Classe représentant un joueur automatique (ordinateur) pour le Tic-Tac-Toe.
    Utilise les attracteurs du graphe biparti pour choisir le meilleur coup possible.
    """
    def __init__(self, G, symb="X") :
        """
        Initialise l'ordinateur avec le graphe des états et le symbole du joueur.

        Paramètres
        ----------
        G : grapheB
            Graphe biparti des états du jeu.
        symb : str, optionnel
            Symbole du joueur contrôlé par l'ordinateur ('X' ou 'O').
        """
        self.G = G
        self.curseur = self.G.sommet
        self.symb = symb
        if symb == "X":
            self.mon_attracteur = self.G.attracteur1
            self.attracteur_adverse = self.G.attracteur2
            self.grille_mon_tour = self.G.S1
            self.grille_son_tour = self.G.S2
        else:
            self.mon_attracteur = self.G.attracteur2
            self.attracteur_adverse = self.G.attracteur1
            self.grille_mon_tour = self.G.S2
            self.grille_son_tour = self.G.S1
    
    
    
    def choix(self) :
        if self.curseur in self.mon_attracteur :
            return min([g for g in self.G.voisins(self.curseur) if g in self.mon_attracteur], key=lambda x : self.mon_attracteur[x])
        elif self.curseur in self.attracteur_adverse :
            return max([g for g in self.G.voisins(self.curseur) if g in self.attracteur_adverse], key=lambda x : self.attracteur_adverse[x])
        else : 
            return random.choice([e for e in self.G.voisins(self.curseur)  if e not in self.attracteur_adverse])
        
    
    
    
    def update_curseur(self, grille) :
        """
        Met à jour la position courante de l'ordinateur (curseur) avec la nouvelle grille.

        Paramètres
        ----------
        grille : grille
            Nouvelle grille courante.
        """
        self.curseur = grille
        





#test

graph = grapheB()
for i in range(min(5,len(graph.attracteur1))) :
    #print(list(graph.attracteur1)[i])
    pass

#print(grille() in graph.attracteur1)

#print(len(graph.attracteur1))
#print(len(graph.attracteur2))
#print(len(graph.adj))

#print("Intersection attracteur1 & attracteur2 est vide", not (set(graph.attracteur1) & set(graph.attracteur2)))

ordii = ordi(graph, "X")
#print(ordii.choix())

def test_ordi_choix_victoire_immediate():
    """L'ordi doit jouer pour gagner immédiatement."""
    g = grille([
        ["X", "X", None],
        ["O", "O", None],
        [None, None, None]
    ])
    graph = grapheB()
    ordi_x = ordi(graph, symb="X")
    ordi_x.curseur = g
    coup = ordi_x.choix()
    print("Grille avant le coup :")
    print(g)
    print("Coup choisi par l'ordi :")
    print(coup)
    assert coup.g[0][2] == "X", "L'ordi doit jouer pour gagner immédiatement sur la ligne 0"

def test_ordi_choix_blocage_adverse():
    """L'ordi doit bloquer la victoire de l'adversaire."""
    g = grille([
        ["O", None, None],
        ["X", "X", None],
        [None, None, None]
    ])
    graph = grapheB()
    ordi_o = ordi(graph, symb="O")
    ordi_o.curseur = g
    coup = ordi_o.choix()
    print("Grille avant le coup :")
    print(g)
    print("Coup choisi par l'ordi :")
    print(coup)
    assert coup.g[1][2] == "O", "L'ordi doit bloquer la victoire de X sur la ligne 1"

def test_ordi_choix_match_nul():
    """Situation où seul un match nul est possible."""
    g = grille([
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", None]
    ])
    graph = grapheB()
    ordi_x = ordi(graph, symb="X")
    ordi_x.curseur = g
    coup = ordi_x.choix()
    print("Grille avant le coup :")
    print(g)
    print("Coup choisi par l'ordi :")
    print(coup)
    assert coup.g[2][2] == "X", "L'ordi doit jouer le dernier coup pour un match nul"

def test_ordi_choix_aleatoire():
    """Situation sans stratégie gagnante ni nulle, l'ordi doit jouer quelque part."""
    g = grille([
        ["O", "X", "O"],
        ["X", "O", "X"],
        [None, None, None]
    ])
    graph = grapheB()
    ordi_o = ordi(graph, symb="X")
    ordi_o.curseur = g
    ordi_o.choix()
    coup = ordi_o.choix()
    print("Grille avant le coup :")
    print(g)
    print("Coup choisi par l'ordi :")
    print(coup)
    assert coup.g[2].count("X") == 1, "L'ordi doit jouer sur la dernière ligne"


if __name__ == "__main__":
    print(grille([['O', 'O', None],['X', 'X', None],[None, None, None]]) in grapheB().attracteur1)
    test_ordi_choix_victoire_immediate()
    test_ordi_choix_blocage_adverse()
    test_ordi_choix_match_nul()
    test_ordi_choix_aleatoire()
    print("Tous les tests ordi.choix() sont passés !")
    

    
