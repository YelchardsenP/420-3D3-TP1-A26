import tkinter as tk
from observers.observer import Observateur


class AffichageAlertes(Observateur):

    def __init__(self, parent):
        self._label = tk.Label(
            parent,
            text="Aucune alerte",
            fg="gray",
            justify=tk.LEFT,
            wraplength=380
        )

        self._label.pack(anchor="w")

    def actualiser(self, sujet) -> None:

        donnees = sujet.get_donnees()

        titres = donnees["titres"]
        prix_actuels = donnees["prix_actuels"]

        alertes = []

        for ticker in titres:

            prix = prix_actuels[ticker]

            seuil_bas = titres[ticker]["seuil_bas"]
            seuil_haut = titres[ticker]["seuil_haut"]

            if prix >= seuil_haut:

                alertes.append(
                    f"⚠️ {ticker} dépasse le seuil haut "
                    f"({prix:.2f} $ ≥ {seuil_haut:.2f} $)"
                )

            elif prix <= seuil_bas:

                alertes.append(
                    f"⚠️ {ticker} sous le seuil bas "
                    f"({prix:.2f} $ ≤ {seuil_bas:.2f} $)"
                )

        if alertes:

            self._label.config(
                text="\n".join(alertes),
                fg="red"
            )

        else:

            self._label.config(
                text="Aucune alerte",
                fg="gray"
            )

# AffichageAlertes.actualiser()
# - Vérifie les seuils des titres.
# - Récupère les alertes déclenchées.
# - Affiche les alertes dans le Label.
# - Affiche "Aucune alerte" s'il n'y en a pas.