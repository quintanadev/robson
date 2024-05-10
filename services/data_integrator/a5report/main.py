import requests
import json
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from .auth import auth

def chamada(db):
  table_name = 'api_a5reportchamada'

  query = f"""
    SELECT
      MAX(datetime(
        concat_ws(' ',
          concat_ws('-',
            substr(inicioChamada, 7, 4),
            substr(inicioChamada, 4, 2),
            substr(inicioChamada, 1, 2)
          ),
          substr(inicioChamada, -8)
        )
      )) AS inicioChamada
    FROM '{table_name}'
  """
  dt_updated = db.execute(query).fetchone()['inicioChamada']
  print(dt_updated)

  if dt_updated:
    first_date = datetime.strptime(dt_updated, "%Y-%m-%d %H:%M:%S") + relativedelta(minutes=-30)
    # first_date = date.today() + relativedelta(days=-1, hour=0)
    filter_date = first_date
  else:
    first_date = date.today() + relativedelta(days=-1, hours=0)
  last_date = first_date + relativedelta(days=1, hour=0, minute=0, second=0)
  first_date = datetime.strftime(first_date, "%d/%m/%Y %H:%M:%S")
  last_date = datetime.strftime(last_date, "%d/%m/%Y %H:%M:%S")

  api_link = 'chamada/chamadaPorPeriodo'
  print(f"Executando api: {api_link} >>> De {first_date} até {last_date}")

  api_url = auth()['url'] + api_link
  headers = auth()['headers']
  json_body = {
    "inicioChamada": first_date,
    "terminoChamada": last_date,
  }
  columns = []
  data = []

  print(f"URL >>> {api_url}")
  api_request = requests.post(api_url, headers=headers, json=json_body)
  
  if api_request.status_code == 200:
    dict_data = json.loads(api_request.text)
    if len(dict_data) == 0:
      print("Sem novos contatos...")
      return False
    
    dict_columns = ['finalizacao', 'aplicacao', 'empresa']
    
    for chamada in dict_data:
      row = {}
      for key in chamada:
        if key in dict_columns:
          if isinstance(chamada.get(key), dict):
            for k, v in chamada.get(key).items():
              row[f"{key}_{k}"] = v
          else:
            row[f"{key}_id"] = None
            row[f"{key}_descricao"] = None
        else:
          row[f"{key}"] = chamada.get(key)
      data.append(row)
    columns = data[0].keys()

    df = pd.DataFrame(data, columns=columns, dtype=str)
    df = df.drop_duplicates(subset=['id'])

    try:
      if dt_updated:
        query = f"""
          SELECT id
          FROM '{table_name}'
          WHERE datetime(
            concat_ws(' ',
              concat_ws('-',
                substr(inicioChamada, 7, 4),
                substr(inicioChamada, 4, 2),
                substr(inicioChamada, 1, 2)
              ),
              substr(inicioChamada, -8)
            )
          ) >= '{filter_date}'
        """
        chamadas = pd.read_sql_query(query, con=db, dtype={'id': str})
        df = df.merge(chamadas, how='outer', on=['id'], indicator=True)
        df = df.query('_merge=="left_only"')
        df = df.drop('_merge', axis=1)
        qtd_registros = len(df)
        if qtd_registros > 0:
          print(f"Inserindo dados na tabela: {qtd_registros}")
          df.to_sql(table_name, db, if_exists='append', index=False)
          db.commit()
        else:
          print("Sem novos registros para gravar!")
      else:
        df.to_sql(table_name, db, if_exists='append', index=False)
    except Exception as e:
      print(f"Erro ao salvar contatos: {str(e)}")
    else:
      print("Contatos gravados na tabela...")
  return True
