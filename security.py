# security.py

from exceptions import UnauthorizedAction
from getpass import getuser

# Affiche un message de retour formaté
def show_result(success: bool, message: str):
    prefix = "[✅ OK] " if success else "[❌ ERREUR] "
    print(prefix + message)

# Valide les choix utilisateurs simples
def ask_input(prompt: str, valid_choices: list):
    while True:
        val = input(prompt)
        if val in valid_choices:
            return val
        print("Choix invalide.")

# Décorateur de vérification de rôle
def require_role(*roles):
    def decorator(func):
        def wrapper(*args, **kwargs):
            current_user = kwargs.get("user")
            if not current_user or current_user["role"] not in roles:
                raise UnauthorizedAction("Action réservée à ces rôles : " + ", ".join(roles))
            return func(*args, **kwargs)
        return wrapper
    return decorator
