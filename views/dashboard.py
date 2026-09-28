#importation de tk et des modules nécessaires

import tkinter as tk

from models.gestion_stocks import GestionStocks
from observers.affichage_alerte import AffichageAlerte
from observers.affichage_date_update import AffichageDateUpdate
from observers.liste_titres import ListeTitres
from observers.logger import Logger
from observers.prix_live import PrixLive
from observers.valeur_totale import ValeurTotale


class Dashboard(tk.Tk):

    INTERVALLE_ACTUALISATION = 3000  # Intervalle d'actualisation en millisecondes

    def __init__(self, gestion_stocks: GestionStocks):
        super().__init__()
        self.title("Gestionnaire de Portfolio")
        self.resizable(False, False)
        self._gestion_stocks = gestion_stocks
        
        self._creer_observateurs()
        self._abonner_observateurs()
        self._creer_widgets()

    
    def _creer_observateurs(self):
        # Initiation des observateurs
        self._affichage_alerte = AffichageAlerte(self)
        self._affichage_date_update = AffichageDateUpdate(self)
        self._liste_titres = ListeTitres(self)
        self._logger = Logger(self)
        self._prix_live = PrixLive(self)
        self._valeur_totale = ValeurTotale(self)
    
    def _abonner_observateurs(self):
        # Abonnement des observateurs au sujet
        self._gestion_stocks.abonner(self._affichage_alerte)
        self._gestion_stocks.abonner(self._affichage_date_update)
        self._gestion_stocks.abonner(self._liste_titres)
        self._gestion_stocks.abonner(self._logger)
        self._gestion_stocks.abonner(self._prix_live)
        self._gestion_stocks.abonner(self._valeur_totale)
    
    def _creer_widgets(self):
        # Création des widgets de l'interface
        
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10)

        
        
        
        
        