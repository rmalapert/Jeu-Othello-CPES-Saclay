from class_plateau import *
from strategie import *


class Joueur:
    def __init__(self, couleur, nom, score=2):
        self.couleur = couleur
        self.nom = nom
        self.score = score

    def __str__(self):
        return f"couleur : {self.couleur}, nom : {self.nom}, score : {self.score}"

    def jouer_coup(self, plateau, position, directions_possibles):
        return plateau.poser_pion(position, self.couleur, directions_possibles)

    def est_ia(self):
        return False

class JoueurIA(Joueur):
    def __init__(self, couleur, nom, niveau=3, score=2):
        super().__init__(couleur, nom, score)
        self.niveau = niveau
        self.nom_niv = "Débutant" if niveau == 1 else\
                       "Intermédiaire" if niveau == 3 else\
                       "Avancé" if niveau == 5 else "Inconnu"

    def __str__(self):
        return super().__str__()

    def jouer_coup(self, plateau):
        coup = ia_joue(plateau, self.couleur, self.niveau)
        if coup:
            position, directions_possibles = coup
            pts = plateau.poser_pion(position, self.couleur, directions_possibles)
            return pts, position, directions_possibles
        else:
            return 0, None, None

    def est_ia(self):
        return True

