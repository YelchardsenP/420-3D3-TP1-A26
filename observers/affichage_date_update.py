import tkinter as tk
from datetime import datetime
from observers.observer import Observateur


class AffichageDateUpdate(Observateur):

    def __init__(self, parent):
        self._label = tk.Label(
            parent,
            text="Dernière mise à jour :",
            fg="gray"
        )

        self._label.pack(pady=5)

    def actualiser(self, sujet) -> None:

        date_heure = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        self._label.config(
            text=f"Dernière mise à jour : {date_heure}"
        )

# AffichageDateUpdate.actualiser()
# - Récupère la date et l'heure actuelles.
# - Met à jour le Label de dernière mise à jour.