# daily_sync.py

from pathlib import Path
from datetime import datetime
from config import BASE_DIR
from file_manager import archive_audit_files
from ftp_backup import connect_ftp, ensure_ftp_path, upload_file
from logger import log_action, log_error

def daily_archive_and_push():
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        ftp = connect_ftp()
        if not ftp:
            return

        for region_folder in BASE_DIR.iterdir():
            if region_folder.is_dir():
                for client_folder in region_folder.iterdir():
                    if client_folder.is_dir():
                        # Archivage local
                        archive_audit_files(client_folder)

                        # Chemin local : archives/YYYY-MM-DD/
                        archive_dir = client_folder / "archives" / today
                        if not archive_dir.exists():
                            continue

                        # Aller dans le bon dossier FTP (ex: /Paris/ClientA/archives/2025-06-25)
                        try:
                            ftp.cwd("/")
                            ensure_ftp_path(ftp, region_folder.name, client_folder.name)
                            for folder in ["archives", today]:
                                try:
                                    ftp.cwd(folder)
                                except:
                                    ftp.mkd(folder)
                                    ftp.cwd(folder)
                        except Exception as e:
                            log_error(f"FTP nav failed: {e}")
                            continue

                        # Upload de tous les fichiers du jour
                        for file in archive_dir.iterdir():
                            if file.is_file() and file.name.startswith("audit."):
                                upload_file(ftp, file, region_folder.name, client_folder.name + f"/archives/{today}")
        
        log_action("DAILY_ARCHIVE_PUSH", f"Archivage + FTP {today} terminé")
    except Exception as e:
        log_error(f"daily_archive_and_push failed: {e}")
    finally:
        if 'ftp' in locals():
            ftp.quit()

if __name__ == "__main__":
    print("=== ARCHIVAGE + PUSH archives/YYYY-MM-DD vers FTP ===")
    daily_archive_and_push()
