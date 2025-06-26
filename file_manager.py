# file_manager.py

import shutil
from pathlib import Path
from config import BASE_DIR
from logger import log_action, log_error

def list_directory(path: Path):
    """
    Liste les fichiers et dossiers dans un chemin donné.
    """
    try:
        return [item.name for item in path.iterdir()]
    except Exception as e:
        log_error(f"list_directory failed: {e}")
        return []

def create_folder(path: Path):
    """
    Crée un dossier à l'emplacement donné.
    """
    try:
        path.mkdir(parents=True, exist_ok=False)
        log_action("CREATE_FOLDER", str(path))
    except FileExistsError:
        log_action("CREATE_FOLDER", str(path), status="ALREADY EXISTS")
    except Exception as e:
        log_error(f"create_folder failed: {e}")

def create_file(path: Path):
    """
    Crée un fichier vide à l'emplacement donné.
    """
    try:
        if not path.exists():
            path.touch()
            log_action("CREATE_FILE", str(path))
        else:
            log_action("CREATE_FILE", str(path), status="ALREADY EXISTS")
    except Exception as e:
        log_error(f"create_file failed: {e}")

def delete_path(path: Path):
    """
    Supprime un fichier ou un dossier (récursivement).
    """
    try:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.is_file():
            path.unlink()
        log_action("DELETE", str(path))
    except Exception as e:
        log_error(f"delete_path failed: {e}")

def rename_path(path: Path, new_name: str):
    """
    Renomme un fichier ou dossier.
    """
    try:
        new_path = path.with_name(new_name)
        path.rename(new_path)
        log_action("RENAME", f"{path} -> {new_path}")
    except Exception as e:
        log_error(f"rename_path failed: {e}")

def copy_path(src: Path, dst: Path):
    """
    Copie un fichier ou un dossier à destination.
    """
    try:
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
        log_action("COPY", f"{src} -> {dst}")
    except Exception as e:
        log_error(f"copy_path failed: {e}")

def move_path(src: Path, dst: Path):
    """
    Déplace un fichier ou un dossier à destination.
    """
    try:
        shutil.move(str(src), str(dst))
        log_action("MOVE", f"{src} -> {dst}")
    except Exception as e:
        log_error(f"move_path failed: {e}")

def print_tree(path: Path, indent: str = ""):
    """
    Affiche récursivement toute l’arborescence depuis un chemin donné.
    """
    try:
        print(indent + f"📁 {path.name}")
        for item in path.iterdir():
            if item.is_dir():
                print_tree(item, indent + "    ")
            else:
                print(indent + "    " + f"📄 {item.name}")
    except Exception as e:
        log_error(f"print_tree failed: {e}")
