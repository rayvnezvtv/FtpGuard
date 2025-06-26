from pathlib import Path
from dotenv import load_dotenv
import os

# Chargement des variables d'environnement
load_dotenv()

# === CONFIGURATION GLOBALE ===

# Chemins de base (à adapter si besoin)
BASE_DIR = Path("C:/FTP")

# FTP Configuration
FTP_HOST = os.getenv("FTP_HOST")
FTP_PORT = int(os.getenv("FTP_PORT", "21"))
FTP_USER = os.getenv("FTP_USER")
FTP_PASS = os.getenv("FTP_PASS")

# Journal des logs
LOG_FILE = Path("activity.log")

# === Clients & régions ===
REGIONS = ["Paris", "Marseille", "Rennes", "Grenoble"]