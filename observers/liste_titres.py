import tkinter as tk
from observers.observer import Observateur

class ListeTitres(Observateur):
    
    def __init__(self, parent):
        pass

    def actualiser(self, sujet) -> None:
        pass

# ListeTitres.actualiser()
# - Récupère les titres depuis GestionStocks.
# - Met à jour la Listbox.
# - Affiche ticker, quantité et seuils.
