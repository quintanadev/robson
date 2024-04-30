from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

from .auth import auth

def mailing(db):
  table_name = 'api_databricksfatomailing'
  query = f"""
    SELECT MAX(dataMailing) AS dataMailing
    FROM '{table_name}'
  """
  date_updated = db.execute(query).fetchone()['dataMailing']
  print(f'Data do mailing no banco: {date_updated}')
  if date_updated and date_updated == date.today().strftime('%Y-%m-%d'):
    pass
  else:
    date_updated = date_updated if date_updated else date(2024, 2, 1).strftime('%Y-%m-%d')
    query_databricks = f"""
      select
        left(m.DatGeracaoArquivo, 6) as periodo,
        to_date(m.DatGeracaoArquivo, 'yyyyMMdd') as dataMailing,
        m.Familia as familia,
        m.Segmento as segmento,
        m.FaixaAtraso as faixaAtraso,
        case m.MomentoAtraso
          when 0 then 'ND'
          when 1 then 'FPD'
          when 2 then 'FTD'
          when 3 then 'RECORRENTE'
          else 'ND' end as momentoAtraso,
        case m.Propensao
          when 0 then '0. ND'
          when 1 then '1. MINIMA'
          when 2 then '2. BAIXA'
          when 3 then '3. MEDIA'
          when 4 then '4. ALTA'
          when 5 then '5. MAXIMA'
          else 'ND' end as propensao,
        count(distinct m.DesRegis) as qtdClientes,
        sum(m.ValorAtraso) as valorAtraso,
        sum(m.ValorSaldo) as valorSaldo,
        sum(d.QtdTentativas) as qtdTentativas,
        sum(d.QtdAlo) as qtdAlo,
        sum(d.QtdLocalizado) as qtdLocalizado,
        sum(d.QtdCpc) as qtdCpc,
        sum(d.QtdCpcTarget) as qtdTarget,
        sum(d.QtdSucesso) as qtdSucesso,
        sum(e.QtdTentativasUnique) as qtdTentativasUnique,
        sum(e.QtdAloUnique) as qtdAloUnique,
        sum(e.QtdLocalizadoUnique) as qtdLocalizadoUnique,
        sum(e.QtdCpcUnique) as qtdCpcUnique,
        sum(e.QtdCpcTargetUnique) as qtdTargetUnique,
        sum(e.QtdSucessoUnique) as qtdSucessoUnique,
        sum(e.QtdPagamentoUnique) as qtdPagamentoUnique,
        sum(e.QtdDiasMailing) as qtdDiasMailing
      from bronze_corporativo_recupera.mailinglayoutolos as m
      left join db_group_csc_qualidade_credito_cobranca.niceativodiario as d on d.Data=to_date(m.DatGeracaoArquivo, 'yyyyMMdd') and d.Cpf=m.DesRegis
      left join db_group_csc_qualidade_credito_cobranca.niceativomensal as e on e.Data=to_date(m.DatGeracaoArquivo, 'yyyyMMdd') and e.Cpf=m.DesRegis
      where to_date(m.DatGeracaoArquivo, 'yyyyMMdd') > '{date_updated}'
      and m.NomeMailingNice not like '%DIGITAL%'
      group by all
    """
    databricks = auth()
    databricks.execute(query_databricks)
    data_result = databricks.fetchall()
    df_databricks = pd.DataFrame(data_result, columns=data_result[0].asDict().keys(), dtype=str)
    df_databricks.to_sql(table_name, db, if_exists='append', index=False)
    db.commit()
    databricks.close()
    print('Mailing gravado no banco!')

  return True

def negocios(db):
  table_name = 'api_databricksanaliticonegocio'
  query = f"""
    SELECT MAX(dataNegocio) AS dataNegocio
    FROM '{table_name}'
  """
  date_updated = db.execute(query).fetchone()['dataNegocio']
  print(f'Data de producao no banco: {date_updated}')
  if date_updated and date_updated == (date.today() + relativedelta(days=-1)).strftime('%Y-%m-%d'):
    pass
  else:
    periodo = (datetime.strptime(date_updated, '%Y-%m-%d') if date_updated else date(2024, 2, 1)).strftime('%Y%m')
    query_databricks = f"""
      select
        Periodo as periodo,
        PeriodoNegocio as periodoNegocio,
        PeriodoVencimento as periodoVencimento,
        PeriodoPagamento as periodoPagamento,
        TipoNegocio as tipoNegocio,
        DataNegocio as dataNegocio,
        DataVencimento as dataVencimento,
        DataPagamento as dataPagamento,
        Cpf as cpf,
        Usuario as usuario,
        Atraso as diasAtraso,
        GrupoProduto as segmento,
        Familia as familia,
        FaixaAtraso as faixaAtraso,
        Atendimento as canal,
        QtdNegocios as qtdNegocios,
        QtdPagamentos as qtdPagamentos,
        QtdQuebra as qtdQuebras,
        Parcelamento as parcelamento,
        FaixaParcelamento as faixaParcelamento,
        DiasVencimento as diasVencimento,
        Nome as nomeColaborador,
        NomeLider as nomeLider,
        replace(TipoCargo, 'Ç', 'C') as tipoCargo,
        ValorDivida as valorDivida,
        ValorNegociado as valorNegociado,
        ValorPagamento as valorPagamento,
        coalesce(ValorSaldoCadoc, if(ValorPagamento = 0, null, ValorPagamento), ValorNegociado) as valorSaldoCadoc,
        coalesce(FaixaAtrasoCadoc, FaixaAtraso) as faixaAtrasoCadoc
      from db_group_csc_qualidade_credito_cobranca.basenegociossaldo
      where Periodo >= {periodo}
    """
    databricks = auth()
    databricks.execute(query_databricks)
    data_result = databricks.fetchall()
    df_databricks = pd.DataFrame(data_result, columns=data_result[0].asDict().keys(), dtype=str)
    df_databricks.to_sql(table_name, db, if_exists='append', index=False)
    db.commit()
    databricks.close()
    print('Negocios gravado no banco!')

  return True
