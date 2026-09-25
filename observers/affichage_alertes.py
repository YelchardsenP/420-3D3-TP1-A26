import tkinter as tk
from observers.observer import Observateur

class AffichageAlertes(Observateur):
    
    def __init__(self, parent):
        pass

    def actualiser(self, sujet) -> None:
        pass

# AffichageAlertes.actualiser()
# - Vérifie les seuils des titres.
# - Récupère les alertes déclenchées.
# - Affiche les alertes dans le Label.
# - Affiche "Aucune alerte" s'il n'y en a pas.