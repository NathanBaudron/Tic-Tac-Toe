from Jeux_a_deux_joueur import GrapheD, calculeAttracteur

class grille :
    
    def __init__(self, t=None):
        if t is None:
            self.g = [[None for _ in range(3)] for _ in range(3)]
        else:
            self.g = [row[:] for row in t]  
        
    def a_qui_le_tour(self) :
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
        txt = ""
        for ligne in self.g :
            txt += str(ligne) + "\n"
        return txt
    
    def ajout_symbole(self, symb, x, y) :
        """retourne une nouvelle grille avec le symbole ajouter aux coordonnées (x,y)

        Args:
            symb ("X" ou "O")
            x (int)
            y (int)

        Raises:
            IndexError: si la case est déjà occupée
        """
        new_g = grille(self.g)
        if self.g[y][x] is None :
            new_g.g[y][x] = symb
            return new_g
        else :
            raise IndexError(f"les coordonées données sont déjà occupées par {self.g[y][x]}")
    
    def verif_winner(self) :
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
        if not isinstance(other, grille):
            return False
        return self.g == other.g

    def __hash__(self):
        # Convertir la grille (liste de listes) en un tuple de tuples pour être hashable
        return hash(tuple(tuple(row) for row in self.g))
    

class grapheB(GrapheD) :
    
    def __init__(self) :
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
        grilles_suiv = [list(self.adj)[0]]
        partie_graphe = self.S2
        while len(grilles_suiv) > 0 :
            grille_actuelle = grilles_suiv.pop(0)
            nouvelles_grilles = grille_actuelle.getNouvellesGrillesPossibles()
            for g in nouvelles_grilles :
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
            #on change de joueur
            if partie_graphe == self.S1 :
                partie_graphe = self.S1
            else :
                partie_graphe = self.S1
                
                
                

                    
        
    
    def creation_des_attracteurs(self) :
        graphe = GrapheD()
        graphe.adj = self.adj
        self.attracteur1 = calculeAttracteur(graphe, self.S1, self.attracteur1)
        self.attracteur2 = calculeAttracteur(graphe, self.S2, self.attracteur2)

    
    
class ordi :
    
    def __init__(self, G, champ_vision = 20) :
        self.G = G
        self.curseur = self.G.sommet
        self.champ_vision = 20
    
    def choix(self) :
        pass
    
    
    




#test

g = grille()
t = g.getNouvellesGrillesPossibles()

for grill in t :
    #print(grill.a_qui_le_tour())

    pass


graph = grapheB()
for i in range(min(5,len(graph.attracteur1))) :
    #print(list(graph.attracteur1)[i])
    pass

#print(len(graph.attracteur1))
#print(len(graph.attracteur2))
#print(len(graph.adj))