from models.gestion_stocks import GestionStocks
from views.dashboard import Dashboard

gestionstock = GestionStocks()

app = Dashboard(gestionstock)

app.mainloop()