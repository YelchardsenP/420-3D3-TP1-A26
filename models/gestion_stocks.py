from models.subject import Sujet
import yfinance as yf



class GestionStocks(Sujet):
    
    def __init__(self):
        super().__init__()
        pass
    
    def ajouter_titre(self):
        """Valide le formulaire d'ajout, vérifie que le ticker existe via yfinance,
        puis l'insère dans TITRES et dans l'UI (ligne de prix + liste)."""
        ticker = self.entry_ticker.get().strip().upper()
        if not ticker:
            return
        if ticker in TITRES:
            self._statut(f"{ticker} est déjà dans le portfolio.", "orange")
            return

        try:
            quantite = entier_positif(self.entry_quantite.get().strip())
        except ValueError:
            self._statut("La quantité doit être un nombre entier positif.", "red")
            return

        # Les seuils sont optionnels à l'ajout : s'ils sont vides, on les
        # calcule plus bas à ±20% du prix actuel une fois celui-ci connu.
        texte_bas = self.entry_seuil_bas_ajout.get().strip()
        texte_haut = self.entry_seuil_haut_ajout.get().strip()
        try:
            seuil_bas = flottant_positif(texte_bas) if texte_bas else None
            seuil_haut = flottant_positif(texte_haut) if texte_haut else None
        except ValueError:
            self._statut("Les alertes doivent être des nombres positifs.", "red")
            return
        if seuil_bas is not None and seuil_haut is not None and seuil_bas >= seuil_haut:
            self._statut("L'alerte basse doit être inférieure à l'alerte haute.", "red")
            return

        # Le ticker n'existe vraiment que si yfinance renvoie un prix
        try:
            prix, ouverture = recuperer_prix(ticker)
        except Exception:
            self._statut(f"Le titre '{ticker}' n'existe pas.", "red")
            return

        TITRES[ticker] = {
            "quantite": quantite,
            "seuil_haut": round(seuil_haut if seuil_haut is not None else prix * 1.2, 2),
            "seuil_bas": round(seuil_bas if seuil_bas is not None else prix * 0.8, 2),
        }

        # Mise à jour de l'UI : nouvelle ligne de prix, nouvelle entrée dans la
        # liste, puis réinitialisation du formulaire d'ajout
        self._creer_ligne_prix(ticker)
        self.listbox_titres.insert(tk.END, self._texte_listbox(ticker))
        for entry, valeur in (
            (self.entry_ticker, ""), (self.entry_quantite, "1"),
            (self.entry_seuil_bas_ajout, ""), (self.entry_seuil_haut_ajout, ""),
        ):
            entry.delete(0, tk.END)
            entry.insert(0, valeur)

        # Affiche le prix tout de suite plutôt que d'attendre le prochain
        # cycle de rafraîchir() (jusqu'à INTERVALLE_MS plus tard)
        texte, couleur = formater_prix(prix, ouverture)
        self.labels_prix[ticker].config(text=texte, fg=couleur)
        self._statut(f"{ticker} ajouté au portfolio ({quantite} action(s)).", "green")
    
    def retirer_titre(self):
        """Retire le titre sélectionné dans la liste : du portefeuille (TITRES),
        de la liste, et détruit sa ligne de prix."""
        selectionne = self._ticker_selectionne()
        if selectionne is None:
            self._statut("Sélectionnez un titre à retirer.", "orange")
            return
        index, ticker = selectionne

        self.listbox_titres.delete(index)
        del TITRES[ticker]
        self.labels_prix.pop(ticker, None)
        self.frames_prix.pop(ticker).destroy()

        self._statut(f"{ticker} retiré du portfolio.", "gray")
    
    def modifier_titre(self) -> None:
        """Modifie la quantité et/ou les seuils du titre sélectionné dans la liste.
        Vérifie que le ticker existe, que les nouvelles valeurs sont valides, puis
        met à jour TITRES et l'affichage de la liste."""
        selectionne = self._ticker_selectionne()
        if selectionne is None:
            self._statut("Sélectionnez un titre à modifier.", "orange")
            return
        index, ticker = selectionne

        try:
            quantite = entier_positif(self.entry_quantite.get().strip())
        except ValueError:
            self._statut("La quantité doit être un nombre entier positif.", "red")
            return

        texte_bas = self.entry_seuil_bas_modif.get().strip()
        texte_haut = self.entry_seuil_haut_modif.get().strip()
        try:
            seuil_bas = flottant_positif(texte_bas) if texte_bas else None
            seuil_haut = flottant_positif(texte_haut) if texte_haut else None
        except ValueError:
            self._statut("Les alertes doivent être des nombres positifs.", "red")
            return
        if seuil_bas is not None and seuil_haut is not None and seuil_bas >= seuil_haut:
            self._statut("L'alerte basse doit être inférieure à l'alerte haute.", "red")
            return

        # Mise à jour des données du titre dans TITRES
        titre_info = TITRES[ticker]
        titre_info["quantite"] = quantite
        if seuil_bas is not None:
            titre_info["seuil_bas"] = seuil_bas
        if seuil_haut is not None:
            titre_info["seuil_haut"] = seuil_haut

        # Mise à jour de l'affichage de la liste
        self.listbox_titres.delete(index)
        self.listbox_titres.insert(index, self._texte_listbox(ticker))
        self.listbox_titres.selection_set(index)

        self._statut(f"{ticker} modifié : {quantite} action(s), "
                     f"seuils {titre_info['seuil_bas']} / {titre_info['seuil_haut']}.", "green")
        
    
    def rafraichir_prix(self) -> None:
        """Cycle principal : récupère les prix de tous les titres, met à jour
        l'affichage de ceux-ci"""
        try:
            # 1. Récupération des prix actuels pour tous les titres du portefeuille
            prix_actuels = {ticker: recuperer_prix(ticker) for ticker in TITRES}

            # 2. Mise à jour de l'affichage prix/variation de chaque titre
            for ticker, (prix, ouverture) in prix_actuels.items():
                texte, couleur = formater_prix(prix, ouverture)
                self.labels_prix[ticker].config(text=texte, fg=couleur)

            # 3. Valeur totale du portefeuille et variation depuis l'ouverture
            valeur_totale = sum(prix * TITRES[t]["quantite"] for t, (prix, _) in prix_actuels.items())
            valeur_ouverture = sum(ouv * TITRES[t]["quantite"] for t, (_, ouv) in prix_actuels.items())
            variation_portfolio = valeur_totale - valeur_ouverture

            self.label_valeur.config(text=f"Valeur totale : {valeur_totale:.2f} $")
            symbole = "▲" if variation_portfolio >= 0 else "▼"
            self.label_variation.config(
                text=f"{symbole} {abs(variation_portfolio):.2f} $ depuis l'ouverture",
                fg="green" if variation_portfolio >= 0 else "red",
            )
    
    def get_donnees(self) -> dict:
        donnees = {
            "titres": {
                ticker: {
                    "quantite": info["quantite"],
                    "seuil_haut": info["seuil_haut"],
                    "seuil_bas": info["seuil_bas"],
                }
                for ticker, info in TITRES.items()
            },
            "prix_actuels": {
                ticker: self.labels_prix[ticker].cget("text")
                for ticker in TITRES
            },
        }


# ajouter_titre()
# - Vérifie que le ticker n'existe pas déjà.
# - Valide la quantité et les seuils.
# - Vérifie que le ticker existe avec yfinance.
# - Ajoute le titre dans le portefeuille.
# - Définit les seuils à ±20% si non fournis.
# - Notifie les observateurs.

# retirer_titre()
# - Vérifie que le ticker existe.
# - Supprime le titre du portefeuille.
# - Supprime ses prix enregistrés.
# - Notifie les observateurs.

# modifier_titre()
# - Vérifie que le ticker existe.
# - Modifie la quantité et/ou les seuils fournis.
# - Vérifie que les nouvelles valeurs sont valides.
# - Notifie les observateurs.

# rafraichir_prix()
# - Récupère les prix actuels de tous les titres avec yfinance.
# - Met à jour les prix enregistrés.
# - Notifie les observateurs pour qu'ils mettent l'interface à jour.

# get_donnees()
# - Retourne un dictionnaire contenant les données du portefeuille.
# - Inclut les titres, les prix actuels et les prix d'ouverture.
# - Permet aux observateurs d'accéder aux données sans modifier GestionStocks.