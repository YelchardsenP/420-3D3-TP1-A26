import tkinter as tk
from observers.observer import Observateur

POLICE_VALEUR = ("Segoe UI", 13, "bold")

class ValeurTotale(Observateur):

    def __init__(self, parent):
        self._label = tk.Label(
            parent,
            text="Valeur totale : calcul en cours...",
            font=POLICE_VALEUR,
        )
        self._label.pack()

        self._label_variation = tk.Label(
            parent,
            text=""
        )
        self._label_variation.pack()

    def actualiser(self, sujet) -> None:

        donnees = sujet.get_donnees()

        titres = donnees["titres"]
        prix_actuels = donnees["prix_actuels"]
        prix_ouverture = donnees["prix_ouverture"]

        valeur_totale = 0
        valeur_ouverture = 0

        for ticker in titres:

            quantite = titres[ticker]["quantite"]

            prix = prix_actuels[ticker]
            ouverture = prix_ouverture[ticker]

            valeur_totale += prix * quantite
            valeur_ouverture += ouverture * quantite

        variation = valeur_totale - valeur_ouverture

        self._label.config(
            text=f"Valeur totale : {valeur_totale:.2f} $"
        )

        symbole = "▲" if variation >= 0 else "▼"
        couleur = "green" if variation >= 0 else "red"

        self._label_variation.config(
            text=f"{symbole} {abs(variation):.2f} $ depuis l'ouverture",
            fg=couleur
        )

# ValeurTotale.actualiser()
# - Récupère les données du portefeuille.
# - Calcule la valeur totale.
# - Calcule la variation depuis l'ouverture.
# - Met à jour les Labels correspondants.