import tkinter as tk
from observers.observer import Observateur

class PrixLive(Observateur):
    
    def __init__(self, parent):
        pass

    def actualiser(self, sujet) -> None:
        pass

# PrixLive.actualiser()
# - Récupère les prix actuels depuis GestionStocks.
# - Calcule la variation par rapport à l'ouverture.
# - Met à jour les Labels des prix.
# - Affiche vert si hausse, rouge si baisse.
