# auth.py

import csv
import hashlib
from getpass import getpass

DATA_FILE = "data.csv"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    users = []
    try:
        with open(DATA_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                users.append(row)
    except Exception as e:
        print(f"Erreur lecture utilisateurs : {e}")
    return users

def save_users(users):
    try:
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["username", "password_hash", "role", "region", "client"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(users)
    except Exception as e:
        print(f"Erreur écriture utilisateurs : {e}")

def authenticate():
    users = load_users()
    username = input("Nom d'utilisateur : ")
    password = getpass("Mot de passe : ")
    hash_pwd = hash_password(password)

    for user in users:
        if user["username"] == username and user["password_hash"] == hash_pwd:
            print(f"✅ Bienvenue {username} ({user['role']})")
            return user
    print("❌ Identifiants invalides.")
    return None

def create_user(current_user):
    if current_user["role"] not in ["superadmin", "admin"]:
        print("❌ Vous n'avez pas le droit de créer des utilisateurs.")
        return

    users = load_users()
    username = input("🔹 Nom du nouvel utilisateur : ")
    if any(u["username"] == username for u in users):
        print("⚠️ Utilisateur déjà existant.")
        return

    password = getpass("🔹 Mot de passe : ")
    role = input("🔹 Rôle (user uniquement pour les admins) : ").strip().lower()

    if current_user["role"] == "admin" and role != "user":
        print("❌ Un admin ne peut créer que des utilisateurs (user).")
        return

    new_user = {
        "username": username,
        "password_hash": hash_password(password),
        "role": role,
        "region": "",
        "client": ""
    }

    if role == "admin" or role == "user":
        if current_user["role"] == "admin":
            new_user["region"] = current_user["region"]
        else:
            new_user["region"] = input("🔹 Région : ")

    if role == "user":
        new_user["client"] = input("🔹 Nom du client : ")

    users.append(new_user)
    save_users(users)
    print(f"✅ Utilisateur {username} créé avec succès.")
