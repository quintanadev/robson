import requests
import json
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from .auth import urls, auth

def contact(db):
  table_name = 'api_nicecontact'

  query = f"""
    SELECT SUBSTR(REPLACE(MAX(contactStart), 'T', ' '), 1, 19) AS contactStart
    FROM '{table_name}'
  """
  dt_updated = db.execute(query).fetchone()['contactStart']

  if dt_updated:
    first_date = datetime.strptime(dt_updated, "%Y-%m-%d %H:%M:%S") + relativedelta(minutes=-30)
    # first_date = date.today() + relativedelta(days=-3, hours=3)
    filter_date = first_date
  else:
    first_date = date.today() + relativedelta(days=0, hours=3)
  last_date = first_date + relativedelta(days=1, hour=3, minute=0, second=0)
  first_date = datetime.strftime(first_date, "%Y-%m-%dT%H:%M:%S.000Z")
  last_date = datetime.strftime(last_date, "%Y-%m-%dT%H:%M:%S.000Z")

  api_link = 'contacts/completed'
  query = '?startDate={}&endDate={}&top=10000'
  api = api_link + query.format(first_date, last_date)
  print(f"Executando api: {api_link} >>> De {first_date} até {last_date}")

  api_url = urls()['cxone'] + api
  headers = auth()
  columns = []
  data = []

  while api_url != None:
    print(f"URL >>> {api_url}")
    api_request = requests.get(api_url, headers=headers)
    if api_request.status_code == 200:
      dict_data = json.loads(api_request.text)

      for contact in dict_data.get('completedContacts'):
        columns = contact.keys()
        if len(contact) == 53:
          data.append(contact.values())
    
      api_url = dict_data['_links']['next']
    else:
      api_url = None
  
  if not data:
    return "Sem novos contatos..."
  
  df = pd.DataFrame(data, columns=columns)
  df = df.fillna('').astype(str)
  df = df.drop_duplicates(subset=['contactId'])

  try:
    if dt_updated:
      query = f"""
        SELECT contactId
        FROM '{table_name}'
        WHERE datetime(contactStart) >= '{filter_date}'
      """
      contacts = pd.read_sql_query(query, con=db, dtype={'contactId': str})
      contacts = contacts.fillna('').astype(str)
      df = df.merge(contacts, how='outer', on=['contactId'], indicator=True)
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
  except:
    msg = "Erro ao salvar contatos..."
  else:
    msg = "Contatos gravados na tabela..."
  return msg

def dimensions(db):
  apis = [
    {"api_link": "/dispositions", "table_name": "api_nicedisposition", "extract": "dispositions", "params": {}},
    {"api_link": "/dispositions/classifications", "table_name": "api_niceclassification", "extract": "classificationResults", "params": {}},
    {"api_link": "/skills", "table_name": "api_niceskill", "extract": "skills", "params": {"fields": "skillId,skillName,campaignId,campaignName,notes,scriptName,callSuppressionScriptId,agentless"}},
    {"api_link": "/agents", "table_name": "api_niceagent", "extract": "agents", "params": {"fields": "agentId,userName,firstName,lastName,teamId,teamName,lastLogin,profileName,notes,createDate,custom1,custom2,custom3,custom4,custom5", "isActive": "true"}},
  ]
  headers = auth()

  for x in apis:
    api_link = x["api_link"]
    table_name = x["table_name"]
    api_url = urls()["cxone"] + api_link

    columns = []
    data = []
    params = x["params"]

    print(f"Executando api: {api_link}")
    api_request = requests.get(api_url, params=params, headers=headers)
    dict_data = json.loads(api_request.text)
    
    for e in dict_data.get(x["extract"]):
      columns = e.keys()
      data.append(e.values())

    df = pd.DataFrame(data, columns=columns)
    try:
      for index, row in df.iterrows():
        try:
          df_row = row.to_frame().T
          df_row.to_sql(table_name, db, if_exists="append", index=False)
          db.commit()
        except Exception as e:
          pass
    except Exception as e:
      msg = f"Erro ao salvar contatos: {e}"
      print(msg)
    else:
      msg = f"Dados gravados na tabela..."
  return msg