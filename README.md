# 🤖 Automates Finis — Projet EFREI 2024/2025

Ce projet a été réalisé dans le cadre du module **"Automates Finis et Expressions Rationnelles"** en 2e année à l’EFREI.  
Il consiste à développer en Python un programme capable de lire, afficher, transformer et tester des automates finis, à partir de fichiers `.txt`.

## 🧠 Objectifs pédagogiques

- Lire un automate depuis un fichier texte
- Afficher sa structure : états, transitions, états initiaux et finaux
- Vérifier s’il est déterministe, standard, complet
- Appliquer des traitements : standardisation, déterminisation, complétion, minimisation
- Tester la reconnaissance de mots
- Générer l’automate du langage complémentaire

## 📁 Structure du projet

- `main.py` : boucle principale du programme (interface console)
- `automate.py` : classes et fonctions liées à la gestion des automates
- `utils.py` : fonctions utilitaires pour la lecture et l'affichage
- `automates/` : fichiers `.txt` contenant les automates à charger
- `README.md` : documentation du projet

## ▶️ Exécution

Assurez-vous d’avoir **Python 3.x** installé.

Lancez simplement :

```bash
python3 main.py
