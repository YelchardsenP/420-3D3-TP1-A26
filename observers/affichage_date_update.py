import tkinter as tk
from observers.observer import Observateur

class AffichageDateUpdate(Observateur):
    
    def __init__(self, parent):
        pass

    def actualiser(self, sujet) -> None:
        pass

# AffichageDateUpdate.actualiser()
# - Récupère la date et l'heure actuelles.
# - Met à jour le Label de dernière mise à jour.