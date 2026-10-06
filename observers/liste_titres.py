import tkinter as tk
from observers.observer import Observateur

class ListeTitres(Observateur):

    def __init__(self, parent):
        self._frame = parent

        self._listbox = tk.Listbox(
            parent,
            height=4,
            exportselection=False
        )

        self._listbox.pack(
            fill=tk.X,
            expand=True
        )

    def actualiser(self, sujet) -> None:
        self._listbox.delete(0, tk.END)

        # IMPORTANT : garder une liste interne des tickers
        self._tickers = list(sujet.titres.keys())

        for ticker, infos in sujet.titres.items():

            texte = (
                f"{ticker} — "
                f"{infos['quantite']} action(s) "
                f"(alerte : "
                f"{infos['seuil_bas']:.2f} $ / "
                f"{infos['seuil_haut']:.2f} $)"
            )

            self._listbox.insert(
                tk.END,
                texte
            )

    def get_selection(self):
        """Retourne le ticker sélectionné dans la Listbox."""
        selection = self._listbox.curselection()
        if not selection:
            return None

        index = selection[0]
        return self._tickers[index]


# ListeTitres.actualiser()
# - Récupère les titres depuis GestionStocks.
# - Met à jour la Listbox.
# - Affiche ticker, quantité et seuils.
