from models.subject import Sujet
import yfinance as yf



class GestionStocks(Sujet):
    
    def __init__(self):
        super().__init__()

        self.titres = {}
        
        self.prix_actuels = {}

        self._ajouter_titres_initiaux()
    

    def _ajouter_titres_initiaux(self):
        self.titres = {
            "AAPL": {
            "quantite": 10,
            "seuil_haut": 250,
            "seuil_bas": 150,
        },
        "MSFT": {
            "quantite": 5,
            "seuil_haut": 500,
            "seuil_bas": 300,
        },
    }


    def ajouter_titre(self):
        """Valide et ajoute un titre au portefeuille,
            puis notifie les observateurs."""
        ticker = self.entry_ticker.get().strip().upper()
        
        if not ticker:
            return
        if ticker in self.titres:
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

        self.titres[ticker] = {
            "quantite": quantite,
            "seuil_haut": round(seuil_haut if seuil_haut is not None else prix * 1.2, 2),
            "seuil_bas": round(seuil_bas if seuil_bas is not None else prix * 0.8, 2),
        }

        self.notifier()

       
    def retirer_titre(self):
        """Retire le titre sélectionné du portefeuille et notifie les observateurs."""
        selectionne = self._ticker_selectionne()
        if selectionne is None:
            self._statut("Sélectionnez un titre à retirer.", "orange")
            return
        _, ticker = selectionne

        #supression de la ligne
        del self.titres[ticker]

        self.notifier()
        
    
    def modifier_titre(self) -> None:
        """Modifie la quantité et les seuils du titre sélectionné,
            puis notifie les observateurs."""
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
        titre_info = self.titres[ticker]
        titre_info["quantite"] = quantite
        if seuil_bas is not None:
            titre_info["seuil_bas"] = seuil_bas
        if seuil_haut is not None:
            titre_info["seuil_haut"] = seuil_haut

        self.notifier()
        
    
    def rafraichir_prix(self) -> None:
        """Récupère les prix actuels et notifie les observateurs."""

        self.prix_actuels = {
            ticker: recuperer_prix(ticker)
            for ticker in self.titres
        }

        self.notifier()


            
    
    def get_donnees(self) -> dict:
        return {
            "titres": {
            ticker: {
                    "quantite": info["quantite"],
                    "seuil_haut": info["seuil_haut"],
                    "seuil_bas": info["seuil_bas"],
                }
                for ticker, info in self.titres.items()
            },
            "prix_actuels": self.prix_actuels,
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