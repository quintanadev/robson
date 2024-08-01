from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import requests
import json
import time

from services.data_integrator.nicecxone.auth import urls
from services.data_integrator.nicecxone.auth import auth, urls

def get_skill_agents_logged(skill, updated_since):
  headers = auth()
  api_link = f'skills/{skill}/agents'
  query = '?updatedSince={}&fields={}'
  api = api_link + query.format(updated_since, 'agentId,firstName,lastName,isActive,isAssigned,isSkillActive,isDialer,isOutbound,skillId,skillName')
  print(f"Executando api: {api_link}")
  api_url = urls()['cxone-v30'] + api
  columns = []
  data = []
  api_request = requests.get(api_url, headers=headers)
  if api_request.status_code == 200:
    dict_data = json.loads(api_request.text)
    for agent_skill in dict_data.get('agentSkillAssignments'):
      columns = agent_skill.keys()
      data.append(agent_skill.values())
    df_agents = pd.DataFrame(data, columns=columns)
    df_agents = df_agents.loc[(df_agents['isActive'] == True) & (df_agents['isDialer'] == False)]
    # df_agents = df_agents.loc[df_agents['agentId'].isin([34817809, 34621269])]
    return df_agents

def get_skill_agents_unassigned(skill, updated_since):
  headers = auth()
  api_link = f'skills/{skill}/agents/unassigned'
  query = '?updatedSince={}$fields={}'
  api = api_link + query.format(updated_since, 'agentId,firstName,isActive,teamName')
  print(f"Executando api: {api_link}")
  api_url = urls()['cxone-v30'] + api
  columns = []
  data = []
  api_request = requests.get(api_url, headers=headers)
  if api_request.status_code == 200:
    dict_data = json.loads(api_request.text)
    for agent_skill in dict_data.get('agents'):
      columns = agent_skill.keys()
      data.append(agent_skill.values())
    df_agents = pd.DataFrame(data, columns=columns)
    df_agents = df_agents.loc[(df_agents['isActive'] == False)]
    # df_agents = df_agents.loc[df_agents['agentId'].isin([34817809, 34621269])]
    return df_agents

def get_agents_status(updated_since):
  headers = auth()
  api_link = 'agents/states'
  query = '?top={}&fields={}&updatedSince={}'
  api = api_link + query.format('10000', 'agentId,firstName,lastName,teamName,agentStateId,agentStateName,isActive,isACW,isOutbound,contactId,outStateDescription,lastUpdateTime,skillName', updated_since)
  print(f"Executando api: {api_link}")
  api_url = urls()['cxone-v30'] + api
  columns = []
  data = []
  api_request = requests.get(api_url, headers=headers)
  if api_request.status_code == 200:
    dict_data = json.loads(api_request.text)
    for agent_skill in dict_data.get('agentStates'):
      columns = agent_skill.keys()
      data.append(agent_skill.values())
    df_agents = pd.DataFrame(data, columns=columns)
    # df_agents = df_agents.loc[df_agents['agentId'].isin([34817809, 34621269])]
    return df_agents

def run_clear_queue(skill):
  try:
    updated_since = (datetime.now() + relativedelta(minutes=-1)).strftime('%Y-%m-%dT%H:%M:%S.000Z')
    
    skill_logged = 20890028
    # skill_logged = 18593849
    # skill = 16412178 if skill == 16412186 else 20889707 if skill == 16412187 else 18640596
    
    df_agents_logged = get_skill_agents_logged(skill_logged, updated_since)
    df_agents_unassigned = get_skill_agents_unassigned(skill, updated_since)
    df_agents_status = get_agents_status(updated_since)
    df_agents_status = df_agents_status.loc[(df_agents_status['isActive'] == True) & (df_agents_status['agentStateId'] == 1) & (df_agents_status['isACW'] == False) & (df_agents_status['isOutbound'] == False) & (df_agents_status['contactId'].isnull())]

    df = df_agents_logged.merge(df_agents_unassigned, how='inner', on=['agentId'], validate='one_to_one')
    df = df.merge(df_agents_status, how='inner', on=['agentId'], validate='one_to_one')
    agent_list = df.head(3)['agentId'].astype(str).values.tolist()

    if len(agent_list) > 0:
      body = {
        'agentAndSkillDetails': [{
          'agentIds': agent_list,
          'skills': [{
            'skillIds': [str(skill)],
            'isActive': True
          }]
        }]
      }

      api_link = 'agents/skills'
      api_url = urls()['cxone-v30'] + api_link
      requests.post(api_url, json=body, headers=headers)
      print(f"Skill {skill} adicionado nos usuarios: {agent_list}")
      
      time.sleep(40.0)

      for agent_id in agent_list:
        body = {
          'skills': [{'skillId': str(skill)}]
        }
        api_link = f"agents/{agent_id}/skills"
        api_url = urls()['cxone-v30'] + api_link
        requests.delete(api_url, json=body, headers=headers)
        return {"result": "success", "message": f"Skill {str(skill)} adicionado aos agentes {str(agent_list).replace('[', '').replace(']', '')}"}
    else:
      return {"result": "info", "message": "Nenhum agente disponível!"}
  except Exception as e:
    return {"result": "danger", "message": "Erro ao localizar agentes disponíveis!"}