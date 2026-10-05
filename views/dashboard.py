#importation de tk et des modules nécessaires

import tkinter as tk

from models.gestion_stocks import GestionStocks
from observers.affichage_alertes import AffichageAlertes
from observers.affichage_date_update import AffichageDateUpdate
from observers.liste_titres import ListeTitres
from observers.logger import Logger
from observers.prix_live import PrixLive
from observers.valeur_total import ValeurTotale


# Polices de l'interface
POLICE = ("Segoe UI", 10)
POLICE_TITRE = ("Segoe UI", 16, "bold")

class Dashboard(tk.Tk):

    INTERVALLE_ACTUALISATION = 30000  # Intervalle d'actualisation de 30 secondes

    def __init__(self, gestion_stocks: GestionStocks):
        super().__init__()
        
        self.title("Gestionnaire de Portfolio")
        self.resizable(False, False)
        
        self.option_add("*Font", POLICE)
        
        self._gestion_stocks = gestion_stocks

        self._creer_widgets()
        
        self._creer_observateurs()
        self._abonner_observateurs()

        self._cycle_actualisation()  # Démarrer le cycle d'actualisation
        
        
    def _champ(self, parent, texte, width, valeur_defaut=""):
        """Ajoute un couple Label + Entry à `parent` et retourne l'Entry."""
        tk.Label(parent, text=f"{texte}:").pack(side=tk.LEFT)
        entry = tk.Entry(parent, width=width)
        if valeur_defaut:
            entry.insert(0, valeur_defaut)
        entry.pack(side=tk.LEFT, padx=(2, 8))
        return entry
    
    def _creer_widgets(self):
        # Création des widgets de l'interface
        
        frame_principal = tk.Frame(self)
        frame_principal.pack(padx=10, pady=10)

        #========================
        # Titre de page
        #========================


        tk.Label(self, text="Portfolio Tracker", font=POLICE_TITRE).pack(pady=10)

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

        #Fait dans le fichier prix_live.py


        #========================
        # Contenu de Frame pour la gestion des titres
        #========================

        # Ligne d'ajout
        ligne_ajout = tk.Frame(self.frame_gestion)
        ligne_ajout.pack(fill=tk.X)

        self.entry_ticker = self._champ(ligne_ajout, "Ticker", width=8)
        self.entry_quantite = self._champ(ligne_ajout, "Qté", width=5, valeur_defaut="1")
        self.entry_seuil_bas = self._champ(ligne_ajout, "Alerte basse", width=7)
        self.entry_seuil_haut = self._champ(ligne_ajout, "Alerte haute", width=7)

        tk.Button(ligne_ajout, text="Ajouter", command=self._action_ajouter).pack(side=tk.LEFT)

        #Note pour utilisateur
        tk.Label(
                    self.frame_gestion,
                    text="(Alertes optionnelles : si vides, calculées à ±20% du prix actuel)",
                    font=("Segoe UI", 8), fg="gray"
                ).pack(anchor="w", pady=(2, 5))

       # Emplacement réservé pour la Listbox (créée par l'observer)
        self.frame_liste = tk.Frame(self.frame_gestion)
        self.frame_liste.pack(fill=tk.X)

        #Bouton de suppression
        tk.Button(self.frame_liste, text="Retirer", command=self._action_retirer).pack(side=tk.RIGHT, padx= 5, pady=5, anchor="n")
        

        
        # Ligne de modification

        ligne_modif = tk.Frame(self.frame_gestion)
        ligne_modif.pack(fill=tk.X, pady=(8, 0))

        tk.Label(ligne_modif, text="Sélection →").pack(side=tk.LEFT)

        self.entry_nouvelle_quantite = self._champ(ligne_modif, "Qté", width=5)
        self.entry_nouveau_seuil_bas = self._champ(ligne_modif, "Alerte basse", width=7)
        self.entry_nouveau_seuil_haut = self._champ(ligne_modif, "Alerte haute", width=7)

        tk.Button(ligne_modif, text="Modifier sélection", command=self._action_modifier).pack(side=tk.LEFT)



        #========================
        # Contenu de  Frame pour la valeur du portfolio
        #========================

        # Fait dans le fichier valeur_total.py


        #========================
        # Contenu de Frame pour les alertes
        #========================

        # Fait dans le fichier affichage_alertes.py

        #========================
        # Contenu de Frame pour la date de mise à jour
        #========================

        # Fait dans le fichier affichage_date_update.py    

    
    def _creer_observateurs(self):
        # Initiation des observateurs
        self._affichage_alerte = AffichageAlertes(self.frame_alertes)
        self._affichage_date_update = AffichageDateUpdate(self.frame_date)
        self._liste_titres = ListeTitres(self.frame_liste)
        self._logger = Logger("portfolio.csv")
        self._prix_live = PrixLive(self.frame_prix)
        self._valeur_totale = ValeurTotale(self.frame_portfolio)
    
    def _abonner_observateurs(self):
        # Abonnement des observateurs au sujet
        self._gestion_stocks.abonner(self._affichage_alerte)
        self._gestion_stocks.abonner(self._affichage_date_update)
        self._gestion_stocks.abonner(self._liste_titres)
        self._gestion_stocks.abonner(self._logger)
        self._gestion_stocks.abonner(self._prix_live)
        self._gestion_stocks.abonner(self._valeur_totale)


    #Fonction des bouttons

    def _action_ajouter(self):
        ticker = self.entry_ticker.get()
        quantite = self.entry_quantite.get()
        seuil_bas = self.entry_seuil_bas.get()
        seuil_haut = self.entry_seuil_haut.get()

        self._gestion_stocks.ajouter_titre(ticker, quantite, seuil_bas, seuil_haut)

    def _action_retirer(self):
        ticker = self._liste_titres.get_selection()
        self._gestion_stocks.retirer_titre(ticker)

    def _action_modifier(self):
        ticker = self._liste_titres.get_selection()
        quantite = self.entry_nouvelle_quantite.get()
        seuil_bas = self.entry_nouveau_seuil_bas.get()
        seuil_haut = self.entry_nouveau_seuil_haut.get()

        self._gestion_stocks.modifier_titre(ticker, quantite, seuil_bas, seuil_haut)

    # Methode pour le cycle d'actualisation
    def _cycle_actualisation(self):
        self._gestion_stocks.rafraichir()
        self.after(self.INTERVALLE_ACTUALISATION, self._cycle_actualisation)


    






        
        
        
        
        