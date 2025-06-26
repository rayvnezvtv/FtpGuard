# ftp_backup.py

from ftplib import FTP, error_perm
from config import FTP_HOST, FTP_PORT, FTP_USER, FTP_PASS, BASE_DIR
from logger import log_action, log_error
from pathlib import Path

def connect_ftp():
    try:
        ftp = FTP()
        ftp.connect(FTP_HOST, FTP_PORT)
        ftp.login(FTP_USER, FTP_PASS)
        log_action("FTP_CONNECT", FTP_HOST)
        return ftp
    except Exception as e:
        log_error(f"FTP connection failed: {e}")
        return None

def ensure_ftp_path(ftp: FTP, region: str, client: str):
    try:
        for folder in [region, client]:
            try:
                ftp.cwd(folder)
            except error_perm:
                ftp.mkd(folder)
                ftp.cwd(folder)
    except Exception as e:
        log_error(f"ensure_ftp_path failed: {e}")

def upload_file(ftp: FTP, local_file: Path, region: str, client: str):
    try:
        ftp.cwd("/")
        ensure_ftp_path(ftp, region, client)
        with open(local_file, "rb") as f:
            ftp.storbinary(f"STOR {local_file.name}", f)
        log_action("FTP_UPLOAD", str(local_file))
    except Exception as e:
        log_error(f"upload_file failed: {e}")

# === SUPERADMIN : tout l'arbre FTP ===
def upload_audit_folder(base_path: Path):
    ftp = connect_ftp()
    if not ftp:
        return
    try:
        for region_folder in base_path.iterdir():
            if region_folder.is_dir():
                for client_folder in region_folder.iterdir():
                    if client_folder.is_dir():
                        for file in client_folder.iterdir():
                            if file.is_file() and file.name.startswith("audit."):
                                upload_file(ftp, file, region_folder.name, client_folder.name)
    except Exception as e:
        log_error(f"upload_audit_folder failed: {e}")
    finally:
        ftp.quit()

# === ADMIN : sa propre ville ===
def upload_admin_audit(user):
    ftp = connect_ftp()
    if not ftp:
        return
    try:
        region = user["region"]
        region_path = BASE_DIR / region
        for client_folder in region_path.iterdir():
            if client_folder.is_dir():
                for file in client_folder.iterdir():
                    if file.is_file() and file.name.startswith("audit."):
                        upload_file(ftp, file, region, client_folder.name)
    except Exception as e:
        log_error(f"upload_admin_audit failed: {e}", user)
    finally:
        ftp.quit()

# === USER : son propre dossier ===
def upload_user_audit(user):
    ftp = connect_ftp()
    if not ftp:
        return
    try:
        region = user["region"]
        client = user["client"]
        path = BASE_DIR / region / client
        for file in path.iterdir():
            if file.is_file() and file.name.startswith("audit."):
                upload_file(ftp, file, region, client)
    except Exception as e:
        log_error(f"upload_user_audit failed: {e}", user)
    finally:
        ftp.quit()
