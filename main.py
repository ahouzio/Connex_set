#!/usr/bin/env python3

"""
compute sizes of all connected components.
sort and display.
"""
from sys import argv
from geo.point import Point

def load_instance(filename):
    """
    loads .pts file.
    returns distance limit and points.
    """
    with open(filename, "r") as instance_file:
        lines = iter(instance_file)
        distance = float(next(lines))
        points = [Point([float(f) for f in l.split(",")]) for l in lines]

    return distance, points
def distance(point1, point2):
    diff = point1.coordinates[0]-point2.coordinates[0],point1.coordinates[1]-point2.coordinates[1]
    return (diff[0]**2 + diff[1]**2)**0.5

class connexe:
    """
    connexe est un carré qui contient des points qui appartient a la meme partie connexe
    """
    def __init__(self, contenu, passed, indice,size):

        self.contenu = contenu
        self.passed = passed
        self.indice = indice
        self.size = size
    def distance_to(self, other, distance_critique):
        """distance entre 2 rectangle(min des distance entre 2 pts qlq)"""
        for point1 in self.contenu:
            for point2 in other.contenu:
                d = distance(point1, point2)
                if d <= distance_critique :
                    return 1
        return 0
 

def print_components_sizes(distance_critique, points):
    """
    affichage des tailles triees de chaque composante
    """
    resultat = []
    if distance_critique == 0:
        for i in range(len(points)):
            resultat.append(1)
        print(resultat)
        return

    n = int((2**(0.5)/distance_critique))+1
    res_dict = {}
    
    
    """ On rempli les rectrangles avec les points de la liste """
    
    for point in points :
        indice_rect_i = int(point.coordinates[0]*(2**(0.5))/distance_critique)
        indice_rect_j = int(point.coordinates[1]*(2**(0.5))/distance_critique)
        if (indice_rect_i,indice_rect_j) not in res_dict.keys():
            connexe0 = connexe([point],0,(indice_rect_i,indice_rect_j),1)
            res_dict[(indice_rect_i,indice_rect_j)] = connexe0
            
        else:
            res_dict[(indice_rect_i,indice_rect_j)].contenu.append(point)
            res_dict[(indice_rect_i,indice_rect_j)].size += 1

   
    for key in res_dict.keys():
            i = key[0]
            j = key[1]
            if res_dict[(i,j)].passed == 1 :
                continue
            peres = [res_dict[(i,j)]]
            longueur = len(peres[0].contenu)
            while peres != []: #on recherche les voisins de tous les peres
                new_peres = []
                for pere in peres :
                    (p,q) = pere.indice
                    for a in range(-2,3):
                        for b in range(-2,3):
                            if 0<= p + a <= n-1 and 0<= q + b <= n-1 and (a != 0 or b != 0):
                                """Si c'est deja parcouru ou n'existe pas, on passe au suivant"""
                                if (p+a,q+b) not in res_dict.keys():
                                    continue
                                
                                if res_dict[(p+a,q+b)].passed == 1:
                                    continue
                                
                                # c nous dit si le voisin est proche de notre rectangle ou non
                                c = pere.distance_to(res_dict[(p+a,q+b)],distance_critique)
                                if c == 1: # Ils sont proches
                                    longueur += res_dict[(p+a,q+b)].size
                                    res_dict[(p+a,q+b)].size = 0
                                    new_peres.append(res_dict[(p+a,q+b)])
                                    
                                   
                    pere.passed = 1
                                                          
                peres = new_peres
                
            resultat.append(longueur)                                      
                   
    resultat.sort(reverse=True)
    print(resultat)                 

   
def main():
    """
    ne pas modifier: on charge une instance et on affiche les tailles
    """
    for instance in argv[1:]:
        distance, points = load_instance(instance)
        print_components_sizes(distance, points)
main()