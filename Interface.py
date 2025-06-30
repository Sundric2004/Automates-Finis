def afficher_accueil():
    """Message d'accueil"""
    print("\n============ Gestion des Automates ============\n")

def afficher_menu():
    """Message du menu principal"""
    print("Que voulez-vous faire ?\n"
          "\t-1 Lire un nouvel automate d'un fichier \n"
          "\t-2 Afficher l'automate courant\n"
          "\t-3 Standardisation\n"
          "\t-4 Déterminisation Completion (DC)\n"
          "\t-5 DC minimal\n"
          "\t-6 DC complémentaire \n"
          "\t-7 Vérifier si l'automate reconnait des mots (nécessite l'automate DC)\n"
          "\t-8 Quitter\n")

def afficher_standard():
    """Message du menu de standardisation"""
    print("Que voulez-vous faire ?\n"
          "\t-1 Vérifier si l'automate d'origine est standard\n"
          "\t-2 Calculer et afficher l'automate standard équivalent\n"
          "\t-3 Retour au menu précédent\n")

def afficher_dc():
    """Message du menu de déterminisation/complétion"""
    print("Que voulez-vous faire ?\n"
          "\t-1 Vérifier si l'automate d'origine est déterministe\n"
          "\t-2 Vérifier si l'automate d'origine est complet\n"
          "\t-3 Calculer et afficher l'automate déterministe complet (DC) équivalent\n"
          "\t-4 Retour au menu précédent\n")

def afficher_dc_minimal():
    """Message du menu de minimisation"""
    print("Que voulez-vous faire ?\n"
          "\t-1 Calculer et afficher l'automate DC minimal \n"
          "\t-2 Retour au menu précédent\n")

def afficher_dc_comp():
    """Message du menu de complémentarisation"""
    print("Que voulez-vous faire ?\n"
          "\t-1 Calculer et afficher l'automate DC complémentaire (nécessite l'automate DC) \n"
          "\t-2 Calculer et afficher l'automate DC minimal complémentaire (nécessite l'automate DC minimal) \n"
          "\t-3 Retour au menu précédent\n")

def choix(max_choix: int):
    """Permet de lire un entier compris entre 1 et l'entier max_choix.
    Redemande la lecture tant que la saisie ne correspond pas"""
    res = 0
    error = True
    while error:
        saisie = input("Votre choix : ")
        try:
            res = int(saisie)
            if res <= 0 or res > max_choix:
                print("Option non valide, veuillez réessayer")
            else:
                error = False
        except ValueError:
            print("Option non valide, veuillez réessayer")
    return res

def lecture_mot():
    """Simple fonction de lecture"""
    return input("Entrez un mot à reconnaître (--stop pour quitter) : ")
