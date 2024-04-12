import requests
import json
import os
from dotenv import load_dotenv

def auth():
  load_dotenv()

  auth = {
    "url": "https://cxone.niceincontact.com/auth/token",
    "username": os.getenv("NICECXONE_GLOBAL_USER"),
    "password": os.getenv("NICECXONE_GLOBAL_PASS")
  }

  auth_data = {
    "grant_type": "password",
    "username": os.getenv("NICECXONE_USER"),
    "password": os.getenv("NICECXONE_PASS")
  }

  headers = {
    "Content-Type": "application/x-www-form-urlencoded"
  }

  res = requests.post(auth["url"], data=auth_data, headers=headers, auth=(auth["username"], auth["password"]))
  access_token = json.loads(res.text)['access_token']

  headers = {
    "Content-Type": "application/json",
    'Authorization': "Bearer " + access_token
  }

  return headers

def urls():
  urls = {
    "cxone": 'https://api-c57.nice-incontact.com/incontactapi/services/v25.0/',
    "users": 'https://na1.nice-incontact.com/user-management/v1/',
  }

  return urls
