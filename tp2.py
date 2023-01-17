# Auteurs :
# Lilou Blanchette (20188851)
# Julien Thibeault (B0610)

# Date : 20 décembre 2020

# But du programme: Recréer le jeu du nom "addiction solitaire".

"""
Description du programme : 

    Le but de ce programme est de créer un tableau où sont disposés
    les 52 cartes d'un paquet de cartes standard (ou les as ne sont
    représentés que par des espaces vides) aléatoirement. Le but de
    ce jeu est de déplacer les cartes une à la fois pour finir par
    avoir, sur chacune des rangées, les cartes du 2 au roi d'une
    même sorte, en séquence.

    Le programme permet de déplacer des cartes 2 seulement lorsqu'il
    y a une case vide située au début d'une des rangées. 

    Le joueur peut déplacer les autres cartes lorsqu'il y a une case
    vide à droite de leur antécédent de même sorte. Lorsque le joueur
    clique sur une carte active, elle est déplacée à la place du vide
    correspondant, laissant ainsi son ancienne position vacante. Cela
    permet alors de nouveaux déplacements.

    Toutes les cartes qui ont une possibilité de mouvement sont dites
    actives et sont marquées d'une couleur verte.

    Lorsqu'une case vide est située à droite d'un roi, il ne sera pas
    possible de déplacer une carte vers cette case. Les rois n'ont aucun
    successeur possible dans ce jeu; ils terminent les séquences.

    Si 2 cases vides sont situées l'une à côté de l'autre, seulement
    celle qui se trouve à gauche pourra recevoir une carte. La cases
    de droite n'a aucun prédécesseur valide.

    Lorsque le joueur n'a plus aucune possibilité de mouvement, ou bien
    lorsque le joueur le souhaite, le programme permet de rebrasser
    toutes les cartes qui ne sont pas déjà dans la bonne position. Ainsi,
    les possibilités de mouvements du jeu seront renouvelées. Le joueur
    peut brasser les cartes jusqu'à 3 fois durant une partie.

    Le joueur peut aussi, à tout moment, créer une nouvelle partie.

    Le joueur est déclaré vainqueur lorsqu'il réussit à placer toutes
    les cartes en séquence sur les 4 rangées selon leurs sortes.
    Le joueur est déclaré vaincu lorsqu'il ne réussit pas à réaliser
    l'ordonnancement des cartes après 3 brassages et qu'il n'y a plus
    de mouvement possible sur le plateau de jeu.
"""



##### Déclaration des variables #####


# La variable "cartes" représente des cartes sous un format numérique
# ordonné. Des As aux Rois, puis du pique au coeur, au carreau, au trèfle.

cartes = list(range(0,52))

# Le plateau de jeu est mémorisé sous forme de liste.

plateauJeu = [None] * 52

# Longeur du tableau de jeu.

lenPlateau = len(plateauJeu)

# Nombre de rangées dans le jeu.

nbRangees = 4

# Nombre de colonnes dans le jeu.

nbColonnes = 13

# Tableau des valeurs pour chacune des cases qui 
# représentent le début d'une rangée.

debutRangee = [0,13,26,39]

# Tableau des valeurs qui représentent les As (cases vides).

cartesEmpty = [0,1,2,3] 

# Tableau des valeurs qui représente les cartes de valeur 2.

cartesDeux = [4,5,6,7]  

# Les cases activés (avec style) sont gardées en mémoire dans une liste.

casesActives = [] # cartes en surbrillance
casesVides = [] # cartes masquées

# Nombre de brassages restant.

brassesRestantes = 3

# Référence pour les fichiers SVG, l'index est la valeur de 0 a 51 du paquet.

refSVG = [  "empty","empty","empty","empty",  
            "2C","2D","2H","2S",
            "3C","3D","3H","3S",
            "4C","4D","4H","4S",
            "5C","5D","5H","5S",
            "6C","6D","6H","6S",
            "7C","7D","7H","7S",
            "8C","8D","8H","8S",
            "9C","9D","9H","9S",
            "10C","10D","10H","10S",
            "JC","JD","JH","JS",
            "QC","QD","QH","QS",
            "KC","KD","KH","KS",
            ]

# Représente les cartes en main.

cartesAPlacer = cartes.copy()



##### Definition des fonctions #####


def init():
    main = document.querySelector("#main")
    main.innerHTML = """
    <style>
        #main table { float: none; }
        #main table td { border: 0; padding: 1px 2px; height: auto; }
        #main table td img { height: auto; }
    </style>
    <div>
        <table id="jeu">
        </table>
    </div>
    <br>
    <div>
        <p id="brassesMessage">
            <span id="vousPouvez">Vous pouvez encore </span>
            <span id="vousDevez" style="display:none">Vous devez </span>
            <button onclick="rebrasser()">Brasser les cartes</button>
            <span id="brassesRestantes"> 3 fois</span>
        </p>

        <p id="aucuneBrasse" style="display:none">
            <span>Vous ne pouvez plus brasser les cartes</span>
        </p>

        <p id="defaite" style="display:none">
            <span >Vous avez perdu! Vous pouvez rejouer.</span>
        </p>

        <p id="victoire" style="display:none">
            <span>Vous avez gagné! Vous pouvez rejouer.</span>
        </p>

        <button onclick="nouvellePartie()">Nouvelle partie</button>
    </div>
    """

    nouvellePartie()


# La fonction nouvellePartie ne prend aucun paramètre et permet
# l'affichage du jeu initial ou lorsqu'une nouvelle partie est
# lancée. Elle permet donc le placement aléatoire des cartes et
# identifie les cartes qui peuvent être déplacées grâce aux fonctions
# melangerCartes, placeCartes et activeCartes.

def nouvellePartie():

    # Réinitialisation du plateau de jeu.

    for i in range(lenPlateau):
        plateauJeu[i] = None
    
    # Réinitialisation des brasses restantes.

    global brassesRestantes
    brassesRestantes = 3
    document.querySelector('#brassesRestantes') \
            .innerHTML = " " + str(brassesRestantes) + " fois"
    document.querySelector('#brassesMessage') \
            .setAttribute("style","display:block")
    document.querySelector('#aucuneBrasse') \
            .setAttribute("style", "display:none")

    # Reprendre toutes les cartes en main (52).

    global cartesAPlacer
    cartesAPlacer = cartes.copy()

    # Mélanger le paquet complet.

    melangerCartes(cartesAPlacer)

    # Mettre en place le plateau de Jeu.

    placerCartes(cartesAPlacer)

    # Afficher le plateau de Jeu - injection du code HTML.

    document.querySelector('#jeu').innerHTML = addictionSolitaireHTML()

    # Identifie les cartes qui peuvent être jouées.

    activeCartes()


# La fonction melangerCartes prend en paramètre un liste et mélange
# celle-ci de façon équiprobable.

def melangerCartes(liste):
    for i in range(len(liste)-1, 1, -1):
        indexRandom = math.floor(random()*i)
        temp = liste[i]
        liste[i] = liste[indexRandom]
        liste[indexRandom] = temp


# La fonction placerCartes prend en paramètre une liste et place
# chacune des cartes qui s'y retrouvent sur le plateau de jeu.

def placerCartes(liste):
    for i in range(lenPlateau):
        if plateauJeu[i] == None:
            plateauJeu[i] = cartesAPlacer.pop()


# La fonction rebrasser ne prend aucun paramètre.
# Elle place et mélange chacune des cartes qui ne font pas
# partie d'une suite débutant une rangée. La fonction rebrasser
# indique aussi au joueur le nombre de brasses restantes.

def rebrasser():
    global brassesRestantes

    reprendreCartes()
    melangerCartes(cartesAPlacer)
    placerCartes(cartesAPlacer)
    document.querySelector('#jeu').innerHTML = addictionSolitaireHTML()
    
    brassesRestantes -= 1

    # Rétablir l'affichage des bonnes balises HTML.

    document.querySelector('#vousDevez') \
            .setAttribute("style", "display:none")
    document.querySelector('#vousPouvez').removeAttribute("style")
    document.querySelector('#brassesRestantes').removeAttribute("style")

    # Permets d'indiquer combien de brassages il reste au joueur.

    if brassesRestantes > 0 :
        document.querySelector('#brassesRestantes').innerHTML = \
                                " " + str(brassesRestantes) + " fois"
    else : 
        document.querySelector('#brassesMessage') \
                .setAttribute("style", "display:none")
        document.querySelector('#aucuneBrasse') \
                .setAttribute("style", "display:block")
    
    activeCartes()


# La fonction reprendreCartes ne prend aucun paramètre.
# Elle retire du plateau de jeu, pour reprendre en main les cartes
# qui ne participe pas à une suite valide qui débute une rangée.

def reprendreCartes():

    # Itération sur chaque rangée.
    
    for i in debutRangee:

        # Indique à quel index nous sommes rendus.

        index = i
 
        # Permet d'indiquer la dernière valeur de la rangée.

        finRangee = i + 13

        # Indique si la rangée possède une série.

        serie = True
        
        # Valide si la première case a une carte de valeur 2 et
        # donc s'il y a une série sur cette rangée.

        if plateauJeu[i] not in cartesDeux :
            serie = False 
        else :   

            # Passer à la 2e case.

            index += 1

        # Vérifie la succession des cases suivantes.

        while (serie and index < finRangee):
            if (plateauJeu[index] == plateauJeu[index-1]+4):
                index += 1
            else :
                serie = False
                
        # Retire les cartes non ordonnées.

        for j in range(index,finRangee):
            cartesAPlacer.append(plateauJeu[j])
            plateauJeu[j] = None
    

# La fonction activeCartes ne prend aucun paramètre.
# Elle identifie les cartes pouvant être jouées,
# en fonction de l'emplacement des as (cartes vides) et des rois.

def activeCartes():

    # Retire l'identification des cartes déjà activées.

    global casesActives

    # Retire le style déjà présent sur les cartes.

    for i in range(lenPlateau):
        elem(i).removeAttribute('style') 

    # Réinitialise la variable de suivi.

    casesActives = []
    
    # Trouver la position des cases vides (les As).

    global casesVides
    casesVides = []
    for i in cartesEmpty:
        casesVides.append(plateauJeu.index(i))

    # Trouver les cartes qui peuvent être jouées.

    cartesAActiver = []
    for i in casesVides:

        # Une case vide en début de rangée active toutes les cartes 2.

        if i in debutRangee:
            
            cartesAActiver.extend([4,5,6,7])

        # Aucune carte ne peut suivre un roi.

        elif plateauJeu[i-1] >= 48 :           

            continue

        # Aucune carte ne peut être placée après une case vide.

        elif plateauJeu[i-1] in cartesEmpty:

            continue

       # Ajoute la carte qui respecte toutes ces conditions
       # et peu donc être activées.

        else :           

            cartesAActiver.append(plateauJeu[i-1] + 4)

    # Trouver l'index des cartes qui peuvent être jouées.

    for i in cartesAActiver:
        casesActives.append(plateauJeu.index(i))
    
    # Identifie les cartes activées.

    for i in casesActives:
        elem(i).setAttribute('style', 'background-color: lime')


### ATTENTION ###
# deplacerCarte doit servir seulement si l'index est valide.
# La carte doit faire partie de la liste cartesActives.

# La fonction deplacerCarte prend en paramètre un entier positif, 
# qui représente l'index de la carte cliqué et permet de déplacer
# celle-ci si elle respecte les diverses contraintes de déplacement
# d'une carte et ajoute elle-ci au tableau contenant les informations
# sur les cartes activées.

def deplacerCarte(index):
    valeurCarte = plateauJeu[index]

    # Valeur pour fin de comparaison.

    indexDestination = 52  
    print('valeurCarte = ' + str(valeurCarte))

    # Si on déplace une carte de valeur 2.

    if valeurCarte in cartesDeux :
        for i in casesVides :

            # Attribuer la première case vide en début de rangée.

            if (i in debutRangee) and (i < indexDestination) :
                indexDestination = i
                
    # Sinon, vérifier la valeur des cartes qui précèdent les cases vides.

    else :
        for i in casesVides :

            # Cas où la rangée débute par une case vide.

            if i in debutRangee :
                continue
            else :
                if (plateauJeu[i-1] + 4) == valeurCarte :
                    indexDestination = i
                    break
    
    # Effectuer le déplacement de la carte.

    temp = plateauJeu[indexDestination]
    plateauJeu[indexDestination] = plateauJeu[index]
    plateauJeu[index] = temp
    
    # Afficher le plateau de jeu mis à jour.

    document.querySelector('#jeu').innerHTML = addictionSolitaireHTML()


# La fonction verifierPartie ne prend aucun paramètre mais permet de
# vérifier les différentes conditions de victoire et affiche un message
# en conséquence.

def verifierPartie():

    if testVictoire() == True :
        document.querySelector('#brassesMessage') \
                .setAttribute("style", "display:none")
        document.querySelector('#victoire').removeAttribute("style")
    else : 
        if brassesRestantes > 0 :
            document.querySelector('#brassesRestantes') \
                    .setAttribute("style", "display:none")
            document.querySelector('#vousPouvez') \
                    .setAttribute("style", "display:none")
            document.querySelector('#vousDevez').removeAttribute("style")
        else :
            document.querySelector('#brassesMessage') \
                    .setAttribute("style", "display:none")
            document.querySelector('#defaite').removeAttribute("style")


# La fonction testVictoire valide les conditions de victoire.

def testVictoire():

    # Itération sur la rangée.

    for i in range(nbRangees):

        # Itération sur les colonnes.

        for j in range(nbColonnes-1):
            valeurCarte = plateauJeu[i*13+j]
            if (valeurCarte - valeurCarte % 4) != j+4 :
                return False
    return True


# La fonction clic prend en paramètre la variable "index", un nombre qui 
# représente la case sur laquelle le joueur a cliqué. Elle permet de
# déplacer la carte sur laquelle le joueur a cliqué si celle-ci est activée
# et permets aussi d'activer la ou les nouvelles cartes en fonction de la 
# position de la nouvelle case vide. Elle permet aussi de vérifier
# si la partie est terminée ou non en fonction de l'état de la partie.

def clic(index):
    if index in casesActives :
        deplacerCarte(index)
        activeCartes()

    # Vérifier l'issue de la partie.

    if casesActives == []:
        verifierPartie()



### Fonctions pour produire le contenu HTML ###


# La fonction "addictionSolitaireHTML" ne prend aucun paramètre et retourne
# le texte HTML pour le contenu de l'élement "#jeu"correspondant au plateau
# de jeu avec les cartes en position de nouvelle partie.

def addictionSolitaireHTML():
    
    # Index : permet de générer un id unique de case
    # et accéder à la valeur du plateau de jeu

    index = 0

    # Texte qui va contenir le contenu de chaque rangée

    contenu = ""

    # Itération sur la rangée.

    for _ in range(nbRangees):

        # Itération sur les colonnes.

        rangee = ""
        for _ in range(nbColonnes):
            cellule = tdHTML(' id="case' + str(index) + '" onclick="clic(' +
                str(index) + ')"', imgSVG(plateauJeu[index]))
            rangee += cellule
            index += 1
        
        rangee = "<tr>" + rangee + "</tr>"

        contenu += rangee

    return contenu

# Toutes les fonctions suivantes ont été prisent de l'exercice
# noté #9. Cela comprends aussi les commentaires.

# La fonction elem prend un nombre entier non-negatif en paramètre
# et retourne une référence vers l'élement DOM du document qui a un
# attribut "id" de la forme "indexN" ou "N" est le nombre passé en
# paramètre.

def elem(n):
    return document.querySelector('#case' + str(n))


# La fonction "tdHTML" prend deux textes en paramètre et retourne le
# texte HTML correspondant à une balise "td" qui a les attributs et
# contenu spécifié par le premier et second paramètre respectivement.

def tdHTML(attrs, contenu):
    return '<td' + attrs + '>' + contenu + '</td>'


# La fonction "imgHTML" prend un texte en paramètre et retourne le
# texte HTML correspondant à une balise "img" avec un attribut "src"
# égal au texte spécifé en paramètre.

def imgSVG(index):
    return '<img src="cards/' + refSVG[index] + '.svg">' if index > 3  \
    else '<img style="visibility: hidden;" src="cards/' + \
                                            refSVG[index] + '.svg">'