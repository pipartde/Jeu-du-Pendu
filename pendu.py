from tkinter import *
from random import choice
import unicodedata


def fenetre():
    global motatrouver, lettredonnee, resultat, lebonmot, motaafficher, lettreabsente, nbrvie, chercher, ltr, dessin, windows
    windows = Tk()
    windows.title("jeu du pendu")

    # ___________________________
    # création des variables

    motaafficher = ["_", "_", "_", "_", "_", "_"]
    lettreabsente = []
    nbrvie = 10
    motatrouver=StringVar()
    lettredonnee=StringVar()
    resultat=StringVar()
    motatrouver.set(motaafficher)
    createmot()

    # ___________________________
    # création des widgets

    Label(windows, text="Mot à Trouver", width=30).grid(row=0, columnspan=3)
    Label(windows, textvariable=motatrouver, width=30).grid(row=1, columnspan=3)
    ltr = Entry(windows, textvariable=lettredonnee, width=5)
    ltr.grid(row=2, column=0)
    ltr.focus()
    Label(windows, text="Votre proposition", width=30).grid(row=2, column=1)
    chercher = Button(windows, text="chercher", command=affichage)
    chercher.grid(row=2, column=2)
    Label(windows, textvariable=resultat, width=60).grid(row=3, columnspan=3)
    dessin = Canvas(windows, width=100, height=100, borderwidth=5, background="#E4E4E4")
    dessin.grid(row=0, column=3, rowspan=4)
    windows.bind_all('<Return>', affichage)
    reset = Button(windows, text="Reset", command=nouveaujeu)
    reset.grid(row=4, column=3)


def load_dictionnary():
    """
    Ouvre le fichier texte et charge le dictionnaire
    :return: un dictionnaire contenant en clé le nombre de lettres et en valeur une liste des mots de cette taille
    """
    dic = {}
    with open("dico.txt", "r", encoding='utf-8') as file:
        for line in file:
            line = line.rstrip("\n").upper()
            size = len(line)
            if size in dic:
                dic[size].append(line)
            else:
                dic[size] = [line]
    return dic


def pick_a_word(size, dico):
    """
    Choisit un mot aléatoirement
    :param size: taille du mot à afficher
    :param dico: dictionnaire à utiliser
    :return: un mot de la taille size
    """
    return choice(dico[size])


def trouverposition():                  # donne la/les position(s) des lettres proposées
    position = []
    lettre=lettredonnee.get()
    for i in range(len(lebonmot)):
        if lebonmot[i] == lettre.upper():
            position.append(i)
    return position


def affichage(ev=None):
    global nbrvie
    motatrouver.set(motaafficher)
    if not trouverposition():                        # si pas de lettre
        lettreabsente.append(lettredonnee.get())     # on ajoute la lettre absente
        nbrvie -= 1                                  # on retire une vie
        if nbrvie > 0:                               # si assez de vie...
            resultat.set(f"Raté, il n'y a pas ces lettres : {', '.join(lettreabsente)}. Il vous reste {nbrvie} vie(s)")
        else:                                        # sinon c'est perdu
            resultat.set(f"perdu, vous n'avez plus de vie. Le mot était {lebonmot}")
    else:                                            # si lettre presente
        for i in trouverposition():                  # on ajoute la lettre
            motaafficher[i] = lettredonnee.get()
        motatrouver.set(motaafficher)
        count = 0
        for i in motaafficher:
            if i == "_":
                count += 1
        if count == 0:
            resultat.set("Gagné !!")
            chercher.config(state='disabled')
            ltr.config(state='disabled')
    lettredonnee.set("")
    pendu()


# création du pendu selon le nombre de PV

def pendu():
    if nbrvie == 9:
        dessin.create_line(20, 80, 80, 80)
    elif nbrvie == 8:
        dessin.create_line(25, 80, 25, 20)
    elif nbrvie == 7:
        dessin.create_line(25, 20, 70, 20)
        dessin.create_line(35, 20, 25, 30)
    elif nbrvie == 6:
        dessin.create_line(50, 20, 50, 30)
    elif nbrvie == 5:
        dessin.create_oval(45, 30, 55, 40)
    elif nbrvie == 4:
        dessin.create_line(50, 40, 50, 65)
    elif nbrvie == 3:
        dessin.create_line(50, 40, 40, 50)
    elif nbrvie == 2:
        dessin.create_line(50, 40, 60, 50)
    elif nbrvie == 1:
        dessin.create_line(50, 65, 40, 75)
    elif nbrvie == 0:
        dessin.create_line(50, 65, 60, 75)


def createmot():
    global lebonmot
    # chargement du mot du dictionnaire
    dic = load_dictionnary()
    leMots = pick_a_word(6, dic)
    lebonmot = ''.join((c for c in unicodedata.normalize('NFD', leMots) if unicodedata.category(c) != 'Mn'))
    print(leMots)
    print(lebonmot)


def nouveaujeu(ev=None):    #trouver une manière moins barbare de tout reset...
    windows.destroy()
    fenetre()


if __name__ == '__main__':
    fenetre()
    mainloop()
