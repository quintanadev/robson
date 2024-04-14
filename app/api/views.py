import pandas as pd
from django.http import JsonResponse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from services.data_integrator.nicecxone.realtime import get_sla_skill_summary, get_forecast, get_dados_receptivo

def inbound_cards(request):
  df = get_sla_skill_summary()
  df = df.assign(tempo_atendimento=lambda x: x["tempo_medio_atendimento"] * x["qtd_contatos_atendidos"])
  df = df.assign(tempo_tabulando=lambda x: x["tempo_medio_tabulando"] * x["qtd_contatos_atendidos"])
  df = df.assign(tempo_em_fila=lambda x: x["tempo_medio_fila"] * x["qtd_contatos_oferecidos"])
  df = df.assign(per_abandono=lambda x: round(x["qtd_contatos_abandonados"] / x["qtd_contatos_oferecidos"] * 100, 2))
  df_ns = df.loc[df["id_skill"].isin([16412186, 16412187])]
  
  df_fore = get_forecast()
  df_fore = df_fore.assign(intervalo_int=lambda x: x["intervalo"].str[:5].str.replace(":", "").astype(int))

  data_atualizacao = df["data_atualizacao"].max()
  data_atual = data_atualizacao.strftime("%Y-%m-%d")
  intervalo_atual = ("0" if data_atualizacao.hour < 10 else "") + str(data_atualizacao.hour) + ":" + ("30" if data_atualizacao.minute >= 30 else "00") + ":00"
  data_comparativo = data_atualizacao + relativedelta(days=-7)
  while data_comparativo.weekday() == 6 or data_comparativo.date() in [
      datetime(2023, 10, 12).date(),
      datetime(2023, 11, 15).date(),
      datetime(2023, 11, 15).date(),
      datetime(2023, 12, 25).date(),
    ]:
    data_comparativo = data_comparativo + relativedelta(days=-1)
  data_comparativo = datetime.strftime(data_comparativo, "%Y-%m-%d")
  
  df_fore_data = df_fore.loc[df_fore["data"] == data_atualizacao.strftime("%d/%m/%Y")]
  df_fore_data_antes = df_fore_data.loc[df_fore_data["intervalo_int"] <= int(intervalo_atual[:5].replace(":", ""))]
  df_fore_data_apos = df_fore_data.loc[df_fore_data["intervalo_int"] > int(intervalo_atual[:5].replace(":", ""))]
  df_fore_intervalo = df_fore_data.loc[df_fore_data["intervalo"] == intervalo_atual]

  forecast_volume_projetado = df_fore_data_apos["volume"].sum()
  forecast_volume_sla_projetado = df_fore_data_apos["atendidas_ns"].sum()
  
  contatos_dentro_sla = df_ns["qtd_contatos_dentro_sla"].sum()
  contatos_sla = df_ns["qtd_contatos_sla"].sum()
  
  nivel_servico = 0 if contatos_sla == 0 else round(contatos_dentro_sla / contatos_sla * 100, 2)
  nivel_servico_projetado = 0 if contatos_sla == 0 else round((contatos_dentro_sla + forecast_volume_sla_projetado) / (contatos_sla + forecast_volume_projetado) * 100, 2)
  fila = df["qtd_fila_skill"].sum()
  tempo_fila_segundos = (data_atualizacao - (df["tempo_fila_skill"].min() if fila > 0 else data_atualizacao)).total_seconds()
  tempo_fila = "00:00:00" if tempo_fila_segundos <= 0 else str(timedelta(seconds=tempo_fila_segundos)).split(".")[0].zfill(8)
  agentes_logados = df["qtd_agentes_logados"].max()
  agentes_disponiveis = df["qtd_agentes_disponiveis"].max()
  agentes_pausas = df["qtd_agentes_pausa"].max() + df["qtd_agentes_indisponiveis"].max()
  contatos_em_atendimento = df["qtd_contatos_ativos"].sum()
  contatos_recebidos = df["qtd_contatos_oferecidos"].sum()
  contatos_abandonados = df["qtd_contatos_abandonados"].sum()
  contatos_atendidos = df["qtd_contatos_atendidos"].sum()
  tempo_em_fila = df["tempo_em_fila"].sum()
  tempo_atendimento = df["tempo_atendimento"].sum()
  tempo_tabulando = df["tempo_tabulando"].sum()

  tma_segundos = 0 if contatos_atendidos == 0 else tempo_atendimento / contatos_atendidos
  tma = "00:00:00" if tempo_atendimento <= 0 else str(timedelta(seconds=tma_segundos)).split(".")[0].zfill(8)
  tmt_segundos = 0 if contatos_atendidos == 0 else tempo_tabulando / contatos_atendidos
  tmt = "00:00:00" if tempo_tabulando <= 0 else str(timedelta(seconds=tmt_segundos)).split(".")[0].zfill(8)
  tme_segundos = 0 if contatos_recebidos == 0 else tempo_em_fila / contatos_recebidos
  tme = "00:00:00" if tempo_em_fila <= 0 else str(timedelta(seconds=tme_segundos)).split(".")[0].zfill(8)

  forecast_volume = df_fore_data_antes["volume"].sum()
  forecast_atendidas = df_fore_data_antes["volume"].sum() - df_fore_data_antes["abandono"].sum()
  forecast_percentual_atendimento = 0 if forecast_volume == 0 else round(forecast_atendidas / forecast_volume * 100, 2)

  percentual_volume_fore = 0 if forecast_volume == 0 else round((contatos_recebidos / forecast_volume - 1) * 100, 2)
  percentual_abandono = 0 if contatos_recebidos == 0 else round(contatos_abandonados / contatos_recebidos * 100, 2)
  percentual_atendimento = 0 if contatos_recebidos == 0 else round(contatos_atendidos / contatos_recebidos * 100, 2)

  forecast_em_atendimento = df_fore_intervalo["volume"].max() / (1800 / df_fore_intervalo["tmo"].max()) if df_fore_intervalo["volume"].max() > 0 else 0
  forecast_agentes = round(df_fore_intervalo["agentes_com_indisp"].max(), 0)
  
  df_db = get_dados_receptivo(data_atual, intervalo_atual, data_comparativo)
  
  negocios = df_db.loc[df_db["data"] == data_atual]["negocios"].sum()
  print(negocios)
  target = df_db.loc[df_db["data"] == data_atual]["target"].sum() + negocios
  percentual_conversao = 0 if target == 0 else round((negocios / target) * 100, 2)
  
  negocios_comparativo = df_db.loc[df_db["data"] == data_comparativo]["negocios"].sum()
  atendidas_comparativo = df_db.loc[df_db["data"] == data_comparativo]["atendidas"].sum()
  percentual_negocios_comparativo = 0 if negocios_comparativo == 0 or negocios == 0 else round(((negocios / contatos_atendidos) / (negocios_comparativo / atendidas_comparativo) - 1) * 100, 2)

  volume_comparativo = df_db.loc[df_db["data"] == data_comparativo]["volume"].sum()
  abandonadas_comparativo = df_db.loc[df_db["data"] == data_comparativo]["abandonadas"].sum()
  percentual_abandono_comparativo = 0 if abandonadas_comparativo == 0 else round((contatos_abandonados / abandonadas_comparativo - 1) * 100, 2)
  percentual_volume_comparativo = 0 if volume_comparativo == 0 else round((contatos_recebidos / volume_comparativo - 1) * 100, 2)
  percentual_tma_comparativo = 0 if atendidas_comparativo == 0 else round((tma_segundos / (df_db.loc[df_db["data"] == data_comparativo]["tempo_atendimento"].sum() / atendidas_comparativo) - 1) * 100, 2)

  # df_clientes = get_clientes_receptivo(data_atual)

  data_response = {
    "data": {
      "data_atualizacao": str(datetime.strftime(data_atualizacao, "%d/%m/%Y %H:%M:%S")),
      "fila": str(fila),
      "tempo_fila_segundos": str(int(tempo_fila_segundos)),
      "tempo_fila": str(tempo_fila),
      "nivel_servico": str(nivel_servico),
      "agentes_logados": str(agentes_logados),
      "agentes_disponiveis": str(agentes_disponiveis),
      "agentes_pausas": str(agentes_pausas),
      "contatos_em_atendimento": str(contatos_em_atendimento),
      "contatos_recebidos": str(contatos_recebidos),
      "contatos_abandonados": str(contatos_abandonados),
      "percentual_abandono": str(percentual_abandono),
      "percentual_atendimento": str(percentual_atendimento),
      "forecast_em_atendimento": str(forecast_em_atendimento),
      "forecast_agentes": str(forecast_agentes),
      "forecast_percentual_volume": str(percentual_volume_fore),
      "forecast_percentual_atendimento": str(forecast_percentual_atendimento),
      "nivel_servico_projetado": str(nivel_servico_projetado),
      "tma": str(tma),
      "tma_segundos": str(tma_segundos),
      "tmt": str(tmt),
      "tmt_segundos": str(tmt_segundos),
      "tme": str(tme),
      "tme_segundos": str(tme_segundos),
      "negocios": str(negocios),
      "percentual_conversao": str(percentual_conversao),
      "percentual_negocios_comparativo": str(percentual_negocios_comparativo),
      "percentual_abandono_comparativo": str(percentual_abandono_comparativo),
      "percentual_volume_comparativo": str(percentual_volume_comparativo),
      "percentual_tma_comparativo": str(percentual_tma_comparativo),
      "skills": df.to_json(orient="records")
    },
    "updated": datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
  }
  return JsonResponse(data_response)