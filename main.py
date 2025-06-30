from Automate import Automate
from Interface import *


def main():
    """Programme principal de test des fonctions"""

    # Variable pour activer la boucle
    continuer = True

    # Variables destinées à accueillir les différents automates
    a_test = None
    a_s_test = None
    a_dc_test = None
    a_dc_m_test = None
    a_dc_comp_test = None
    a_dc_m_comp_test = None

    # Message d'accueil
    afficher_accueil()

    while continuer:
        # Menu principal, avec sélection de l'option
        afficher_menu()
        res = choix(8)

        # Lecture d'un fichier contenant un automate
        if res == 1:
            try:
                if not a_test:
                    a_test = Automate()
                num_automate = input("\nVeuillez entrer le numéro de l'automate (max 44) : ")
                a_test.lire_fichier(f"Automates/P4_{num_automate}.txt")
                print("\nLecture réussie !!\n")
            except FileNotFoundError:
                print("Ce fichier n'existe pas, veuillez réessayer")
                continue

        # Affichage de l'automate lu (sans modification)
        elif res == 2:
            if not a_test:
                print("Aucun automate lu, veuillez d'abord en lire un")
            else:
                a_test.affichage()

        # Menu de standardisation
        elif res == 3:
            if not a_test:
                print("Aucun automate lu, veuillez d'abord en lire un")
            else:
                res_dc = 0
                while res_dc != 3:
                    afficher_standard()
                    res_dc = choix(3)

                    if res_dc == 1:
                        test_d = a_test.est_standard()
                        if test_d[0]:
                            print("L'automate d'origine est bien standard !")
                        elif test_d[1] == 1:
                            print("L'automate d'origine n'est pas standard, car il possède plus d'une entrée")
                        else:
                            print("L'automate d'origine n'est pas standard, car il existe une transition allant à l'état d'entrée")

                    elif res_dc == 2:
                        if a_test.est_standard()[0]:
                            print("L'automate d'origine est déjà standard")
                            a_test.affichage()
                        else:
                            a_s_test = a_test.standardisation()
                            a_s_test.affichage()

        # Menu de déterminisation et de complétion
        elif res == 4:
            if not a_test:
                print("Aucun automate lu, veuillez d'abord en lire un")
            else:
                res_dc = 0
                while res_dc != 4:
                    afficher_dc()
                    res_dc = choix(4)

                    if res_dc == 1:
                        test_d = a_test.est_deterministe()
                        if test_d[0]:
                            print("L'automate d'origine est bien déterministe !")
                        elif test_d[1] == 1:
                            print("L'automate d'origine n'est pas déterministe, car il est asynchrone")
                        elif test_d[1] == 2:
                            print("L'automate n'est pas déterministe, car il possède plus d'une entrée")
                        else:
                            print("L'automate d'origine n'est pas déterministe, car un état possède par un même caractère de transition plusieurs états d'arrivée")

                    elif res_dc == 2:
                        test_c = a_test.est_complet()
                        if test_c[0]:
                            print("L'automate d'origine est bien complet !")
                        elif test_c[1] == 1:
                            print("L'automate d'origine n'est pas complet, car il n'est pas déterministe")
                        else:
                            print("L'automate d'origine n'est pas complet car il manque une transition pour un des états")

                    elif res_dc == 3:
                        if a_test.est_complet()[0]:
                            a_dc_test = a_test
                        elif a_test.est_deterministe()[0]:
                            a_dc_test = a_test.completion()
                        else:
                            a_dc_test = a_test.determinisation_et_completion()
                        a_dc_test.affichage()

        # Menu de minimisation
        elif res == 5:
            if not a_dc_test:
                print("L'automate DC n'a pas été calculé, veuillez d'abord le calculer")
            else:
                res_dc = 0
                while res_dc != 2:
                    afficher_dc_minimal()
                    res_dc = choix(2)

                    if res_dc == 1:
                        a_dc_m_test, minimal = a_dc_test.minimisation()
                        if minimal:
                            print("L'automate DC était déjà minimal !")
                        else:
                            print("L'automate DC n'était pas minimal")
                        a_dc_m_test.affichage()

        # Menu du complémentaire
        elif res == 6:
            if not a_dc_test:
                print("L'automate DC n'a pas été calculé, veuillez le calculer avant")
            else:
                res_dc = 0
                while res_dc != 3:
                    afficher_dc_comp()
                    res_dc = choix(3)

                    if res_dc == 1:
                        if not a_dc_test:
                            print("\nL'automate DC n'est pas calculé, veuillez le calculer avant")
                        else:
                            a_dc_comp_test = a_dc_test.complementaire()
                            a_dc_comp_test.affichage()

                    elif res_dc == 2:
                        if not a_dc_m_test:
                            print("\nL'automate DC minimal n'est pas calculé, veuillez le calculer avant")
                        else:
                            a_dc_m_comp_test = a_dc_m_test.complementaire()
                            a_dc_m_comp_test.affichage()

        # Menu de reconnaissance des mots
        elif res == 7:
            if not a_dc_test:
                print("L'automate DC n'a pas été calculé, veuillez le calculer avant")
            else:
                lecture = ""
                while lecture != "--stop":
                    lecture = lecture_mot()
                    if lecture != "--stop":
                        if a_dc_test.reconnaitre_mot(lecture):
                            print(f"L'automate reconnait le mot {lecture}")
                        else:
                            print(f"L'automate ne reconnait pas le mot {lecture}")

        # Quitter le programme
        elif res == 8:
            continuer = False


if __name__ == "__main__":
    main()
