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
        for frame in self._labels.values():
            frame.destroy()

        self._labels.clear()

        # Créer une ligne pour chaque titre
        for ticker in prix_actuels:

            prix = prix_actuels[ticker]
            ouverture = prix_ouverture[ticker]

            variation = (prix - ouverture) / ouverture * 100
            symbole = "▲" if variation >= 0 else "▼"
            couleur = "green" if variation >= 0 else "red"

            # --- Créer une ligne (frame) ---
            ligne = tk.Frame(self._frame)
            ligne.pack(fill=tk.X, pady=2)

            # --- Ticker en noir ---
            tk.Label(
                ligne,
                text=f"{ticker}:",
                width=8,
                font=("Segoe UI", 10, "bold"),
                anchor="w",
                fg="black"
            ).pack(side=tk.LEFT)

            # --- Prix + variation en couleur ---
            tk.Label(
                ligne,
                text=f"{prix:.2f} $ {symbole} {abs(variation):.2f}%",
                fg=couleur
            ).pack(side=tk.LEFT)

            # Stocker la ligne entière
            self._labels[ticker] = ligne


# PrixLive.actualiser()
# - Récupère les prix actuels depuis GestionStocks.
# - Calcule la variation par rapport à l'ouverture.
# - Met à jour les Labels des prix.
# - Affiche vert si hausse, rouge si baisse.
