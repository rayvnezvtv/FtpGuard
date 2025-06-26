# auth.py
import json
from getpass import getpass

USERS_FILE = "users.json"

def load_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def authenticate():
    users = load_users()
    username = input("Nom d'utilisateur : ")
    password = getpass("Mot de passe : ")

    for user in users:
        if user["username"] == username and user["password"] == password:
            print(f"✅ Bienvenue {username} ({user['role']})")
            return user
    print("❌ Identifiants invalides.")
    return None
