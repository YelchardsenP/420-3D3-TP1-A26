import tkinter as tk
from observers.observer import Observateur

class ValeurTotale(Observateur):
    
    def __init__(self, parent):
        pass

    def actualiser(self, sujet) -> None:
        pass

# ValeurTotale.actualiser()
# - Récupère les données du portefeuille.
# - Calcule la valeur totale.
# - Calcule la variation depuis l'ouverture.
# - Met à jour les Labels correspondants.