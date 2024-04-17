import os
from dotenv import load_dotenv

def auth():
  load_dotenv()
  
  infos = {
    "url": "https://renner.http.msging.net/commands",
    "auth-human": {
      "Content-Type": "application/json",
      "Authorization": f"Key {os.getenv("TAKEBLIP_TOKEN_HUMAN")}"
    },
    "auth-router": {
      "Content-Type": "application/json",
      "Authorization": f"Key {os.getenv("TAKEBLIP_TOKEN_ROUTER")}"
    }
  }

  return infos