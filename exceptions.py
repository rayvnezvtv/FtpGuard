# exceptions.py

class UnauthorizedAction(Exception):
    """Exception levée lorsqu'un utilisateur tente une action interdite."""
    pass

class InvalidPath(Exception):
    """Exception levée lorsqu'un chemin est invalide ou dangereux."""
    pass

class OperationFailed(Exception):
    """Exception levée lorsqu'une opération échoue (copie, suppression, etc.)."""
    pass
