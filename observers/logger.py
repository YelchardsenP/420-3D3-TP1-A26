import tkinter as tk
from observers.observer import Observateur

class Logger(Observateur):
    
    def __init__(self, fichier : portfolio.csv ):
        pass

    def actualiser(self, sujet) -> None:
        pass


# Logger.actualiser()
# - Récupère les prix actuels.
# - Récupère la date et l'heure.
# - Ajoute les données dans portfolio.csv.