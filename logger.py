# logger.py
import datetime
from config import LOG_FILE

def log_action(action: str, path: str = "", status: str = "OK", user=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    who = f"{user['username']} ({user['role']})" if user else "SYSTEM"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {who} | {action} | {path} | {status}\n")

def log_error(error_msg: str, user=None):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    who = f"{user['username']} ({user['role']})" if user else "SYSTEM"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {who} | ERROR | {error_msg}\n")
