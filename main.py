from models.gestion_stocks import GestionStock
from views.dashboard import Dashboard

gestionstock = GestionStock()

app = Dashboard(gestionstock)

app.mainloop()