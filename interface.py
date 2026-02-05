from time import *
import pygame
import traceback
from pygame.locals import *
from os import sys
from class_plateau import *
from strategie import *
from class_joueur import *


TAILLE_PLATEAU = 550
NB_CASES = 8
MARGE = 50
ESP_JOUEUR = 100
MENU = 300
TAILLE_FENETRE = TAILLE_PLATEAU + 2 * MARGE
TAILLE_CASE = TAILLE_PLATEAU // NB_CASES

BUTTON_JvsJ = pygame.Rect(TAILLE_FENETRE + 40, 100, 240, 50)
BUTTON_JvsIA = pygame.Rect(TAILLE_FENETRE + 40, 160, 240, 50)
BUTTON_IAvsIA = pygame.Rect(TAILLE_FENETRE + 40, 220, 240, 50)

BUTTON_DEBUTANT = pygame.Rect(TAILLE_FENETRE + 40, 320, 240, 50)
BUTTON_INTERMEDIAIRE = pygame.Rect(TAILLE_FENETRE + 40, 380, 240, 50)
BUTTON_EXPERT = pygame.Rect(TAILLE_FENETRE + 40, 440, 240, 50)

BUTTON_DEBUTANT2 = pygame.Rect(TAILLE_FENETRE + 40, 540, 240, 50)
BUTTON_INTERMEDIAIRE2 = pygame.Rect(TAILLE_FENETRE + 40, 600, 240, 50)
BUTTON_EXPERT2 = pygame.Rect(TAILLE_FENETRE + 40, 660, 240, 50)

BUTTON_QUITTER = pygame.Rect(TAILLE_FENETRE + 50, 370, 220, 50)
BUTTON_REJOUER = pygame.Rect(TAILLE_FENETRE + 50, 280, 220, 50)
BUTTON_REJOUER_partie = pygame.Rect(TAILLE_FENETRE + 90, 780, 140, 50)


def afficher_grille(fenetre):
    font = pygame.font.SysFont(None, 28)
    lettres = 'abcdefgh'
    chiffres = '12345678'

    # affiche le cadre du plateau
    rect =pygame.Rect(0, ESP_JOUEUR, TAILLE_FENETRE, TAILLE_FENETRE)
    pygame.draw.rect(fenetre, (91, 60, 17), rect, border_radius = 38)

    # affiche la grille
    for i in range(NB_CASES):
        for j in range(NB_CASES):
            x = MARGE + i * TAILLE_CASE
            y = ESP_JOUEUR + MARGE + j * TAILLE_CASE
            rect = pygame.Rect(x, y, TAILLE_CASE, TAILLE_CASE)
            pygame.draw.rect(fenetre, (0, 128, 0), rect)
            pygame.draw.rect(fenetre, (0, 0, 0), rect, width=1)
            
    # affiche les lettres dans la marge
    for i in range(NB_CASES):
        lettre = font.render(lettres[i], True, (255, 255, 255))
        x = MARGE + i * TAILLE_CASE + TAILLE_CASE // 2 - lettre.get_width() // 2
        y_haut = ESP_JOUEUR + MARGE // 2 - lettre.get_height() // 2
        y_bas = ESP_JOUEUR + TAILLE_FENETRE - MARGE // 2 - lettre.get_height() // 2
        fenetre.blit(lettre, (x, y_haut))
        fenetre.blit(lettre, (x, y_bas))
        
    # affiche les chiffres dans la marge
    for j in range(NB_CASES):
        chiffre = font.render(chiffres[j], True, (255, 255, 255))
        x_gauche = MARGE // 2 - chiffre.get_width() // 2
        x_droite = TAILLE_FENETRE - MARGE // 2 - chiffre.get_width() // 2
        y = ESP_JOUEUR + MARGE + j * TAILLE_CASE + TAILLE_CASE // 2 - chiffre.get_height() // 2
        fenetre.blit(chiffre, (x_gauche, y))
        fenetre.blit(chiffre, (x_droite, y))

        
def bouton_echange(fenetre):
    img_echange = pygame.image.load("images/echange.png").convert_alpha()
    image_reduite = pygame.transform.scale(img_echange,(50,50))
    
    fenetre.blit(image_reduite, (19, TAILLE_FENETRE - 25 + 3*ESP_JOUEUR//2))


def afficher_scores(fenetre, moi, adversaire):
    rect = pygame.Rect(10, 10, TAILLE_FENETRE-20, ESP_JOUEUR-20)
    pygame.draw.rect(fenetre, (155, 155, 155), rect, border_radius = 50)

    rect = pygame.Rect(10, TAILLE_FENETRE + ESP_JOUEUR + 10, TAILLE_FENETRE - 20, ESP_JOUEUR - 20)
    pygame.draw.rect(fenetre, (155, 155, 155), rect, border_radius = 50)
    
    font = pygame.font.SysFont("arial", 28, bold=True)
    if adversaire.est_ia():
        texte_adv = font.render(f"{adversaire.nom} - {adversaire.nom_niv} : {adversaire.score} points",
                                True, (255, 255, 255) if moi.couleur == 1 else (0, 0, 0))
    else:
        texte_adv = font.render(f"{adversaire.nom}  : {adversaire.score} points", True, (255, 255, 255) if moi.couleur == 1 else (0, 0, 0))
    if moi.est_ia():
        texte_moi = font.render(f"{moi.nom} - {moi.nom_niv} : {moi.score} points",
                                True, (255, 255, 255) if moi.couleur == 2 else (0, 0, 0))
    else:
        texte_moi = font.render(f"{moi.nom} : {moi.score} points", True, (255, 255, 255) if moi.couleur == 2 else (0, 0, 0))

    fenetre.blit(texte_adv, (1.5*MARGE, ESP_JOUEUR // 2 - 20))
    fenetre.blit(texte_moi, (1.5*MARGE, TAILLE_FENETRE + 3*ESP_JOUEUR//2 - 20))
    bouton_echange(fenetre)


def afficher_pions(fenetre, plateau):
    for i in range(8):
        for j in range(8):
            centre_x = MARGE + j * TAILLE_CASE + TAILLE_CASE // 2
            centre_y = MARGE + i * TAILLE_CASE + TAILLE_CASE // 2 + ESP_JOUEUR
            if plateau.plateau[i][j] == 1:
                pygame.draw.circle(fenetre, "black", (centre_x, centre_y), TAILLE_CASE // 2 - 5)
            elif plateau.plateau[i][j] == 2:
                pygame.draw.circle(fenetre, "white", (centre_x, centre_y), TAILLE_CASE // 2 - 5)


def afficher_coups_possibles(fenetre, plateau, joueur):
    couleur = joueur.couleur
    t = plateau.coups_possibles(couleur)
    for pos in t:
        i, j = pos
        centre_x = MARGE + j * TAILLE_CASE + TAILLE_CASE // 2
        centre_y = MARGE + i * TAILLE_CASE + TAILLE_CASE // 2 + ESP_JOUEUR
        if couleur == 1:
            pygame.draw.circle(fenetre, "black", (centre_x, centre_y), TAILLE_CASE // 4, width = 3)
        elif couleur == 2:
            pygame.draw.circle(fenetre, "white", (centre_x, centre_y), TAILLE_CASE // 4, width = 3)


def dessiner_bouton(fenetre, rect, texte, actif, font=None):
    if font is None:
        font = pygame.font.Font(None, 36)
    couleur = (20, 99, 50) if actif else (9, 141, 67)
    texte_couleur = (128, 128, 128) if actif else (0, 0, 0)

    pygame.draw.rect(fenetre, couleur, rect)
    rendu_texte = font.render(texte, True, texte_couleur)
    fenetre.blit(rendu_texte, (rect.x + 13, rect.y + 12))


def afficher_boutons(fenetre, jvsj, jvsia, iavsia):
    boutons = [("Joueur VS Joueur", BUTTON_JvsJ, jvsj),
               ("Joueur VS IA", BUTTON_JvsIA, jvsia),
               ("IA VS IA", BUTTON_IAvsIA, iavsia)]

    for nom, rect, actif in boutons:
        dessiner_bouton(fenetre, rect, nom, actif)

def dessiner_etoiles(surface, x, y, n, taille=15):
    for i in range(n):
        pygame.draw.polygon(surface, (255, 215, 0),
                            [(x + i*25 + taille//2, y),
                             (x + i*25 + taille, y + taille),
                             (x + i*25, y + taille//2),
                             (x + i*25 + taille, y + taille//2),
                             (x + i*25, y + taille)])


def dessiner_bouton_difficulte(fenetre, font, nom, rect, actif, etoiles):
    couleur = (20, 99, 50) if actif else (9, 141, 67)
    pygame.draw.rect(fenetre, couleur, rect)
    text = font.render(nom, True, (0, 0, 0))
    fenetre.blit(text, (rect.x + 10, rect.y + 15))
    x_etoile = -25 * etoiles + 225  # f(x) = -25x + 225
    dessiner_etoiles(fenetre, rect.x + x_etoile, rect.y + 18, etoiles)


def afficher_boutons_difficulte(fenetre, deb, inte, av, iavsia=0, deb2=0, inte2=0, av2=0):
    font = pygame.font.Font(None, 28)

    if iavsia:
        dessiner_bouton_difficulte(fenetre, font, "Débutant", BUTTON_DEBUTANT2, deb2, 1)
        dessiner_bouton_difficulte(fenetre, font, "Intermédiaire", BUTTON_INTERMEDIAIRE2, inte2, 3)
        dessiner_bouton_difficulte(fenetre, font, "Avancé", BUTTON_EXPERT2, av2, 5)

    dessiner_bouton_difficulte(fenetre, font, "Débutant", BUTTON_DEBUTANT, deb, 1)
    dessiner_bouton_difficulte(fenetre, font, "Intermédiaire", BUTTON_INTERMEDIAIRE, inte, 3)
    dessiner_bouton_difficulte(fenetre, font, "Avancé", BUTTON_EXPERT, av, 5)

def afficher_bouton_menu(fenetre):
    font = pygame.font.Font(None, 36)
    texte = font.render("REJOUER", True, (0, 0, 0))

    pygame.draw.rect(fenetre, (200, 50, 50), BUTTON_REJOUER_partie)
    fenetre.blit(texte, (BUTTON_REJOUER_partie.x + 13, BUTTON_REJOUER_partie.y + 12))


def afficher_menu_mode_de_jeu(fenetre, jvsj=0, jvsia=0, iavsia=0, deb=0, inte=0, av=0, deb2=0, inte2=0, av2=0):
    rect = pygame.Rect(TAILLE_FENETRE + 20, 10, TAILLE_FENETRE+MENU+20, TAILLE_FENETRE + 2*ESP_JOUEUR - 20)
    pygame.draw.rect(fenetre, (155, 155, 155), rect, border_radius = 50)
    font = pygame.font.SysFont("comic sans ms", 40, bold =True)
    text = font.render("Mode de jeu", True, (0, 0, 0))
    fenetre.blit(text, (TAILLE_FENETRE +40, 30))
    afficher_boutons(fenetre, jvsj, jvsia, iavsia)
    
    pause_button = pygame.image.load("images/pause_debut.png").convert_alpha()
    pause_reduit = pygame.transform.scale(pause_button,(TAILLE_CASE*2, TAILLE_CASE*2))
    fenetre.blit(pause_reduit,(255, 355))

    if jvsia:
        font = pygame.font.SysFont("comic sans ms", 20)
        text = font.render("Niveau de l'IA", True, (0, 0, 0))
        fenetre.blit(text, (TAILLE_FENETRE + 40, BUTTON_DEBUTANT.y - 35))
        afficher_boutons_difficulte(fenetre, deb, inte, av, iavsia)
        
    if iavsia:
        font = pygame.font.SysFont("comic sans ms", 20)
        text = font.render("Niveau de l'IA 1 (noir)", True, (0, 0, 0))
        fenetre.blit(text, (TAILLE_FENETRE + 40, BUTTON_DEBUTANT.y - 35))

        font = pygame.font.SysFont("comic sans ms", 20)
        text = font.render("Niveau de l'IA 2 (blanc)", True, (0, 0, 0))
        fenetre.blit(text, (TAILLE_FENETRE + 40, BUTTON_DEBUTANT2.y - 35))
        afficher_boutons_difficulte(fenetre, deb, inte, av, iavsia, deb2, inte2, av2)
    

def afficher_menu_fin(fenetre, joueur):
    pygame.display.set_caption("Menu de fin")
    pygame.draw.rect(fenetre, (0, 0, 0), pygame.Rect(TAILLE_FENETRE, 0, TAILLE_FENETRE + MENU, 1000))#TAILLE_FENETRE + 2 * ESP_JOUEUR

    font = pygame.font.SysFont("arial black", 26, bold = False, italic=False) 
    if joueur is None:
        texte = font.render("Egalité !", 1, (255, 255, 255))
    else:
        texte = font.render(f"{joueur.nom} a gagné !", 1, (255, 255, 255))

    texte_width = texte.get_width()
    texte_height = texte.get_height()

    x_pos = TAILLE_FENETRE + (MENU - texte_width) // 2
    y_pos = 150

    fenetre.blit(texte, (x_pos, y_pos))
    
    pygame.draw.rect(fenetre, (255, 0, 0), BUTTON_QUITTER)
    font = pygame.font.Font(None, 36)
    text = font.render('Quitter', True, (255, 255, 255))
    fenetre.blit(text, (BUTTON_QUITTER.x + 65, BUTTON_QUITTER.y + 12))

    couleur = (50, 230, 50)
    pygame.draw.rect(fenetre, (50, 230, 50), BUTTON_REJOUER)
    font = pygame.font.Font(None, 36)
    text = font.render('Rejouer', True, (255, 255, 255))
    fenetre.blit(text, (BUTTON_REJOUER.x + 65, BUTTON_REJOUER.y + 12))


def joueur_suivant(joueur, joueur1, joueur2):
    return joueur1 if joueur is joueur2 else joueur2

def maj_tour(joueur, joueur1, joueur2, plateau, position, directions):
    if joueur.est_ia():
        pts, pos, dirs = joueur.jouer_coup(plateau)
        if pos:
            joueur.score += pts
            joueur = joueur_suivant(joueur, joueur1, joueur2)
            joueur.score -= (pts - 1)
    else:
        pts = joueur.jouer_coup(plateau, position, directions)
        joueur.score += pts
        joueur = joueur1 if joueur is joueur2 else joueur2
        joueur.score -= (pts - 1)
    return joueur

def choix_mode(fenetre, plateau):
    jvsj = True
    jvsia = False
    iavsia = False

    deb = False
    inte = True
    av = False
    deb2 = False
    inte2 = True
    av2 = False 
    difficulte = 3
    difficulte2 = 3

    joueur1 = Joueur(1, "Joueur 1")
    joueur2 = Joueur(2, "Joueur 2")
    joueur=joueur1
    compte_boucle = 0
    continuer = True

    afficher_grille(fenetre)
    afficher_pions(fenetre, plateau)
    afficher_scores(fenetre, joueur1, joueur2)
    pygame.display.flip()
    while continuer:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                position_clic = event.pos
                x, y = position_clic
                #print(x, y)
                if 255 <= x <= 390 and 355 <= y <= 490:
                    continuer = False
                    continue
                if 27 <= x <= 65 and 780 <= y <= 817:
                    #print("echange")
                    joueur1.couleur, joueur2.couleur = joueur2.couleur, joueur1.couleur

                if BUTTON_JvsJ.collidepoint(event.pos):
                    jvsj = not jvsj 
                    jvsia = False
                    iavsia = False
                    
                elif BUTTON_JvsIA.collidepoint(event.pos):
                    jvsj = False
                    jvsia = not jvsia
                    iavsia = False
                    
                elif BUTTON_IAvsIA.collidepoint(event.pos):
                    jvsj = False
                    jvsia = False
                    iavsia = not iavsia

                if jvsia:
                    if BUTTON_DEBUTANT.collidepoint(event.pos):
                        deb = not deb
                        inte = False
                        av = False
                        difficulte = 1 if deb else 0
                        
                    elif BUTTON_INTERMEDIAIRE.collidepoint(event.pos):
                        deb = False
                        inte = not inte
                        av = False
                        difficulte = 3 if inte else 0
                    elif BUTTON_EXPERT.collidepoint(event.pos):
                        deb = False
                        inte = False
                        av = not av
                        difficulte = 5 if av else 0

                elif iavsia:
                    if BUTTON_DEBUTANT.collidepoint(event.pos):
                        deb = not deb
                        inte = False
                        av = False
                        difficulte = 1 if deb else 0
                        
                    elif BUTTON_INTERMEDIAIRE.collidepoint(event.pos):
                        deb = False
                        inte = not inte
                        av = False
                        difficulte = 3 if inte else 0
                        
                    elif BUTTON_EXPERT.collidepoint(event.pos):
                        deb = False
                        inte = False
                        av = not av
                        difficulte = 5 if av else 0

                    if BUTTON_DEBUTANT2.collidepoint(event.pos):
                        deb2 = not deb2
                        inte2 = False
                        av2 = False
                        difficulte2 = 1 if deb2 else 0
                        
                    elif BUTTON_INTERMEDIAIRE2.collidepoint(event.pos):
                        deb2 = False
                        inte2 = not inte2
                        av2 = False
                        difficulte2 = 3 if inte2 else 0
                        
                    elif BUTTON_EXPERT2.collidepoint(event.pos):
                        deb2 = False
                        inte2 = False
                        av2 = not av2
                        difficulte2 = 5 if av2 else 0

                if jvsj:
                    joueur1 = Joueur(joueur1.couleur, "Joueur 1")
                    joueur2 = Joueur(joueur2.couleur, "Joueur 2")
                elif jvsia:
                    joueur1 = Joueur(joueur1.couleur, "Joueur 1")
                    joueur2 = JoueurIA(joueur2.couleur, "IA", niveau=difficulte)
                elif iavsia:
                    joueur1 = JoueurIA(joueur1.couleur, "IA 1", niveau=difficulte)
                    joueur2 = JoueurIA(joueur2.couleur, "IA 2", niveau=difficulte2)
                joueur = joueur1 if joueur1.couleur == 1 else joueur2
                afficher_scores(fenetre, joueur1, joueur2)                        

            elif event.type == QUIT:
                continuer = False
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continuer = False
                    pygame.quit()
                    sys.exit()
    
        afficher_menu_mode_de_jeu(fenetre, jvsj, jvsia, iavsia, deb, inte, av, deb2, inte2, av2)
        afficher_bouton_menu(fenetre)
        pygame.display.flip()
    afficher_coups_possibles(fenetre, plateau, joueur)
    pygame.display.flip()
    if iavsia:
        ia_diff = [[deb, inte, av, difficulte],
               [deb2, inte2, av2, difficulte2]]
    elif jvsia:
        ia_diff = [deb, inte, av, difficulte]
    else:
        ia_diff = [None, None]
    return joueur, joueur1, joueur2, jvsj, jvsia, iavsia, ia_diff

        

def interface():
    pygame.init()
    try:
        fenetre = pygame.display.set_mode((TAILLE_FENETRE + MENU, TAILLE_FENETRE + 2*ESP_JOUEUR))
        fenetre.fill((0, 0, 0))
        pygame.display.set_caption("Othello")

        continuer = True
        help_affiche = True

        plateau = Plateau()
        joueur, joueur1, joueur2, jvsj, jvsia, iavsia, ia_diff = choix_mode(fenetre, plateau)
##        print("joueur", joueur)
##        print("joueur1", joueur1)
##        print("joueur2", joueur2)
##        print("jvj", jvsj)
##        print("jvia", jvsia)
##        print("iavsia", iavsia)
##        print("ia_difficulté", ia_diff)
        if iavsia:
            t1, t2 = ia_diff
            deb, inte, av, difficulte = t1
            deb2, inte2, av2, difficulte2 = t2
            
        elif jvsia:
            deb, inte, av, difficulte = ia_diff
        #else:
        

        afficher_grille(fenetre)
        afficher_pions(fenetre, plateau)
        afficher_coups_possibles(fenetre, plateau, joueur)
        afficher_scores(fenetre, joueur1, joueur2)
        afficher_menu_mode_de_jeu(fenetre)
        afficher_bouton_menu(fenetre)
        pygame.display.flip()


        while continuer:
            fini = not (plateau.coups_possibles(joueur1.couleur) or plateau.coups_possibles(joueur2.couleur))
            if fini:
                if joueur1.score > joueur2.score:
                    gagnant = joueur1
                elif joueur2.score > joueur1.score:
                    gagnant = joueur2
                else:
                    gagnant = None
                
                afficher_menu_fin(fenetre, gagnant)

            else:
                if not plateau.coups_possibles(joueur.couleur):
                    print(f"Le joueur {joueur.couleur} ne peut pas jouer, passe son tour.")
                    joueur = joueur_suivant(joueur, joueur1, joueur2)
                    continue
                if jvsia:
                    if joueur.est_ia():
                        # fonction du fichier stratégie
                        coup = ia_joue(plateau, joueur.couleur, profondeur=difficulte)
                        #print("coup", coup)
                        if coup:
                            position, directions = coup
                            joueur =  maj_tour(joueur, joueur1, joueur2, plateau, position, directions)
                        pygame.time.delay(300-50*difficulte)

                elif iavsia:
                    pygame.time.delay(50)
                    niveau = difficulte if joueur is joueur1 else difficulte2
                    # fonction du fichier stratégie
                    coup = ia_joue(plateau, joueur.couleur, profondeur=niveau)
                    if coup:
                        position, directions = coup
                        joueur = maj_tour(joueur, joueur1, joueur2, plateau, position, directions)

                    else:
                        joueur = joueur_suivant(joueur, joueur1, joueur2)
                    pygame.time.delay(300-50*difficulte)

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    if fini:
                        if BUTTON_QUITTER.collidepoint(event.pos):
                            pygame.quit()
                            sys.exit()

                        if BUTTON_REJOUER.collidepoint(event.pos):
                            fenetre.fill((0, 0, 0))
                            compte_boucle = 0
                            continuer = True
                            plateau = Plateau()
                            joueur, joueur1, joueur2, jvsj, jvsia, iavsia, ia_diff = choix_mode(fenetre, plateau)
                            
                            if iavsia:
                                t1, t2 = ia_diff
                                deb, inte, av, difficulte = t1
                                deb2, inte2, av2, difficulte2 = t2
                                
                            elif jvsia:
                                deb, inte, av, difficulte = ia_diff

                            afficher_grille(fenetre)
                            afficher_pions(fenetre, plateau)
                            afficher_coups_possibles(fenetre, plateau, joueur)
                            afficher_scores(fenetre, joueur1, joueur2)
                            afficher_menu_mode_de_jeu(fenetre)
                            afficher_bouton_menu(fenetre)
                            pygame.display.flip()
                            
                    else:
                        if BUTTON_REJOUER_partie.collidepoint(event.pos):
                            fenetre.fill((0, 0, 0))
                            compte_boucle = 0
                            continuer = True
                            plateau = Plateau()
                            joueur, joueur1, joueur2, jvsj, jvsia, iavsia, ia_diff = choix_mode(fenetre, plateau)

                            if iavsia:
                                t1, t2 = ia_diff
                                deb, inte, av, difficulte = t1
                                deb2, inte2, av2, difficulte2 = t2
                                
                            elif jvsia:
                                deb, inte, av, difficulte = ia_diff

                            afficher_grille(fenetre)
                            afficher_pions(fenetre, plateau)
                            afficher_coups_possibles(fenetre, plateau, joueur)
                            afficher_scores(fenetre, joueur1, joueur2)
                            afficher_menu_mode_de_jeu(fenetre)
                            afficher_bouton_menu(fenetre)
                            pygame.display.flip()
                        
                        if not joueur.est_ia():
                            position_clic = event.pos
                            x, y = position_clic
                            if MARGE <= x < MARGE + TAILLE_PLATEAU and MARGE <= y < MARGE + ESP_JOUEUR + TAILLE_PLATEAU:
                                col = (x - MARGE) // TAILLE_CASE
                                lig = (y - MARGE - ESP_JOUEUR) // TAILLE_CASE
                                directions_possibles = plateau.coup_valide((lig, col), joueur.couleur)
                                if directions_possibles:
                                    position = (lig, col)
                                    joueur = maj_tour(joueur, joueur1, joueur2, plateau, position, directions_possibles)

                            

                elif event.type == QUIT:
                    continuer = False

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        continuer = False
                    elif event.key == K_h:
                        help_affiche = not help_affiche

            afficher_grille(fenetre)
            afficher_scores(fenetre, joueur1, joueur2)
            afficher_pions(fenetre, plateau)
            if help_affiche:
                afficher_coups_possibles(fenetre, plateau, joueur)
            pygame.display.flip()

    except:
        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit()





