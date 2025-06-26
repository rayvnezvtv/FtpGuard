# main.py
from pathlib import Path
from config import BASE_DIR
from file_manager import print_tree, create_folder, create_file, delete_path, rename_path
from ftp_backup import upload_audit_folder, upload_user_audit
from auth import authenticate
import sys

# Authentification
user = None
while not user:
    user = authenticate()

role = user["role"]

# Restriction du chemin pour les clients
if role == "user":
    user_path = BASE_DIR / user["region"] / user["client"]
else:
    user_path = BASE_DIR

def show_menu():
    print("\n=== MENU ===")
    print("1. Afficher l’arborescence")
    print("2. Créer un dossier")
    print("3. Créer un fichier")
    print("4. Supprimer un fichier ou dossier")
    print("5. Renommer un fichier ou dossier")
    print("6. Sauvegarder les fichiers d’audit vers le FTP")
    print("0. Quitter")

while True:
    show_menu()
    choice = input("Votre choix : ")

    if choice == "1":
        print_tree(user_path)

    elif choice == "2":
        name = input("Nom du dossier à créer : ")
        create_folder(user_path / name)

    elif choice == "3":
        name = input("Nom du fichier à créer : ")
        create_file(user_path / name)

    elif choice == "4":
        name = input("Nom du fichier ou dossier à supprimer : ")
        delete_path(user_path / name)

    elif choice == "5":
        old = input("Nom du fichier ou dossier à renommer : ")
        new = input("Nouveau nom : ")
        rename_path(user_path / old, new)

    elif choice == "6":
        if role == "admin":
            upload_audit_folder(BASE_DIR)
        else:
            upload_user_audit(user)

    elif choice == "0":
        print("À bientôt !")
        sys.exit()

    else:
        print("Choix invalide.")
