from selenium import webdriver
# from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# service = Service("./automations/extensions/msedgedriver.exe")
options = webdriver.EdgeOptions()
options.add_argument('--headless')


def get_encerradas(db):
  # driver = webdriver.Edge(service=service, options=options)
  driver = webdriver.Edge(options=options)
  print(f"Abrindo site...")
  driver.get("https://portal.realizesolucoesfinanceiras.com.br/")
  assert "Login" in driver.title
  wait = WebDriverWait(driver, 10)
  print(f"Realizando login no sistema...")
  elem_user = driver.find_element(By.ID, "username")
  elem_user.clear()
  elem_user.send_keys("001144622")
  elem_pass = driver.find_element(By.ID, "password")
  elem_pass.clear()
  elem_pass.send_keys("Renner@2031")
  elem_pass.send_keys(Keys.ENTER)

  class element_validate(object):
    def __init__(self, locator, validate, type):
      self.locator = locator
      self.validate = validate
      self.type = type

    def __call__(self, driver):
      element = driver.find_element(*self.locator)
      if self.type == 'class':
        if self.validate in element.get_attribute('class'):
          return element
        else:
          return False
      elif self.type == 'not-class':
        if self.validate in element.get_attribute('class'):
          return False
        else:
          return element
      elif self.type == 'text':
        if self.validate in element.text:
          return element
        else:
          return False
      else:
        return False

  try:
    print(f"Aguardando login...")
    wait.until(EC.title_is("Página Inicial"))
    print(f"Acessando consulta analitica...")
    driver.get("https://portal.realizesolucoesfinanceiras.com.br/portal-realize/?#/tc/mesaCredito/consultaAnalitica")

    print(f"Alterando filtros...")
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/form/div/div[1]/div[1]/div[1]/div'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="select2-drop"]/ul/li[2]/div'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/form/div/div[1]/div[1]/div[3]/div'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="select2-drop"]/ul/li[2]/div'))).click()
    driver.find_element(By.XPATH, '//*[@id="main"]/div/form/div/div[2]/button').click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/ng-include[2]/table/tbody/tr[1]')))
    print(f"Alterando para visualizacao de 100 registros...")
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="s2id_autogen27"]/a'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="select2-drop"]/ul/li[4]'))).click()
    wait.until(element_validate((By.XPATH, '/html/body/div[1]'), 'body-loader active', 'not-class'))

    pagination = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/ul')
    pages = pagination.find_elements(By.TAG_NAME, 'li')
    data = []
    for page in pages:
      page_link = page.find_element(By.TAG_NAME, 'a')
      page_number = page_link.text
      page_link.click()
      
      text_validation = f"Exibindo {(int(page_number) * 100) - 100 + 1}"
      print(f"Validando pagina {page_number}...")
      wait.until(element_validate((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/span'), text_validation, 'text'))
      table = driver.find_element(By.XPATH, '//*[@id="main"]/div/ng-include[2]/table/tbody')
      rows = table.find_elements(By.TAG_NAME, 'tr')

      for row in rows:
        cols = row.find_elements(By.TAG_NAME, 'td')
        row_data = []
        for col in cols:
          cells = col.find_elements(By.TAG_NAME, 'div')
          if cells:
            for cell in cells:
              row_data.append(cell.text)
          else:
            cells = col.find_elements(By.TAG_NAME, 'span')
            if cells:
              for cell in cells:
                row_data.append(cell.text)
            else:
              row_data.append(col.text)
        data.append(row_data)
    
    columns = ['cpf', 'nome', 'tipoAnalise', 'produto', 'cartao', 'canal', 'captacao', 'numeroProposta', 'situacao', 'dataInicio', 'horaInicio', 'dataFim', 'horaFim', 'tempoFila', 'tempoAnalise', 'tempoTotal']
    df = pd.DataFrame(data, columns=columns)
    print(f"Gravando dados no banco...")
    qtd_registros = len(df)
    if qtd_registros > 0:
      table_name = 'api_portalrealizeencerradas'
      filter_date = df.head(1)['dataFim'][0]
      query = f"""
        DELETE
        FROM '{table_name}'
        WHERE dataFim = ?
      """

      db.execute(query, (filter_date, ))
      db.commit()

      print(f"Inserindo dados na tabela: {qtd_registros}")
      df.to_sql(table_name, db, if_exists='append', index=False)
      db.commit()
    else:
      print("Sem novos registros para gravar!")
  finally:
    driver.quit()
