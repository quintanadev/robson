from services.data_integrator.db import get_db
from services.data_integrator.nicecxone.api import contact, dimensions

db = get_db()
dimensions = dimensions(db)
contact = contact(db)
print(dimensions)
print(contact)