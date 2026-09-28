from models.subject import Sujet
class GestionStocks(Sujet): 
    def __init__(self): 
        super().__init__() 
        pass 

    def ajouter_titre(self) -> None: 
        pass 

    def retirer_titre(self) -> None: 
        pass 

    def modifier_titre(self) -> None: 
        pass 

    def rafraichir_prix(self) -> None: 
        pass 

    def get_donnees(self) -> dict: 
        pass


# ajouter_titre() 
# # - Vérifie que le ticker n'existe pas déjà. 
# # - Valide la quantité et les seuils. 
# # - Vérifie que le ticker existe avec yfinance. 
# # - Ajoute le titre dans le portefeuille. 
# # - Définit les seuils à ±20% si non fournis. 
# # - Notifie les observateurs. 
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
# ajouter_titre() 
# # - Vérifie que le ticker n'existe pas déjà. 
# # - Valide la quantité et les seuils. 
# # - Vérifie que le ticker existe avec yfinance. 
# # - Ajoute le titre dans le portefeuille. 
# # - Définit les seuils à ±20% si non fournis. 
# # - Notifie les observateurs. 
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