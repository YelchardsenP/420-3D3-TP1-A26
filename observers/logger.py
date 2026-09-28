from datetime import datetime
from observers.observer import Observateur


class Logger(Observateur):

    def __init__(self, fichier="portfolio.csv"):
        self._fichier = fichier

    def actualiser(self, sujet) -> None:

        donnees = sujet.get_donnees()

        prix_actuels = donnees["prix_actuels"]
        prix_ouverture = donnees["prix_ouverture"]

        date_heure = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        with open(self._fichier, "a") as fichier:

            for ticker in prix_actuels:

                prix = prix_actuels[ticker]
                ouverture = prix_ouverture[ticker]

                fichier.write(
                    f"{date_heure},"
                    f"{ticker},"
                    f"{prix:.2f},"
                    f"{ouverture:.2f}\n"
                )


# Logger.actualiser()
# - Récupère les prix actuels.
# - Récupère la date et l'heure.
# - Ajoute les données dans portfolio.csv.