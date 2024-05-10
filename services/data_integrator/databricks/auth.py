from databricks import sql
from dotenv import load_dotenv
import os

def auth():
  load_dotenv()
  
  databricks = sql.connect(
    server_hostname=os.getenv('DATABRICKS_HOSTNAME'),
    http_path=os.getenv('DATABRICKS_HTTPPATH'),
    auth_type="databricks-oauth"
  )
  cursor = databricks.cursor()

  return cursor