class GrapheD:
    def _init_(self, adj={}):
        self.adj=adj

    def ajouter_sommet(self,s):
        self.adj[s]=set()
    
    def ajouter_arc(self,s1,s2):
        if s1 not in self.adj :
            self.ajouter_sommet(s1)
        if s2 not in self.adj :
            self.ajouter_sommet(s2)
        self.adj[s1].add(s2)
    
    def arc(self,s1,s2):
        if s2 in self.adj[s1]:
            return True
        return False

    def voisins(self,s):
        a=[]
        for e in self.adj[s]:
            a.append(e)
        return a 

    def afficher(self):
        for i in self.adj:
            print(i,end=" ")
            print(self.adj[i])
    
    def nb_sommets(self):
        a=0
        for e in self.adj :
            a+=1
        return a 

    def degre(self,s) :
        a=0
        for e in self.adj[s] :
            a+=1
        return a
    
    def nb_arcs(self):
        a=0
        for i in self.adj :
            a+= self.degre(i)
        return a
    
    def supprimer_arc(self,s1,s2):
        if self.arc(s1,s2):
            self.adj[s1].remove(s2)
        
def parcours_prof(g,vus,s):
    if s not in vus:
        vus.add(s)
        for v in g.voisins(s):
            parcours_prof(g,vus,v)

def parcours_largeur(g,a):
    dist={a:0}
    courant=[a]
    suivant=[]
    d=0
    while len(courant)!=0:
        d+=1
        for j in courant:
            b=courant.pop(j)
            for i in g.voisins(b) :
                if i not in dist :
                    dist[i]=d
                    suivant.append(i)
        courant,suivant=suivant,courant
    return dist

def reverseGraph(g) :
    new_d = {s : set() for s in g.adj}
    for s in g.adj :
        for v in g.voisins(s) :
            new_d[v].add(s)
    graph = GrapheD()
    graph.adj = new_d
    return graph

def degre_dico(g) :
    d = {}
    for s in g.adj :
        d[s] = len(g.voisins(s))
    return d


def marqueEtPropage(s, d, B, S1, attracteur, compteur):
    if s not in attracteur:
        attracteur[s] = compteur
        compteur += 1
        for y in B.adj[s]:
            d[y] -= 1
            if y in S1 or d[y] == 0:
                marqueEtPropage(y, d, B, S1, attracteur, compteur)

def calculeAttracteur(A, S1, V1):
    d = degre_dico(A)  # dictionnaire des degrés sortants du graphe A
    B = reverseGraph(A)  # graphe inverse de A
    attracteur = dict()
    for s in V1:
        marqueEtPropage(s, d, B, S1, attracteur, 0)
    return attracteur





