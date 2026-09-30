#importation de tk et des modules nécessaires

import tkinter as tk

from models.gestion_stocks import GestionStocks
from observers.affichage_alertes import AffichageAlerte
from observers.affichage_date_update import AffichageDateUpdate
from observers.liste_titres import ListeTitres
from observers.logger import Logger
from observers.prix_live import PrixLive
from observers.valeur_total import ValeurTotale


# Polices de l'interface
POLICE = ("Segoe UI", 10)
POLICE_TITRE = ("Segoe UI", 16, "bold")

class Dashboard(tk.Tk):

    INTERVALLE_ACTUALISATION = 3000  # Intervalle d'actualisation en millisecondes

    def __init__(self, gestion_stocks: GestionStocks):
        super().__init__()
        
        self.title("Gestionnaire de Portfolio")
        self.resizable(False, False)
        
        self.fenetre.option_add("*Font", POLICE)
        
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
        
        frame_principal = tk.Frame(self)
        frame_principal.pack(padx=10, pady=10)

        #========================
        # Titre de page
        #========================


        tk.Label(self.fenetre, text="Portfolio Tracker", font=POLICE_TITRE).pack(pady=10)

        #========================
        # Creation des frames
        #========================

        
        self.frame_prix = tk.LabelFrame(self, text="Prix en temps réel", padx=10, pady=10)
        self.frame_prix.pack(fill=tk.X, padx=10, pady=5)
        
        self.frame_gestion = tk.LabelFrame(self, text="Gérer les titres", padx=10, pady=10)
        self.frame_gestion.pack(fill=tk.X, padx=10, pady=5)
        
        self.frame_portfolio = tk.LabelFrame(self, text="Mon portfolio", padx=10, pady=10)
        self.frame_portfolio.pack(fill=tk.X, padx=10, pady=5)
        
        self.frame_alertes = tk.LabelFrame(self, text="Alertes", padx=10, pady=10)
        self.frame_alertes.pack(fill=tk.X, padx=10, pady=5)
        
        self.frame_date = tk.Frame(self)
        self.frame_date.pack(fill=tk.X, padx=10, pady=5)

        #========================
        # Contenu de Frame pour le prix en temps réel
        #========================




        #========================
        # Contenu de Frame pour la gestion des titres
        #========================

        #========================
        # Contenu de  Frame pour la valeur du portfolio
        #========================

        #========================
        # Contenu de Frame pour les alertes
        #========================

        #========================
        # Contenu de Frame pour la date de mise à jour
        #========================





        
        
        
        
        