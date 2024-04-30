import requests
import pandas as pd
import json
from pathlib import Path
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from services.data_integrator.nicecxone.auth import auth, urls

def get_sla_skill_summary():
  headers = auth()
  first_date = date.today() + relativedelta(days=0, hours=3)
  last_date = first_date + relativedelta(days=1)
  first_date = datetime.strftime(first_date, "%Y-%m-%dT%H:%M:%S.000Z")
  last_date = datetime.strftime(last_date, "%Y-%m-%dT%H:%M:%S.000Z")
 
  api_link = '/skills/activity'
  api_url = urls()["cxone"] + api_link
  params = {
    "isOutbound": "false"
  }
  api_request = requests.get(api_url, headers=headers, params=params)
  dict_data = json.loads(api_request.text)
 
  columns = []
  data = []
  for e in dict_data.get('skillActivity'):
    columns = e.keys()
    data.append(e.values())
 
  df_activity = pd.DataFrame(data, columns=columns)
  # df_activity = df_activity.fillna('').astype(str)
  df_activity["serverTime"] = df_activity["serverTime"].apply(lambda x: pd.Timestamp(x, tz="UTC").tz_convert(tz="America/Sao_Paulo"))
  df_activity["earliestQueueTime"] = df_activity["earliestQueueTime"].apply(lambda x: pd.Timestamp(x, tz="UTC").tz_convert(tz="America/Sao_Paulo"))
  df_activity = df_activity[["skillId", "skillName", "campaignId", "campaignName", "serverTime", "skillQueueCount", "earliestQueueTime", "contactsActive", "agentsLoggedIn", "agentsWorking", "agentsUnavailable", "agentsAvailable", "agentsACW", "agentsIdle"]]
  df_activity = df_activity.loc[df_activity["skillName"].isin(["RECEPTIVO 4004", "RECEPTIVO LOJAS", "RECEPTIVO AGENTE DIGITAL"])]
 
  # SLA SUMMARY
 
  api_link = '/skills/sla-summary'
  api_url = urls()["cxone"] + api_link
  params = {
    "startDate": first_date,
    "endDate": last_date
  }
  api_request = requests.get(api_url, headers=headers, params=params)
  dict_data = json.loads(api_request.text)
 
  columns = []
  data = []
  for e in dict_data.get('serviceLevelSummaries'):
    columns = e.keys()
    data.append(e.values())
 
  df_sla = pd.DataFrame(data, columns=columns)
  # df_sla = df_sla.fillna('').astype(str)
  df_sla = df_sla[["skillId", "contactsWithinSLA", "contactsOutOfSLA"]]
  df_sla['totalContacts'] = df_sla['contactsWithinSLA'] + df_sla['contactsOutOfSLA']
  df = df_activity.merge(df_sla, how="left", on=["skillId"], validate="one_to_one")
 
  # SKILLS SUMMARY
 
  api_link = '/skills/summary'
  api_url = urls()["cxone"] + api_link
  params = {
    "startDate": first_date,
    "endDate": last_date,
    "isOutbound": "false"
  }
  api_request = requests.get(api_url, headers=headers, params=params)
  dict_data = json.loads(api_request.text)
 
  columns = []
  data = []
  for e in dict_data.get('skillSummaries'):
    columns = e.keys()
    data.append(e.values())
 
  df_skills = pd.DataFrame(data, columns=columns)
  # df_skills = df_skills.fillna('').astype(str)
  df_skills = df_skills[["skillId", "abandonCount", "contactsQueued", "contactsHandled", "averageHandleTime", "averageWrapTime", "averageSpeedToAnswer"]]
 
  df_skills["averageHandleHour"] = df_skills["averageHandleTime"].apply(lambda x: (x.split("H"))[0].replace("PT", ""))
  df_skills.loc[(df_skills["averageHandleTime"].str.split("H")).str.len() == 1, "averageHandleHour"] = "0"
  df_skills["averageHandleMinute"] = df_skills["averageHandleTime"].apply(lambda x: (x.split("M"))[0][-2:].replace("H", "").replace("T", ""))
  df_skills.loc[(df_skills["averageHandleTime"].str.split("M")).str.len() == 1, "averageHandleMinute"] = "0"
  df_skills["averageHandleSecond"] = df_skills["averageHandleTime"].apply(lambda x: x[x.find("M" if x.find("M") > 0 else "H" if x.find("H") > 0 else "T") + 1:].replace("S", ""))
  df_skills.loc[~df_skills["averageHandleTime"].str.contains("S"), "averageHandleSecond"] = "0"
  df_skills[["averageHandleHour", "averageHandleMinute", "averageHandleSecond"]] = df_skills[["averageHandleHour", "averageHandleMinute", "averageHandleSecond"]].astype(float)
  df_skills["averageHandleTime"] = (df_skills["averageHandleHour"] * 60 * 60) + (df_skills["averageHandleMinute"] * 60) + df_skills["averageHandleSecond"]
  df_skills = df_skills.drop(columns=["averageHandleHour", "averageHandleMinute", "averageHandleSecond"])
 
  df_skills["averageWrapHour"] = df_skills["averageWrapTime"].apply(lambda x: (x.split("H"))[0].replace("PT", ""))
  df_skills.loc[(df_skills["averageWrapTime"].str.split("H")).str.len() == 1, "averageWrapHour"] = "0"
  df_skills["averageWrapMinute"] = df_skills["averageWrapTime"].apply(lambda x: (x.split("M"))[0][-2:].replace("H", "").replace("T", ""))
  df_skills.loc[(df_skills["averageWrapTime"].str.split("M")).str.len() == 1, "averageWrapMinute"] = "0"
  df_skills["averageWrapSecond"] = df_skills["averageWrapTime"].apply(lambda x: x[x.find("M" if x.find("M") > 0 else "H" if x.find("H") > 0 else "T") + 1:].replace("S", ""))
  df_skills.loc[~df_skills["averageWrapTime"].str.contains("S"), "averageWrapSecond"] = "0"
  df_skills[["averageWrapHour", "averageWrapMinute", "averageWrapSecond"]] = df_skills[["averageWrapHour", "averageWrapMinute", "averageWrapSecond"]].astype(float)
  df_skills["averageWrapTime"] = (df_skills["averageWrapHour"] * 60 * 60) + (df_skills["averageWrapMinute"] * 60) + df_skills["averageWrapSecond"]
  df_skills = df_skills.drop(columns=["averageWrapHour", "averageWrapMinute", "averageWrapSecond"])
 
  df_skills["averageSpeedHour"] = df_skills["averageSpeedToAnswer"].apply(lambda x: (x.split("H"))[0].replace("PT", ""))
  df_skills.loc[(df_skills["averageSpeedToAnswer"].str.split("H")).str.len() == 1, "averageSpeedHour"] = "0"
  df_skills["averageSpeedMinute"] = df_skills["averageSpeedToAnswer"].apply(lambda x: (x.split("M"))[0][-2:].replace("H", "").replace("T", ""))
  df_skills.loc[(df_skills["averageSpeedToAnswer"].str.split("M")).str.len() == 1, "averageSpeedMinute"] = "0"
  df_skills["averageSpeedSecond"] = df_skills["averageSpeedToAnswer"].apply(lambda x: x[x.find("M" if x.find("M") > 0 else "H" if x.find("H") > 0 else "T") + 1:].replace("S", ""))
  df_skills.loc[~df_skills["averageSpeedToAnswer"].str.contains("S"), "averageSpeedSecond"] = "0"
  df_skills[["averageSpeedHour", "averageSpeedMinute", "averageSpeedSecond"]] = df_skills[["averageSpeedHour", "averageSpeedMinute", "averageSpeedSecond"]].astype(float)
  df_skills["averageSpeedToAnswer"] = (df_skills["averageSpeedHour"] * 60 * 60) + (df_skills["averageSpeedMinute"] * 60) + df_skills["averageSpeedSecond"]
  df_skills = df_skills.drop(columns=["averageSpeedHour", "averageSpeedMinute", "averageSpeedSecond"])
 
  df = df.merge(df_skills, how="left", on=["skillId"], validate="one_to_one")
  df = df.rename(columns={
    "skillId": "id_skill",
    "skillName": "nome_skill",
    "campaignId": "id_campanha",
    "campaignName": "nome_campanha",
    "serverTime": "data_atualizacao",
    "skillQueueCount": "qtd_fila_skill",
    "earliestQueueTime": "tempo_fila_skill",
    "contactsActive": "qtd_contatos_ativos",
    "agentsLoggedIn": "qtd_agentes_logados",
    "agentsWorking": "qtd_agentes_trabalhando",
    "agentsUnavailable": "qtd_agentes_indisponiveis",
    "agentsAvailable": "qtd_agentes_disponiveis",
    "agentsACW": "qtd_agentes_tabulando",
    "agentsIdle": "qtd_agentes_ociosos",
    "totalContacts": "qtd_contatos_sla",
    "contactsWithinSLA": "qtd_contatos_dentro_sla",
    "contactsOutOfSLA": "qtd_contatos_fora_sla",
    "abandonCount": "qtd_contatos_abandonados",
    "contactsQueued": "qtd_contatos_oferecidos",
    "contactsHandled": "qtd_contatos_atendidos",
    "averageHandleTime": "tempo_medio_atendimento",
    "averageWrapTime": "tempo_medio_tabulando",
    "averageSpeedToAnswer": "tempo_medio_fila"
  })
  
  return df


def get_dados_receptivo(data_atual, intervalo_atual, data_comparativo):
  from services.data_integrator.db import get_db
  db = get_db()
  
  query = f"""
    SELECT
      date(contactStart, '-3 hours') AS data,
      CASE
        WHEN skillName != 'RECEPTIVO 4004' THEN skillName
        WHEN UPPER(pointOfContactName) LIKE '%COMMERCE%' THEN 'ECOMMERCE'
        WHEN UPPER(pointOfContactName) LIKE '%MEU CART%' THEN 'MEU CARTAO'
        WHEN UPPER(pointOfContactName) LIKE '%0800%' OR skillName = 'RECEPTIVO 0800' THEN 'RECEPTIVO 0800'
        WHEN UPPER(pointOfContactName) NOT LIKE '%0800%' THEN 'COBRANCA'
        ELSE '' END AS nome_skill,
      IIF(skillName IN ('RECEPTIVO LOJAS', 'RECEPTIVO AGENTE DIGITAL'), skillName, 'RECEPTIVO 4004') as nome_campanha,
      COUNT(*) AS qtd_contatos_oferecidos,
      SUM(IIF(abandoned = 'True', 1, 0)) AS qtd_contatos_abandonados,
      SUM(IIF(abandoned = 'False', 1, 0)) AS qtd_contatos_atendidos,
      SUM(IIF(notes LIKE '%target%', 1, 0)) AS qtd_contatos_target,
      SUM(IIF(notes LIKE '%sucesso%', 1, 0)) AS qtd_contatos_negocios,
      SUM(agentSeconds) AS tempo_atendimento,
      MAX(datetime(contactStart, '-3 hours')) AS data_atualizacao
    FROM 'api_nicecontact' AS c
    LEFT JOIN 'api_nicedisposition' AS d ON CAST(d.dispositionId AS INTEGER)=CAST(c.primaryDispositionId AS INTEGER)
    WHERE campaignName IN ('RECEPTIVO', 'COB - RECEPTIVO DIGITAL')
    AND pointOfContactName NOT IN ('inContactOutboundPOC')
    AND date(contactStart, '-3 hours') IN ('{data_atual}', '{data_comparativo}')
    AND CAST(SUBSTR(datetime(contactStart, '-3 hours'), 12, 2)||IIF(CAST(SUBSTR(datetime(contactStart, '-3 hours'), 15, 2) AS INTEGER) >= 30, '30', '00') AS INTEGER) <= {int(intervalo_atual[:5].replace(":", ""))}
    GROUP BY date(contactStart, '-3 hours'), CASE
      WHEN skillName != 'RECEPTIVO 4004' THEN skillName
      WHEN UPPER(pointOfContactName) LIKE '%COMMERCE%' THEN 'ECOMMERCE'
      WHEN UPPER(pointOfContactName) LIKE '%MEU CART%' THEN 'MEU CARTAO'
      WHEN UPPER(pointOfContactName) LIKE '%0800%' OR skillName = 'RECEPTIVO 0800' THEN 'RECEPTIVO 0800'
      WHEN UPPER(pointOfContactName) NOT LIKE '%0800%' THEN 'COBRANCA'
      ELSE '' END, IIF(skillName IN ('RECEPTIVO LOJAS', 'RECEPTIVO AGENTE DIGITAL'), skillName, 'RECEPTIVO 4004')
  """
  df = pd.read_sql_query(query, con=db, dtype={"data": str, "qtd_contatos_oferecidos": int, "qtd_contatos_abandonados": int, "qtd_contatos_atendidos": int, "qtd_contatos_target": int, "qtd_contatos_negocios": int})
 
  return df

def get_dispositions():
  from services.data_integrator.db import get_db
  db = get_db()

  query = f"""
    SELECT
      date(contactStart, '-3 hours') AS data,
      campaignName AS nome_campanha,
      dispositionName AS tabulacao,
      COUNT(*) AS qtd_contatos_oferecidos
    FROM 'api_nicecontact' AS c
    LEFT JOIN 'api_nicedisposition' AS d ON CAST(d.dispositionId AS INTEGER)=CAST(c.primaryDispositionId AS INTEGER)
    WHERE campaignName IN ('RECEPTIVO', 'COB - RECEPTIVO DIGITAL')
    AND pointOfContactName NOT IN ('inContactOutboundPOC')
    AND date(contactStart, '-3 hours') IN (SELECT MAX(date(contactStart, '-3 hours')) FROM 'api_nicecontact')
    GROUP BY date(contactStart, '-3 hours'), campaignName, dispositionName
  """
  df = pd.read_sql_query(query, con=db, dtype={"data": str, "qtd_contatos_oferecidos": int})
 
  return df

def get_forecast():
  file_path = Path.cwd() / 'forecast.csv'
  dtype_fore = {
    "data": str,
    "intervalo": str,
    "volume": float,
    "tmo": float,
    "abandono": float,
    "agentes_sem_indisp": float,
    "agentes_com_indisp": float,
    "ns": float,
    "trafego": float,
    "atendidas_ns": float
  }
  df = pd.read_csv(file_path, sep=";", dtype=dtype_fore, index_col=False, decimal=",")
 
  return df
 
def get_whatsapp_tabulacoes():
  file_path = Path.cwd() / 'whatsapp_tabulacoes.csv'
  dtype = {
    "tabulacao": str,
    "tipo": str
  }
  df = pd.read_csv(file_path, sep="|", dtype=dtype, index_col=False, decimal=",")
 
  return df