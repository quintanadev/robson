import time

from services.data_integrator.db import get_db
from services.data_integrator.portalrealize.main import get_encerradas

starttime = time.time()
seconds_update = 900.0
while True:
  try:
    timehour = int(time.strftime("%H"))
    timeminute = int(time.strftime("%M"))
    if (timehour >= 9 and timehour <= 21):
      timenow = time.strftime("%H:%M")
      print(f"Iniciando o processo: {timenow}")

      db = get_db()
      get_encerradas(db)
      
      timenow = time.strftime("%H:%M")
      print(f"Processo finalizado: {timenow}")
    else:
      seconds_update = 86400.0 * (8.0 - timehour + 1.0)
      print("Fora do horário de operação...")
  except Exception as e:
    print("Erro no processo! Aguardando 1 minuto para nova tentativa...")
    print(str(e))
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
  else:
    time.sleep(seconds_update - ((time.time() - starttime) % seconds_update))