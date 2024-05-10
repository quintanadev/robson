import requests
import json
import os
from dotenv import load_dotenv

def auth():
  load_dotenv()

  url = 'https://a5report.a5solutions.com/a5-ws-relatorios-select-only/api/'

  auth_data = {
    "username": os.getenv('A5REPORT_USER'),
    "password": os.getenv('A5REPORT_PASS')
  }

  res = requests.post(f"{url}auth/signin", json=auth_data)
  access_token = json.loads(res.text)['token']['accessToken']

  headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + access_token
  }

  return {"headers": headers, "url": url}