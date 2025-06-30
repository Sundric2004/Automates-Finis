class Automate:
    def __init__(self):
        # Liste des attributs de l'automate
        self.langage = []
        self.etats = []
        self.etats_initiaux = []
        self.etats_finaux = []
        self.transitions = []

        # Type d'automate (synchrone/asynchrone)
        self.synchrone = True

    def reset(self):
        self.langage = []
        self.etats = []
        self.etats_initiaux = []
        self.etats_finaux = []
        self.transitions = []

        # Type d'automate (synchrone/asynchrone)
        self.synchrone = True

    def est_synchrone(self):
        """Met à jour et renvoie le type de l'automate (synchrone/asynchrone)"""
        for t in self.langage:
            if t == "$":
                self.langage.remove(t)
                self.synchrone = False
                break
        return self.synchrone

    def lire_mot_vide(self):
        """Renvoie vrai si l'automate reconnait le mot vide, faux sinon"""
        for t in self.etats_initiaux:
            if t in self.etats_finaux:
                return True
        return False

    def est_standard(self):
        """Vérifie si l'automate est standard."""
        if len(self.etats_initiaux) > 1:
            return False, 1
        for t in self.transitions:
            if t[2] == self.etats_initiaux[0]:
                return False, 2
        return True, None

    def est_deterministe(self):
        """Vérifie si l'automate est déterministe.

        Renvoie un tuple (booléen, code_erreur) où le booléen indique si l'automate est déterministe
        et code_erreur fournit une indication sur le type d'erreur détectée (None si aucun problème).
        """
        # Si l'automate n'est pas synchrone, il n'est pas déterministe
        if not self.synchrone:
            return False, 1

        # Un automate déterministe ne peut avoir qu'un seul état initial
        if len(self.etats_initiaux) > 1:
            return False, 2

        # Vérification des transitions : pour un même état et symbole, il doit n'y avoir qu'une seule transition
        for i in range(len(self.transitions)):
            for j in range(i + 1, len(self.transitions)):
                if (self.transitions[i][0] == self.transitions[j][0] and
                        self.transitions[i][1] == self.transitions[j][1]):
                    return False, 3

        return True, None

    def est_complet(self):
        """Vérifie si l'automate est complet."""
        if not self.est_deterministe()[0]:
            return False, 1
        if len(self.transitions) == len(self.etats) * len(self.langage):
            return True, None
        return False, 2

    def standardisation(self):
        """
        Renvoie un automate standardisé équivalent à celui courant s'il
        n'est pas déjà standard, sinon renvoie l'automate lui-même.
        """
        if not self.est_standard()[0]:
            a_standard = Automate()

            # Copie du langage et des états finaux
            a_standard.langage = self.langage[:]
            a_standard.etats_finaux = self.etats_finaux[:]

            # Copie des transitions
            a_standard.transitions = [t[:] for t in self.transitions]

            # Ajout du nouvel état initial dans la liste des états
            a_standard.etats.append("i")

            for etat in self.etats:
                a_standard.etats.append(etat)

            a_standard.etats_initiaux = ["i"]

            # Si l'état initial est aussi un état final, "i" devient final
            if self.lire_mot_vide():
                a_standard.etats_finaux.append("i")

            # Recréation des transitions avec les anciens états initiaux
            for t in self.transitions:
                if t[0] in self.etats_initiaux:
                    nouvelle_transition = ["i", t[1], t[2]]
                    if nouvelle_transition not in a_standard.transitions:
                        a_standard.transitions.append(nouvelle_transition)

            return a_standard

        return self

    def determinisation_et_completion(self):
        """
        Applique la déterminisation et la complétion à l'automate courant.
        Gère séparément les cas des automates synchrones et asynchrones.
        """
        if self.est_synchrone():
            return self.dc_synchrone()

        return self.dc_asynchrone()

    def parcours_epsilon(self, etat):
        """
        Retourne l'epsilon-clôture d'un état de l'automate de manière récursive.
        Les états de l'epsilon-clôture sont séparés par un point ".".
        """
        retour = etat + "."

        for transition in self.transitions:
            if transition[0] == etat and transition[1] == "$":
                retour += self.parcours_epsilon(transition[2]) + "."

        return retour[:-1]  # Suppression du dernier caractère "."

    def dc_asynchrone(self):
        """
        Renvoie l'automate déterministe, complet et synchrone équivalent à l'automate
        courant asynchrone.

        L'algorithme de déterminisation d'un automate asynchrone est similaire à celui
        d'un automate synchrone, sauf que les comparaisons se font sur l'ensemble des
        états de son epsilon-clôture.
        """

        # Dictionnaire contenant les epsilon-clôtures de chaque état
        liste_clotures = {}
        for etat in self.etats:
            liste_clotures[etat] = self.parcours_epsilon(etat)

        # Création de l'unique état initial
        ei = "-".join(liste_clotures[etat] for etat in self.etats_initiaux)

        # Initialisation des nouveaux attributs de l'automate
        nouveaux_e = [ei]
        sous_e_nouveaux = {ei: ei.split("-")}
        sous_e_nouveaux[ei].sort()
        nouveaux_ei = [ei]
        nouveaux_ef = []
        nouveaux_t = []

        # Gestion de la queue pour le parcours des états
        queue = [ei]
        while queue:
            etat = queue.pop(0)
            liste_etats = etat.split("-")
            final = any(e in self.etats_finaux for sous_e in liste_etats for e in sous_e.split("."))

            # Ajout aux états finaux si l'un des états est final
            if final and etat not in nouveaux_ef:
                nouveaux_ef.append(etat)

            # Création des transitions de l'état
            for lettre in self.langage:
                liste_es = []
                for e in liste_etats:
                    for t in self.transitions:
                        if t[0] in e.split(".") and t[1] == lettre:
                            liste_es.append(liste_clotures[t[2]])

                etat_suivant = "-".join(liste_es)
                sous_etat_suivant = etat_suivant.split("-")
                sous_etat_suivant.sort()

                if etat_suivant:
                    # Ajout de l'état d'arrivée dans la queue et la liste des états
                    if sous_etat_suivant not in sous_e_nouveaux.values():
                        queue.append(etat_suivant)
                        nouveaux_e.append(etat_suivant)
                        sous_e_nouveaux[etat_suivant] = sous_etat_suivant
                        nouveaux_t.append([etat, lettre, etat_suivant])
                    else:
                        for e, sous_e in sous_e_nouveaux.items():
                            if sous_e == sous_etat_suivant:
                                nouveaux_t.append([etat, lettre, e])
                                break

        # Mise à jour des attributs de l'automate
        a_deterministe = Automate()
        a_deterministe.langage = self.langage.copy()
        a_deterministe.etats = nouveaux_e
        a_deterministe.etats_initiaux = nouveaux_ei
        a_deterministe.etats_finaux = nouveaux_ef
        a_deterministe.transitions = nouveaux_t
        a_deterministe.synchrone = True

        return a_deterministe.completion(nouveau=False)

    def dc_synchrone(self):
        """Renvoie l'automate déterministe et complet équivalent à l'automate courant"""

        if not self.est_deterministe()[0]:
            # Création de l'unique état initial
            ei = "-".join(self.etats_initiaux)

            # Initialisation des nouveaux attributs de l'automate
            nouveaux_e = [ei]
            sous_e_nouveaux = {ei: list(ei.split("-"))}
            sous_e_nouveaux[ei].sort()
            nouveaux_ei = [ei]
            nouveaux_ef = []
            nouveaux_t = []

            # Création de la queue pour les états et transitions à construire
            queue = [ei]
            while queue:
                # Premier état de la queue
                etat = queue.pop(0)

                # Séparation de chaque état composé en ses états élémentaires
                liste_etats = etat.split("-")
                for e in liste_etats:
                    # Rend le nouvel état final si l'un de ses états élémentaires est final
                    if etat not in nouveaux_ef and e in self.etats_finaux:
                        nouveaux_ef.append(etat)

                # Création des transitions de l'état
                for lettre in self.langage:
                    liste_es = []
                    for e in liste_etats:
                        for t in self.transitions:
                            # Prend l'état d'arrivée de chacun de ses états élémentaires par la transition
                            if t[0] == e and t[1] == lettre and t[2] not in liste_es:
                                liste_es.append(t[2])

                    etat_suivant = "-".join(liste_es)
                    sous_etat_suivant = etat_suivant.split("-")
                    sous_etat_suivant.sort()

                    if etat_suivant:
                        # Ajout de l'état d'arrivée dans la queue et dans la liste des états
                        if sous_etat_suivant not in sous_e_nouveaux.values():
                            queue.append(etat_suivant)
                            nouveaux_e.append(etat_suivant)
                            sous_e_nouveaux[etat_suivant] = sous_etat_suivant
                            # Ajout de la transition dans la liste des transitions
                            nouveaux_t.append([etat, lettre, etat_suivant])
                        else:
                            for e, sous_e in sous_e_nouveaux.items():
                                if sous_e == sous_etat_suivant:
                                    nouveaux_t.append([etat, lettre, e])
                                    break

            # Mise à jour des attributs de l'automate
            a_deterministe = Automate()
            a_deterministe.langage = self.langage.copy()
            a_deterministe.etats = nouveaux_e
            a_deterministe.etats_initiaux = nouveaux_ei
            a_deterministe.etats_finaux = nouveaux_ef
            a_deterministe.transitions = nouveaux_t
            a_deterministe.synchrone = True

            return a_deterministe.completion(nouveau=False)

        else:
            return self.completion(nouveau=True)

    def completion(self, nouveau=True):
        """
        Renvoie un automate qui correspond à la version complète de l'automate d'origine.
        Si "nouveau" est mis à False, l'automate d'origine est modifié et renvoyé,
        sinon un nouveau est créé pour accueillir les modifications.
        """

        # Vérification si l'automate est déjà complet
        if self.est_complet()[0]:
            return self

        # Création de la liste des transitions manquantes
        t_manquants = {}
        for etat in self.etats:
            for lettre in self.langage:
                existe = any(t[0] == etat and t[1] == lettre for t in self.transitions)
                if not existe:
                    t_manquants.setdefault(etat, []).append(lettre)

        # Création de l'automate à retourner s'il n'est pas déjà créé
        if nouveau:
            a_complet = Automate()

            # Copie profonde des attributs pour éviter les modifications accidentelles
            a_complet.langage = self.langage.copy()
            a_complet.etats = self.etats.copy()
            a_complet.etats_initiaux = self.etats_initiaux.copy()
            a_complet.etats_finaux = self.etats_finaux.copy()
            a_complet.transitions = [t.copy() for t in self.transitions]
        else:
            a_complet = self

        # Ajout de l'état poubelle
        a_complet.etats.append("P")

        # Ajout des transitions manquantes vers l'état poubelle
        for etat, lettres in t_manquants.items():
            for lettre in lettres:
                a_complet.transitions.append([etat, lettre, "P"])

        # Ajout des transitions de l'état poubelle sur lui-même
        for lettre in a_complet.langage:
            a_complet.transitions.append(["P", lettre, "P"])

        return a_complet

    def lire_fichier(self, *file: str):
        """Lit un fichier contenant un automate et met à jour les attributs."""
        self.reset()
        file = file[0] if file else "test.txt"
        with open(file, 'r') as f:
            i = 1
            for ligne in f:
                if i in [1, 2, 5]:
                    i += 1
                    continue
                elif i == 3:
                    ligne_scinde = ligne[:-1].split(" ")
                    for j in range(int(ligne_scinde[0])):
                        self.etats.append(ligne_scinde[j + 1])
                        self.etats_initiaux.append(ligne_scinde[j + 1])
                elif i == 4:
                    ligne_scinde = ligne[:-1].split(" ")
                    for j in range(int(ligne_scinde[0])):
                        self.etats_finaux.append(ligne_scinde[j + 1])
                        if ligne_scinde[j + 1] not in self.etats:
                            self.etats.append(ligne_scinde[j + 1])
                else:
                    ligne_scinde = ligne[:-1].split(" ")
                    self.transitions.append(ligne_scinde)
                    if ligne_scinde[1] not in self.langage:
                        self.langage.append(ligne_scinde[1])
                    if ligne_scinde[0] not in self.etats:
                        self.etats.append(ligne_scinde[0])
                    if ligne_scinde[2] not in self.etats:
                        self.etats.append(ligne_scinde[2])
                i += 1
        self.est_synchrone()

    def minimisation(self):
        """Renvoie un tuple contenant l'automate minimal équivalent à l'automate courant,
        accompagné d'un True si l'automate d'origine était déjà minimal, False sinon"""

        # Deux groupes au premier tour : Terminaux et Non-Terminaux
        groupes = [{}, {}]
        for ei in self.etats_finaux:
            groupes[0][ei] = [0 for _ in range(len(self.langage))]
        for etat in self.etats:
            if etat not in self.etats_finaux:
                groupes[1][etat] = [0 for _ in range(len(self.langage))]

        # Tant que les groupes sont séparés...
        separer = True
        while separer:
            # Pour chaque état de chaque groupe...
            for g in groupes:
                for etat in g.keys():
                    # Pour chaque caractère du langage...
                    for i in range(len(self.langage)):
                        # On prend l'état d'arrivée...
                        etat_arrive = ""
                        for t in self.transitions:
                            if t[0] == etat and t[1] == self.langage[i]:
                                etat_arrive = t[2]

                        # Puis on le retrouve dans la liste des groupes pour assigner à l'état de départ
                        # le bon indice dans la liste qui correspond
                        for j in range(len(groupes)):
                            if etat_arrive in groupes[j].keys():
                                g[etat][i] = j
                                break

            # Pour chacun des groupes existants...
            nb_groupes = len(groupes)
            for i in range(nb_groupes):
                # On forme un sous-groupes de l'ensemble des transitions qui existent...
                sous_groupes = {}
                for etat, t in groupes[i].items():
                    if tuple(t) in sous_groupes.keys():
                        sous_groupes[tuple(t)].append(etat)
                    else:
                        sous_groupes[tuple(t)] = [etat]

                # Puis on recrée un groupe avec tous les états qui ont les mêmes indices en liste de transitions
                for t, etats in sous_groupes.items():
                    nouveau_groupe = {}
                    for etat in etats:
                        nouveau_groupe[etat] = list(t)
                    groupes.append(nouveau_groupe)

            # On retire les groupes du tour précédent
            for i in range(nb_groupes):
                groupes.pop(0)

            # Si le nombre de groupes n'a pas changé, alors l'automate est minimal : plus d'opération à faire
            separer = not (len(groupes) == nb_groupes)

        # Mise à jour des informations
        a_minimal = Automate()
        a_minimal.langage = self.langage.copy()

        # Pour chaque nouvel état résultat de l'agrégation des groupes...
        for comb_etats in groupes:
            # On les nomme par une combinaison des noms des états précédents
            etat = "_".join(comb_etats.keys())
            a_minimal.etats.append(etat)

        k = 0
        for etat in a_minimal.etats:
            nom_etats = list(groupes[k].keys())

            # Mise à jour des états initiaux
            for etat_elementaire in nom_etats:
                if etat_elementaire in self.etats_initiaux:
                    a_minimal.etats_initiaux.append(etat)
                    break

            # Mise à jour des états finaux
            for etat_elementaire in nom_etats:
                if etat_elementaire in self.etats_finaux:
                    a_minimal.etats_finaux.append(etat)
                    break

            # Création des transitions des nouveaux états
            for lettre in self.langage:
                creer = False
                for t in self.transitions:
                    if creer:
                        break
                    for ancien_etat in nom_etats:
                        if creer:
                            break
                        # Recherche du groupe contenant l'état d'arrivée
                        if t[0] == ancien_etat and t[1] == lettre:
                            for i in range(len(groupes)):
                                if t[2] in list(groupes[i].keys()):
                                    a_minimal.transitions.append([etat, lettre, a_minimal.etats[i]])
                                    creer = True
                                    break
            k += 1

        # Si l'automate final a autant d'états que l'automate de départ, alors il est minimal
        return (a_minimal, len(self.etats) == len(a_minimal.etats))

    def complementaire(self):
        """Retourne le complémentaire de l'automate courant à partir de son
        équivalent déterminisé et complet"""

        # L'algorithme déterminise et complète si l'automate fourni n'est pas DC,
        # et cela même si la boucle principale empêche l'automate en attribut de ne pas être DC

        if not self.est_deterministe()[0]:
            a_complementaire = self.determinisation_et_completion()
            a_complementaire.etats_finaux = []

        elif not self.est_complet()[0]:
            a_complementaire = self.completion()
            a_complementaire.etats_finaux = []

        else:
            # Copie profonde des attributs de l'automate d'origine
            a_complementaire = Automate()
            a_complementaire.langage = self.langage.copy()
            a_complementaire.etats = self.etats.copy()
            a_complementaire.etats_initiaux = self.etats_initiaux.copy()

            # Copie des transitions
            for t in self.transitions:
                a_complementaire.transitions.append(t.copy())

        # Les états qui étaient finaux ne le sont plus, ceux qui ne l'étaient pas le deviennent
        a_complementaire.etats_finaux = [
            etat for etat in self.etats if etat not in self.etats_finaux
        ]

        return a_complementaire

    def reconnaitre_mot(self, mot: str):
        """Vérifie si un mot est reconnu par l'automate courant"""

        # Si l'automate n'est pas déterministe ou complet, on le transforme
        if not self.est_deterministe()[0]:
            a_lecture = self.determinisation_et_completion()
        elif not self.est_complet()[0]:
            a_lecture = self.completion()
        else:
            a_lecture = self

        # Commencement à l'état initial
        etat = a_lecture.etats_initiaux[0]

        for l_mot in mot:
            # Si le caractère n'est pas reconnu par le langage, le mot ne l'est pas non plus
            if l_mot not in a_lecture.langage:
                return False

            changement = False

            # Vérifie si une transition existe pour ce caractère
            for t in a_lecture.transitions:
                if t[0] == etat and t[1] == l_mot:
                    etat = t[2]
                    changement = True
                    break

            # Si aucune transition n'existe, le mot n'est pas reconnu
            if not changement:
                return False

        # Si l'état final atteint est un état d'acceptation, le mot est reconnu
        return etat in a_lecture.etats_finaux

    def affichage(self):
        """Affiche l'automate sous forme de tableau et sauvegarde le résultat dans un fichier texte (ajout à chaque appel)."""

        # Liste pour accumuler les chaînes de caractères affichées
        output = []

        # Fonction d'affichage personnalisée qui affiche et enregistre la sortie
        def my_print(*args, **kwargs):
            sep = kwargs.get("sep", " ")
            end = kwargs.get("end", "\n")
            texte = sep.join(str(arg) for arg in args) + end
            # Affichage à la console
            print(texte, end='')
            # Ajout dans la variable output
            output.append(texte)

        # Début de l'affichage
        my_print("-----------------------------------" + "-------------------" * len(self.langage))

        # Ligne des caractères du langage
        my_print("|              |                  |", end="")
        for lettre in self.langage:
            my_print(" {:^16} |".format(lettre), end="")
        my_print("")
        my_print("-----------------------------------" + "-------------------" * len(self.langage))

        raccourcis = {}
        remplacement = "A"

        # Lignes des états pour l'automate synchrone
        if self.synchrone:
            for etat in self.etats:
                # Attribution d'un raccourci si le nom de l'état est trop long
                if len(etat) > 16:
                    raccourcis[etat] = remplacement
                    remplacement = chr(ord(remplacement) + 1) if remplacement != "D" else "F"

            for etat in self.etats:
                # Marquage de l'état initial
                my_print("| {:^6}".format("E" if etat in self.etats_initiaux else ""), end="")

                # Marquage de l'état terminal
                my_print("{:^6} |".format("S" if etat in self.etats_finaux else ""), end="")

                # Affichage du nom ou du raccourci de l'état
                if etat in raccourcis:
                    my_print(" {:^16} |".format(raccourcis[etat]), end="")
                else:
                    my_print(" {:^16} |".format(etat), end="")

                for lettre in self.langage:
                    # Liste des états d'arrivés pour le caractère courant
                    liste_transitions = []
                    for t in self.transitions:
                        if t[0] == etat and t[1] == lettre:
                            liste_transitions.append(raccourcis[t[2]] if t[2] in raccourcis else t[2])
                    # Gestion des transitions multiples
                    nouveau_t = ",".join(liste_transitions)
                    if len(nouveau_t) > 16:
                        if nouveau_t in raccourcis:
                            nouveau_t = raccourcis[nouveau_t]
                        else:
                            raccourcis[nouveau_t] = remplacement
                            nouveau_t = remplacement
                            remplacement = chr(ord(remplacement) + 1) if remplacement != "D" else "F"
                    my_print(" {:^16} |".format(nouveau_t), end="")
                my_print("")
            my_print("-----------------------------------" + "-------------------" * len(self.langage))
        else:
            # Automate non synchrone : gestion de l'epsilon cloture
            liste_noms = {}
            for etat in self.etats:
                nom_etat = self.parcours_epsilon(etat)
                liste_noms[etat] = nom_etat
                if len(nom_etat) > 16:
                    raccourcis[nom_etat] = remplacement
                    remplacement = chr(ord(remplacement) + 1) if remplacement != "D" else "F"

            for etat in self.etats:
                liste_e_cloture = liste_noms[etat].split(".")
                ei = "E" if any(sous_etat in self.etats_initiaux for sous_etat in liste_e_cloture) else ""
                ef = "S" if any(sous_etat in self.etats_finaux for sous_etat in liste_e_cloture) else ""
                my_print("| {:^6} | {:^6} |".format(ei, ef), end="")

                nom_etat = liste_noms[etat]
                if nom_etat in raccourcis:
                    my_print(" {:^16} |".format(raccourcis[nom_etat]), end="")
                else:
                    my_print(" {:^16} |".format(nom_etat), end="")

                for lettre in self.langage:
                    liste_transitions = []
                    for t in self.transitions:
                        if t[0] in liste_e_cloture and t[1] == lettre:
                            nouveau_nom = liste_noms[t[2]]
                            liste_transitions.append(
                                raccourcis[nouveau_nom] if nouveau_nom in raccourcis else nouveau_nom)
                    nouveau_t = ",".join(liste_transitions)
                    if len(nouveau_t) > 16:
                        raccourcis[nouveau_t] = remplacement
                        nouveau_t = remplacement
                        remplacement = chr(ord(remplacement) + 1) if remplacement != "D" else "F"
                    my_print(" {:^16} |".format(nouveau_t), end="")
                my_print("")
            my_print("-----------------------------------" + "-------------------" * len(self.langage))

        # Affichage des correspondances utilisées
        if raccourcis:
            my_print("\nCorrespondances:")
            for long, court in raccourcis.items():
                my_print(f"{court} = {long}")

        # Sauvegarde du résultat dans un fichier texte en mode ajout
        with open("resultat.txt", "a", encoding="utf-8") as fichier:
            fichier.write("".join(output))
