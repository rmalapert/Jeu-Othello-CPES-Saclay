Othello – Jeu en Python avec Interface Pygame
Ce projet est une implémentation du jeu à deux joueurs Othello (ou Reversi) en Python, avec une interface graphique développée à l’aide de Pygame. Il propose plusieurs modes de jeu : joueur contre joueur, joueur contre IA, et IA contre IA.

Objectif :
Avoir plus de pions de ta couleur (noir ou blanc) que ton adversaire à la fin de la partie.

Déroulement du jeu :
Le jeu se joue sur un plateau 8x8.
Au départ, 4 pions sont placés au centre (2 noirs, 2 blancs en diagonale).
Les joueurs jouent à tour de rôle.

Règle pour poser un pion :
Tu dois poser ton pion de manière à encercler un ou plusieurs pions adverses entre ton nouveau pion et un autre de tes pions déjà en place.
Tous les pions adverses ainsi encerclés sont retournés à ta couleur.
Si aucun coup n’est possible, tu passes ton tour.
La partie se termine quand aucun joueur ne peut jouer.

Fonctionnalités:
 - Plateau de jeu 8x8 avec affichage graphique complet
 - Interface interactive avec Pygame
 - 3 modes de jeu :
     ¤ Joueur vs Joueur
     ¤ Joueur vs IA (niveau Débutant / Intermédiaire / Avancé)
     ¤ IA vs IA
 - Affichage des coups possibles par défaut (appuyer sur h pour les enlever/afficher)
 - Représentation visuelle du score en direct
 - Changer de couleur (appuyer sur le bouton à gauche de votre nom)
 - Possibilité de rejouer la partie avant de la finir (bouton rejouer)
 - Possibilité de rejouer la partie avant de la finir (appuyer sur echap)
 - Menu de fin pour quitter ou rejour


Intelligence Artificielle
L’IA peut jouer avec 3 niveaux de difficulté, grâce à des stratégies définies dans le fichier strategie.py:
 - Débutant : IA simple (1 coup en profondeur)
 - Intermédiaire : IA avec meilleure évaluation (3 coups en profondeur)
 - Avancé : IA plus stratégique (5 coups en profondeur)
Une IA de niveau Avancé gagnera toujours contre des IA de niveau plus faible (Intermédiaire et Débutant), de même qu'une IA de niveau Intermédiaire gagnera toujours contre une IA de niveau Débutant.

Lancer le jeu
Assurez-vous d’avoir Python 3.x et Pygame installés
pip install pygame

Puis exécutez le jeu en appuyant sur F5 dans le fichier main.py ou en exécutant cette ligne dans le bash :
python main.py