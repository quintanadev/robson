import pandas as pd
import requests
import urllib3
import json
import uuid
from pathlib import Path
from datetime import date, datetime

from services.data_integrator.takeblip.auth import auth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_whatsapp_tabulacoes():
  file_path = Path.cwd() / 'whatsapp_tabulacoes.csv'
  dtype = {
    "tabulacao": str,
    "tipo": str
  }
  df = pd.read_csv(file_path, sep="|", dtype=dtype, index_col=False, decimal=",")

  return df

def get_tickets_times():
  infos = auth()
  url = infos["url"]
  headers = infos["auth-human"]
  request_id = str(uuid.uuid4())
  body = {
    "id": request_id,
    "to": "postmaster@desk.msging.net",
    "method": "get",
    "uri": "/monitoring/ticket-metrics?version=2&$take=500&$skip=0&refreshCache=true"
  }

  api_request = requests.post(url, json=body, headers=headers, verify=False)
  dict_data = json.loads(api_request.text)
  data = dict_data.get("resource")
  return data

def get_tickets_agents():
  infos = auth()
  url = infos["url"]
  headers = infos["auth-human"]
  request_id = str(uuid.uuid4())
  body = {
    "id": request_id,
    "to": "postmaster@desk.msging.net",
    "method": "get",
    "uri": "/monitoring/attendants?version=2&$take=500&$skip=0&refreshCache=true"
  }

  api_request = requests.post(url, json=body, headers=headers, verify=False)
  dict_data = json.loads(api_request.text)

  df = pd.DataFrame()
  for e in dict_data.get("resource").get("items"):
    df_row = pd.DataFrame([e.values()], columns=e.keys())
    df = pd.concat([df, df_row], ignore_index=True)
  df = df.loc[df["status"] != "Offline"]

  data = {
    "maxOpenedTickets": f'{df["openedTickets"].max()}',
    "minOpenedTickets": f'{df["openedTickets"].min()}',
    "maxClosedTickets": f'{df["closedTickets"].max()}',
    "minClosedTickets": f'{df["closedTickets"].min()}'
  }
  return data

def get_tickets_tags():
  infos = auth()
  url = infos["url"]
  headers = infos["auth-human"]
  request_id = str(uuid.uuid4())
  body = {
    "id": request_id,
    "to": "postmaster@desk.msging.net",
    "method": "get",
    "uri": "/monitoring/tags-metrics?version=2&$take=500&$skip=0&refreshCache=true"
  }

  api_request = requests.post(url, json=body, headers=headers, verify=False)
  dict_data = json.loads(api_request.text)
  
  df_tab = get_whatsapp_tabulacoes()
  df = pd.DataFrame()
  for e in dict_data.get("resource").get("items"):
    df_row = pd.DataFrame([e.values()], columns=e.keys())
    df = pd.concat([df, df_row], ignore_index=True)
  df["name"] = df["name"].str.upper().str.strip()
  df = df.merge(df_tab, how="left", left_on=["name"], right_on=["tabulacao"])

  data = {
    "ticketsCpc": f'{df.loc[df["tipo"] == "CPC"]["closedTickets"].sum()}',
    "ticketsTarget": f'{df.loc[df["tipo"] == "TARGET"]["closedTickets"].sum()}',
    "ticketsNegocio": f'{df.loc[df["tipo"] == "SUCESSO"]["closedTickets"].sum()}',
  }
  return data

def get_contacts_bot():
  infos = auth()
  url = infos["url"]
  headers = infos["auth-router"]
  request_id = str(uuid.uuid4())
  
  filter_date = datetime.strftime(date.today(), "%Y-%m-%d")

  body = {
    "id": request_id,
    "to": "postmaster@analytics.msging.net",
    "method": "get",
    "uri": f"/metrics/active-identity-quantity?startDate={filter_date}&endDate={filter_date}&$take=1000"
  }

  api_request = requests.post(url, json=body, headers=headers, verify=False)
  dict_data = json.loads(api_request.text)
  data = dict_data.get("resource")
  return {
    "contactsBot": f'{data["count"]}'
  }

def get_nps():
  infos = auth()
  url = infos["url"]
  headers = infos["auth-router"]
  request_id = str(uuid.uuid4())

  filter_date = datetime.strftime(date.today(), "%Y-%m-%d")

  body = {
    "id": request_id,
    "to": "postmaster@analytics.msging.net",
    "method": "get",
    "uri": f"/event-track/NPS%20Atendimento%20Humano%20-%20Nota?startDate={filter_date}&endDate={filter_date}&$take=1000"
  }

  api_request = requests.post(url, json=body, headers=headers, verify=False)
  dict_data = json.loads(api_request.text)
  # data = dict_data.get("resource").get("items")

  df = pd.DataFrame()
  for e in dict_data.get("resource").get("items"):
    df_row = pd.DataFrame([e.values()], columns=e.keys())
    df = pd.concat([df, df_row], ignore_index=True)
  
  if len(df) > 0:
    df = df.loc[df["action"].isin(['0','1','2','3','4','5','6','7','8','9','10'])]
    total_notas = df["count"].sum()
    df = pd.pivot_table(df, values="count", index=["storageDate"], columns=["action"])

    df = df.rename(columns={"0": "nota_00", "1": "nota_01", "2": "nota_02", "3": "nota_03", "4": "nota_04", "5": "nota_05",
                          "6": "nota_06", "7": "nota_07", "8": "nota_08", "9": "nota_09", "10": "nota_10"})
    df["nota_total"] = total_notas
  data = df.to_json(orient='records')

  try:
    return json.loads(data)[0]
  except:
    return {}

def get_agents_status_blip():
  infos = auth()
  url = infos["url"]
  headers = infos["auth-human"]
  request_id = str(uuid.uuid4())
  body = {
    "id": request_id,
    "to": "postmaster@desk.msging.net",
    "method": "get",
    "uri": "/monitoring/attendant-status-metrics?version=2&$take=500&$skip=0&refreshCache=true"
  }

  api_request = requests.post(url, json=body, headers=headers, verify=False)
  dict_data = json.loads(api_request.text)
  data = dict_data.get("resource")
  return data

def get_tickets_status_blip():
  infos = auth()
  url = infos["url"]
  headers = infos["auth-human"]
  request_id = str(uuid.uuid4())
  body = {
    "id": request_id,
    "to": "postmaster@desk.msging.net",
    "method": "get",
    "uri": "/monitoring/tickets?version=2"
  }

  api_request = requests.post(url, json=body, headers=headers, verify=False)
  dict_data = json.loads(api_request.text)
  data = dict_data.get("resource")
  return data