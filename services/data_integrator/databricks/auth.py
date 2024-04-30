from databricks import sql

def auth():
  databricks = sql.connect(
    server_hostname="adb-6621577254898039.19.azuredatabricks.net",
    http_path="/sql/1.0/warehouses/0402b5a1921690d5",
    auth_type="databricks-oauth"
  )
  cursor = databricks.cursor()

  return cursor