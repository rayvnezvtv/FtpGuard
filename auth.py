# auth.py
import json
from getpass import getpass
from pathlib import Path

USERS_FILE = Path("../users.json")

def load_users():
    if not USERS_FILE.exists():
        print("❌ Fichier users.json introuvable.")
        return {}

    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
            else:
                print("❌ Le fichier users.json ne contient pas un dictionnaire valide.")
                return {}
    except Exception as e:
        print(f"❌ Erreur lors de la lecture de users.json : {e}")
        return {}

def authenticate():
    users = load_users()
    if not users:
        print("❌ Aucun utilisateur trouvé.")
        return None

    username = input("Nom d'utilisateur : ")
    password = getpass("Mot de passe : ")

    user = users.get(username)
    if user and user["password"] == password:
        print(f"✅ Bienvenue {username} ({user['role']})")
        user["username"] = username  # on ajoute le nom dans le dictionnaire retourné
        return user

    print("❌ Identifiants invalides.")
    return None

if __name__ == "__main__":
    user = authenticate()
    print(user)
