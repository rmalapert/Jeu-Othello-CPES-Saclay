from class_plateau import *
import copy

def eval_plateau(plateau, couleur):
    opposant = 3 - couleur
    grille = plateau.plateau
    
    # Matrice de poids pour valoriser certaines positions du plateau (coins, bords, centre, etc.)
    poids = [[100, -20, 10, 5, 5, 10, -20, 100],
             [-20, -50, -2, -2, -2, -2, -50, -20],
             [10, -2, 5, 1, 1, 5, -2, 10],
             [5, -2, 1, 0, 0, 1, -2, 5],
             [5, -2, 1, 0, 0, 1, -2, 5],
             [10, -2, 5, 1, 1, 5, -2, 10],
             [-20, -50, -2, -2, -2, -2, -50, -20],
             [100, -20, 10, 5, 5, 10, -20, 100]]

    score_pos = 0

    # Parcourt la grille pour évaluer la position des pions et les compter
    for i in range(8):
        for j in range(8):
            if grille[i][j] == couleur:
                score_pos += poids[i][j]
            elif grille[i][j] == opposant:
                score_pos -= poids[i][j]
    # Calcul du score de mobilité : différence de coups possibles
    coups_joueur = len(plateau.coups_possibles(couleur))
    coups_ennemi = len(plateau.coups_possibles(opposant))
    if coups_joueur + coups_ennemi != 0:
        score_mobilite = 100 * (coups_joueur - coups_ennemi) / (coups_joueur + coups_ennemi)
    else:
        score_mobilite = 0

    # Score de parité : avantage si nombre de cases vides impair
    cases_vides = sum(ligne.count(0) for ligne in grille)
    score_parite = 5 if (cases_vides % 2 == 1) else 0

    # Score final pondéré
    return 2.5 * score_mobilite + 4.0 * score_pos + score_parite


def minimax_alpha_beta(plateau, couleur, profondeur, alpha, beta, maximisant):

    # Condition d'arrêt : profondeur atteinte ou plus de coups possibles
    if profondeur == 0 or not (plateau.coups_possibles(1) or plateau.coups_possibles(2)):
        return eval_plateau(plateau, couleur), None

    joueur_actuel = couleur if maximisant else 3 - couleur
    coups = plateau.coups_possibles(joueur_actuel)
    
    # Si aucun coup possible, passer le tour à l'adversaire
    if not coups:
        return minimax_alpha_beta(plateau, couleur, profondeur - 1, alpha, beta, not maximisant)

    meilleur_score = float('-inf') if maximisant else float('inf')
    meilleur_coup = None

    for pos in coups:
        directions = plateau.coup_valide(pos, joueur_actuel) # Directions de retournement valides
        copie = plateau.copie()
        copie.poser_pion(pos, joueur_actuel, directions)

        # Appel récursif pour explorer les coups suivants
        score, _ = minimax_alpha_beta(copie, couleur, profondeur - 1, alpha, beta, not maximisant)

        if maximisant:
            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = (pos, directions)
            alpha = max(alpha, score)
            if beta <= alpha:
                break  # Élagage
        else:
            if score < meilleur_score:
                meilleur_score = score
                meilleur_coup = (pos, directions)
            beta = min(beta, score)
            if beta <= alpha:
                break  # Élagage

    return meilleur_score, meilleur_coup


def ia_joue(plateau, couleur, profondeur=3):

    _, coup = minimax_alpha_beta(plateau, couleur, profondeur, float('-inf'), float('inf'), True)
    return coup
