import requests
import json

def auth():
  auth = {
    "url": "https://cxone.niceincontact.com/auth/token",
    "username": "8127a9ec-5d09-44f9-849a-9cca0bcb4ad8",
    "password": "kRIcCunt9NrAcHDRzlZigA=="
  }

  auth_data = {
    "grant_type": "password",
    "username": "ASRKDRVHWRSIDGNDUTTYZSSRHAU7YXV655ZNO3PG2F3PFGNCKENA====",
    "password": "MAP4EET7QAYST7CLP3QKAB2MFQCPMG43LO4FJ75HCRKXJWAPUVZA===="
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
