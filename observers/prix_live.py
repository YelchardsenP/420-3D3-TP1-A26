import tkinter as tk
from observers.observer import Observateur

class PrixLive(Observateur):
    
    def __init__(self, parent):
        self._frame = parent
        self._labels = {}

    def actualiser(self, sujet) -> None:
        donnees = sujet.get_donnees()

        prix_actuels = donnees["prix_actuels"]
        prix_ouverture = donnees["prix_ouverture"]

        # Supprimer les anciennes lignes
        for label in self._labels.values():
            label.destroy()

        self._labels.clear()

        # Créer une ligne pour chaque titre
        for ticker in prix_actuels:

            prix = prix_actuels[ticker]
            ouverture = prix_ouverture[ticker]

            variation = (prix - ouverture) / ouverture * 100

            symbole = "▲" if variation >= 0 else "▼"
            couleur = "green" if variation >= 0 else "red"

            label = tk.Label(
                self._frame,
                text=f"{ticker}: {prix:.2f} $ "
                     f"{symbole} {abs(variation):.2f}%",
                fg=couleur
            )

            label.pack(
                anchor="w",
                pady=2
            )

            self._labels[ticker] = label

# PrixLive.actualiser()
# - Récupère les prix actuels depuis GestionStocks.
# - Calcule la variation par rapport à l'ouverture.
# - Met à jour les Labels des prix.
# - Affiche vert si hausse, rouge si baisse.
