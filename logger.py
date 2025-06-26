# logger.py
import datetime
from config import LOG_FILE

def log_action(action: str, path: str = "", status: str = "OK"):
    """
    Enregistre une action dans le fichier de log avec un horodatage.
    :param action: Nom de l'action (CREATE, DELETE, FTP_UPLOAD, etc.)
    :param path: Chemin concerné
    :param status: Résultat (OK, ERROR, etc.)
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {action} | {path} | {status}\n")

def log_error(error_msg: str):
    """
    Enregistre une erreur dans le fichier de log avec un horodatage.
    :param error_msg: Message de l'erreur
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] ERROR | {error_msg}\n")
