from subject import Sujet
import yfinance as yf

class GestionStocks(Sujet):
    
    def __init__(self):
        super().__init__()

        self.titres = {}
        self.prix_actuels = {}

        self._ajouter_titres_initiaux()
    
    def _ajouter_titres_initiaux(self):
        self.titres = {
            "AAPL": {"quantite": 10, "seuil_haut": 250, "seuil_bas": 150},
            "MSFT": {"quantite": 5, "seuil_haut": 500, "seuil_bas": 300}
        }

    # Recuperation des prix
    def _recuperer_prix(self, ticker):
        info = yf.Ticker(ticker).fast_info or {}
        prix = info.get("last_price")
        ouverture = info.get("open")

        if prix is None:
            raise ValueError(f"Le titre '{ticker}' n'existe pas.")

        return prix, ouverture

    # Methodes privées pour modifer texte en entier ou flottant positif
    def _entier_positif(self, texte):
        valeur = int(texte)
        if valeur <= 0:
            raise ValueError
        return valeur

    def _flottant_positif(self, texte):
        valeur = float(texte)
        if valeur <= 0:
            raise ValueError
        return valeur


    def ajouter_titre(self, ticker, quantite, seuil_bas=None, seuil_haut=None):

        # defintion ticket
        ticker = ticker.upper()

        if ticker in self.titres:
            raise ValueError(f"{ticker} est déjà dans le portefeuille.")

        quantite = self._entier_positif(quantite)

        # Validation des seuils
        if seuil_bas in ("", None):
            seuil_bas = None
        else:
            seuil_bas = self._flottant_positif(seuil_bas)

        if seuil_haut in ("", None):
            seuil_haut = None
        else:
            seuil_haut = self._flottant_positif(seuil_haut)

        if seuil_bas is not None and seuil_haut is not None and seuil_bas >= seuil_haut:
            raise ValueError("Le seuil bas doit être inférieur au seuil haut.")

        

        # Récupération du prix actuel et du prix d'ouverture
        prix, ouverture = self._recuperer_prix(ticker)

        # Ajout du titre au portefeuille avec les seuils par défaut si non fournis
        self.titres[ticker] = {
            "quantite": quantite,
            "seuil_haut": round(seuil_haut if seuil_haut else prix * 1.2, 2),
            "seuil_bas": round(seuil_bas if seuil_bas else prix * 0.8, 2),
        }
        

        self.notifier()


    def retirer_titre(self, ticker):

        # defintion ticket
        ticker = ticker.upper()

        if ticker not in self.titres:
            raise ValueError(f"{ticker} n'est pas dans le portefeuille.")

        # Suppression du titre et de ses prix
        del self.titres[ticker]
        
        self.notifier()
        

    def modifier_titre(self, ticker, quantite=None, seuil_bas=None, seuil_haut=None):

        # defintion ticket
        ticker = ticker.upper()

        if ticker not in self.titres:
            raise ValueError(f"{ticker} n'existe pas.")

        
        titre_info = self.titres[ticker]

        # Validation des nouvelles valeurs
        if quantite is not None:
            titre_info["quantite"] = self._entier_positif(quantite)

        if seuil_bas is not None:
            titre_info["seuil_bas"] = self._flottant_positif(seuil_bas)

        if seuil_haut is not None:
            titre_info["seuil_haut"] = self._flottant_positif(seuil_haut)

        if titre_info["seuil_bas"] >= titre_info["seuil_haut"]:
            raise ValueError("Le seuil bas doit être inférieur au seuil haut.")

        self.notifier()


    def rafraichir_prix(self):

        # Récupération des prix actuels pour tous les titres
        self.prix_actuels = {
            ticker: self._recuperer_prix(ticker)
            for ticker in self.titres
        }
        self.notifier()


    def get_donnees(self):

        # Construction du dictionnaire de données à retourner
        donnees = {
            ## Titres avec leurs quantités et seuils
            "titres": {
                ticker: {
                    "quantite": data["quantite"],
                    "seuil_haut": data["seuil_haut"],
                    "seuil_bas": data["seuil_bas"],
                }
                for ticker, data in self.titres.items()
            },

            # prix actuels
            "prix_actuels": {
                ticker: prix[0]   # prix actuel
                for ticker, prix in self.prix_actuels.items()
            },

            # prix d’ouverture
            "prix_ouverture": {
                ticker: prix[1]   # prix ouverture
                for ticker, prix in self.prix_actuels.items()
            }
        }
    
        return donnees

#---------------------------------
#------Notes des méthodes---------
#---------------------------------

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