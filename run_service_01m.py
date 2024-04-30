import time

from services.data_integrator.db import get_db
from services.data_integrator.nicecxone.main import contact, dimensions

starttime = time.time()
while True:
  try:
    timehour = int(time.strftime("%H"))
    timeminute = int(time.strftime("%M"))
    if (timehour >= 8 and timehour <= 22):
      timenow = time.strftime("%H:%M")
      print(f"Iniciando o processo: {timenow}")

      db = get_db()
      if timehour in (9, 12, 18) and timeminute == 0:
        dimensions(db)
      contact(db)
      
      timenow = time.strftime("%H:%M")
      print(f"Processo finalizado: {timenow}")
    else:
      print("Fora do horário de operação...")
  except Exception as e:
    print("Erro no processo! Aguardando 1 minuto para nova tentativa...")
    print(str(e))
    time.sleep(120.0 - ((time.time() - starttime) % 120.0))
  else:
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))