# main.py

from networkscanner import scan_network
from pathlib import Path
from config import BASE_DIR
from file_manager import (
    print_tree, create_folder, create_file,
    delete_path, rename_path
)
from ftp_backup import (
    upload_audit_folder,
    upload_user_audit,
    upload_admin_audit
)
from auth import authenticate, create_user
from security import show_result
import sys

# === Authentification utilisateur ===
user = None
while not user:
    user = authenticate()

role = user["role"]

# === Détermination du périmètre d’accès selon le rôle ===
if role == "superadmin":
    user_path = BASE_DIR
elif role == "admin":
    user_path = BASE_DIR / user["region"]
elif role == "user":
    user_path = BASE_DIR / user["region"] / user["client"]
else:
    print("❌ Rôle inconnu.")
    sys.exit()

# === Menu dynamique selon le rôle ===
def show_menu():
    print("\n=== MENU ===")
    print("1. Afficher l’arborescence")
    print("2. Créer un dossier")
    print("3. Créer un fichier")
    print("4. Supprimer un fichier ou dossier")
    print("5. Renommer un fichier ou dossier")
    print("6. Sauvegarder les fichiers d’audit vers le FTP")
    if role in ["superadmin", "admin"]:
        print("7. Créer un utilisateur")
    if role == "superadmin":
        print("8. Voir le journal d’activité")
        print("9.Activer le scan réseau")
    print("0. Quitter")

# === Boucle principale ===
while True:
    show_menu()
    choice = input("Votre choix : ")

    if choice == "1":
        print_tree(user_path)

    elif choice == "2":
        name = input("Nom du dossier à créer : ")
        path = user_path / name
        create_folder(path, user, user_path)

    elif choice == "3":
        name = input("Nom du fichier à créer : ")
        path = user_path / name
        create_file(path, user, user_path)

    elif choice == "4":
        name = input("Nom du fichier/dossier à supprimer : ")
        path = user_path / name
        delete_path(path, user, user_path)

    elif choice == "5":
        old = input("Nom actuel : ")
        new = input("Nouveau nom : ")
        path = user_path / old
        rename_path(path, new, user, user_path)

    elif choice == "6":
        if role == "superadmin":
            upload_audit_folder(BASE_DIR)
        elif role == "admin":
            upload_admin_audit(user)
        elif role == "user":
            upload_user_audit(user)

    elif choice == "7" and role in ["superadmin", "admin"]:
        create_user(user)

    elif choice == "8" and role == "superadmin":
        from tools import read_logs
        read_logs(user)
    
    elif choice == "9" and role == "superadmin":
        from networkscanner import scan_network
        scan_network(portscan=True)


    elif choice == "0":
        print("👋 À bientôt.")
        break

    else:
        show_result(False, "Choix invalide.")
