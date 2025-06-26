# tools.py

from config import LOG_FILE
from security import show_result

def read_logs(user):
    if user["role"] != "superadmin":
        show_result(False, "Accès interdit. Réservé au superadmin.")
        return

    try:
        print("\n=== Journal des activités ===")
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            print(f.read())
    except Exception as e:
        show_result(False, f"Erreur lecture log: {e}")
