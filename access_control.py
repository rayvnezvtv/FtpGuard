# access_control.py

def is_admin(role: str) -> bool:
    """
    Vérifie si le rôle donné est celui d’un administrateur.
    """
    return role.lower() in ["admin", "superadmin", "super", "1"]

def can_delete(role: str) -> bool:
    """
    Vérifie si ce rôle a le droit de supprimer.
    """
    return is_admin(role)

def can_rename(role: str) -> bool:
    """
    Vérifie si ce rôle peut renommer des fichiers/dossiers.
    """
    return is_admin(role)

def can_modify(role: str) -> bool:
    """
    Vérifie si le rôle peut modifier (copier/déplacer/ajouter).
    """
    return is_admin(role)

def can_upload(role: str) -> bool:
    """
    Tous les utilisateurs peuvent uploader vers le FTP.
    """
    return True

def role_label(role: str) -> str:
    """
    Donne un label propre pour l'affichage du rôle.
    """
    return "Super Admin" if is_admin(role) else "Utilisateur"
