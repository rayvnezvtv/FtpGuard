# file_manager.py

import shutil
import datetime
from pathlib import Path
from config import BASE_DIR
from logger import log_action, log_error
from exceptions import UnauthorizedAction
from security import show_result

def check_access(path: Path, user_path: Path):
    """Vérifie si l'utilisateur a le droit d'accéder au chemin demandé."""
    if not str(path.resolve()).startswith(str(user_path.resolve())):
        raise UnauthorizedAction("Accès interdit hors de votre périmètre.")

def list_directory(path: Path):
    try:
        return [item.name for item in path.iterdir()]
    except Exception as e:
        log_error(f"list_directory failed: {e}")
        return []

def create_folder(path: Path, user, user_path):
    try:
        check_access(path, user_path)
        path.mkdir(parents=True, exist_ok=False)
        log_action("CREATE_FOLDER", str(path), user=user)
        show_result(True, "Dossier créé.")
    except FileExistsError:
        log_action("CREATE_FOLDER", str(path), status="ALREADY EXISTS", user=user)
        show_result(False, "Le dossier existe déjà.")
    except UnauthorizedAction as e:
        log_error(str(e), user)
        show_result(False, str(e))
    except Exception as e:
        log_error(f"create_folder failed: {e}", user)
        show_result(False, str(e))

def create_file(path: Path, user, user_path):
    try:
        check_access(path, user_path)
        if not path.exists():
            path.touch()
            log_action("CREATE_FILE", str(path), user=user)
            show_result(True, "Fichier créé.")
        else:
            log_action("CREATE_FILE", str(path), status="ALREADY EXISTS", user=user)
            show_result(False, "Le fichier existe déjà.")
    except UnauthorizedAction as e:
        log_error(str(e), user)
        show_result(False, str(e))
    except Exception as e:
        log_error(f"create_file failed: {e}", user)
        show_result(False, str(e))

def delete_path(path: Path, user, user_path):
    try:
        check_access(path, user_path)
        if path.is_dir():
            shutil.rmtree(path)
        elif path.is_file():
            path.unlink()
        log_action("DELETE", str(path), user=user)
        show_result(True, "Suppression réussie.")
    except UnauthorizedAction as e:
        log_error(str(e), user)
        show_result(False, str(e))
    except Exception as e:
        log_error(f"delete_path failed: {e}", user)
        show_result(False, str(e))

def rename_path(path: Path, new_name: str, user, user_path):
    try:
        check_access(path, user_path)
        new_path = path.with_name(new_name)
        path.rename(new_path)
        log_action("RENAME", f"{path} -> {new_path}", user=user)
        show_result(True, "Renommé avec succès.")
    except UnauthorizedAction as e:
        log_error(str(e), user)
        show_result(False, str(e))
    except Exception as e:
        log_error(f"rename_path failed: {e}", user)
        show_result(False, str(e))

def print_tree(path: Path, indent: str = ""):
    try:
        print(indent + f"📁 {path.name}")
        for item in path.iterdir():
            if item.is_dir():
                print_tree(item, indent + "    ")
            else:
                print(indent + "    " + f"📄 {item.name}")
    except Exception as e:
        log_error(f"print_tree failed: {e}")
        show_result(False, "Erreur d'affichage de l'arborescence.")

def archive_audit_files(client_path: Path, user=None):
    """Archive les fichiers audit.* du dossier client dans un sous-dossier daté."""
    try:
        today = datetime.date.today().isoformat()  # YYYY-MM-DD
        archive_dir = client_path / "archives" / today
        archive_dir.mkdir(parents=True, exist_ok=True)

        for file in client_path.iterdir():
            if file.is_file() and file.name.startswith("audit."):
                shutil.copy2(file, archive_dir)
                log_action("ARCHIVE_FILE", f"{file} -> {archive_dir}", user=user)

        show_result(True, f"Fichiers d’audit archivés dans {archive_dir}")
    except Exception as e:
        log_error(f"archive_audit_files failed: {e}", user)
        show_result(False, str(e))
