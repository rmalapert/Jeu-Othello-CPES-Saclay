import copy

class Plateau():
    def __init__(self):
        self.plateau = [[0] * 8 for i in range(8)]
        self.plateau[3][3] = 2
        self.plateau[4][4] = 2
        self.plateau[3][4] = 1
        self.plateau[4][3] = 1

        self.dico_dir = {"haut": (-1, 0),
                           "bas": (1, 0),
                           "gauche": (0, -1),
                           "droite": (0, 1),
                           "diag_hd": (-1, 1),
                           "diag_hg": (-1, -1),
                           "diag_bd": (1, 1),
                           "diag_bg": (1, -1)}

    def coup_valide(self, position, couleur):
        plateau = self.plateau
        lig, col = position
        dico_dir = self.dico_dir
        directions_possibles = []

        # case déjà occupée
        if plateau[lig][col] != 0:
            return []

        # 1 devient 2, 2 devient 1
        autre_couleur = 3 - couleur 

        for n_dir, (dx, dy) in dico_dir.items():
            x, y = lig + dx, col + dy
            traverse_adversaire = False

            while 0 <= x < 8 and 0 <= y < 8:
                if plateau[x][y] == autre_couleur:
                    traverse_adversaire = True
                elif plateau[x][y] == couleur:
                    if traverse_adversaire:
                        directions_possibles.append(n_dir)
                        break
                    # Si on trouve un pion de la même couleur sans
                    # en avoir trouvé un adversaire avant
                    else:
                        break
                # case vide
                else:
                    break
                x += dx
                y += dy

        return directions_possibles

    def coups_possibles(self, couleur):
        res = []
        for i in range(8):
            for j in range(8):
                if self.coup_valide((i, j), couleur):
                    res.append((i, j))
        return res
                
    def poser_pion(self, position, couleur, directions_possibles):
        lig, col = position
        self.plateau[lig][col] = couleur
        return 1 + self.retourner_pions(position, couleur, directions_possibles)

    def retourner_pions(self, position, couleur, directions_possibles):
        plateau = self.plateau
        dico_dir = self.dico_dir
        lig, col = position
        autre_couleur = 3 - couleur
        pts = 0
        
        for direction in directions_possibles:
            dx, dy = dico_dir[direction]
            x, y = lig + dx, col + dy
            while 0 <= x < 8 and 0 <= y < 8 \
                  and plateau[x][y] == autre_couleur:
                plateau[x][y] = couleur
                x += dx
                y += dy
                pts += 1
        return pts

    def copie_plateau(self):
        return [row[:] for row in self.plateau]

    def copie(self):
        new = Plateau()
        new.plateau = self.copie_plateau()
        return new
