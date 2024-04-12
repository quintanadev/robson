from services.data_integrator.db import get_db
from services.data_integrator.nicecxone.api import contact

db = get_db()
contact = contact(db)
print(contact)