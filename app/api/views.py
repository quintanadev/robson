from django.http import JsonResponse, HttpResponseNotFound
from django.core import serializers
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import json

from services.data_integrator.nicecxone.realtime import get_sla_skill_summary, get_forecast, get_dados_receptivo, get_dispositions
from services.data_integrator.takeblip.realtime import get_tickets_times, get_tickets_agents, get_tickets_tags, get_contacts_bot, get_nps, get_agents_status, get_tickets_status

from .models import PortalRealizeEncerradas

def realtime_inbound_cards(request):
  if request.method == 'GET':
    try:
      df = get_sla_skill_summary()
    except:
      return JsonResponse({'result': 'error', 'message': 'Erro ao consultar a API!'})
    
    df = df.assign(tempo_atendimento=lambda x: x["tempo_medio_atendimento"] * x["qtd_contatos_atendidos"])
    df = df.assign(tempo_tabulando=lambda x: x["tempo_medio_tabulando"] * x["qtd_contatos_atendidos"])
    df = df.assign(tempo_em_fila=lambda x: x["tempo_medio_fila"] * x["qtd_contatos_oferecidos"])
    df = df.assign(per_abandono=lambda x: round(x["qtd_contatos_abandonados"] / x["qtd_contatos_oferecidos"] * 100, 2))
    df_ns = df.loc[df["id_skill"].isin([16412186, 16412187])]
    
    try:
      df_fore = get_forecast()
    except:
      return JsonResponse({'result': 'error', 'message': 'Erro ao consultar o forecast!'})
    
    df_fore = df_fore.assign(intervalo_int=lambda x: x["intervalo"].str[:5].str.replace(":", "").astype(int))

    data_atualizacao = df["data_atualizacao"].max()
    data_atual = data_atualizacao.strftime("%Y-%m-%d")
    intervalo_atual = ("0" if data_atualizacao.hour < 10 else "") + str(data_atualizacao.hour) + ":" + ("30" if data_atualizacao.minute >= 30 else "00") + ":00"
    data_comparativo = data_atualizacao + relativedelta(days=-6)
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
    agentes_pausas = (df["qtd_agentes_indisponiveis"] - df["qtd_agentes_tabulando"]).max()
    agentes_trabalhando = df["qtd_agentes_trabalhando"].sum()
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
    
    try:
      df_db = get_dados_receptivo(data_atual, intervalo_atual, data_comparativo)
    except:
      return JsonResponse({'result': 'error', 'message': 'Erro ao consultar o banco de dados!'})
    
    negocios = df_db.loc[df_db["data"] == data_atual]["qtd_contatos_negocios"].sum()
    target = df_db.loc[df_db["data"] == data_atual]["qtd_contatos_target"].sum() + negocios
    percentual_conversao = 0 if target == 0 else round((negocios / target) * 100, 2)
    
    negocios_comparativo = df_db.loc[df_db["data"] == data_comparativo]["qtd_contatos_oferecidos"].sum()
    atendidas_comparativo = df_db.loc[df_db["data"] == data_comparativo]["qtd_contatos_atendidos"].sum()
    contatos_atendidos_comparativo = df_db.loc[df_db["data"] == data_atual]["qtd_contatos_atendidos"].sum()
    percentual_negocios_comparativo = 0 if negocios_comparativo == 0 or negocios == 0 else round(((negocios / contatos_atendidos_comparativo) / (negocios_comparativo / atendidas_comparativo) - 1) * 100, 2)

    volume_comparativo = df_db.loc[df_db["data"] == data_comparativo]["qtd_contatos_oferecidos"].sum()
    abandonadas_comparativo = df_db.loc[df_db["data"] == data_comparativo]["qtd_contatos_abandonados"].sum()
    percentual_abandono_comparativo = 0 if abandonadas_comparativo == 0 else round((contatos_abandonados / abandonadas_comparativo - 1) * 100, 2)
    percentual_volume_comparativo = 0 if volume_comparativo == 0 else round((contatos_recebidos / volume_comparativo - 1) * 100, 2)
    percentual_tma_comparativo = 0 if atendidas_comparativo == 0 else round((tma_segundos / (df_db.loc[df_db["data"] == data_comparativo]["tempo_atendimento"].sum() / atendidas_comparativo) - 1) * 100, 2)

    df_s = df[["nome_skill", "id_skill", "qtd_fila_skill", "qtd_contatos_ativos", "qtd_contatos_oferecidos", "qtd_contatos_abandonados", "qtd_agentes_disponiveis"]]
    df_c = df_db.loc[df_db["data"] == data_atual][["nome_skill", "nome_campanha", "qtd_contatos_negocios", "qtd_contatos_oferecidos", "qtd_contatos_abandonados", "qtd_contatos_target", "data_atualizacao"]]
    df_m = df_s.merge(df_c, how="outer", on="nome_skill")
    df_m["ordem_skill"] = 100
    df_m.loc[df_m["nome_skill"] == "RECEPTIVO 4004", "ordem_skill"] = 1
    df_m.loc[df_m["nome_skill"] == "COBRANCA", "ordem_skill"] = 2
    df_m.loc[df_m["nome_skill"] == "RECEPTIVO 0800", "ordem_skill"] = 3
    df_m.loc[df_m["nome_skill"] == "MEU CARTAO", "ordem_skill"] = 4
    df_m.loc[df_m["nome_skill"] == "ECOMMERCE", "ordem_skill"] = 5
    df_m.loc[df_m["nome_skill"] == "RECEPTIVO LOJAS", "ordem_skill"] = 6
    df_m.loc[df_m["nome_skill"] == "RECEPTIVO AGENTE DIGITAL", "ordem_skill"] = 7

    df_m["qtd_contatos_oferecidos"] = df_m[["qtd_contatos_oferecidos_x", "qtd_contatos_oferecidos_y"]].max(axis=1)
    df_m["qtd_contatos_abandonados"] = df_m[["qtd_contatos_abandonados_x", "qtd_contatos_abandonados_y"]].max(axis=1)
    df_m.loc[df_m["nome_skill"] == "RECEPTIVO 4004", "qtd_contatos_oferecidos"] = df_m.loc[df_m["nome_campanha"] == "RECEPTIVO 4004"]["qtd_contatos_oferecidos"].sum()
    df_m.loc[df_m["nome_skill"] == "RECEPTIVO 4004", "qtd_contatos_abandonados"] = df_m.loc[df_m["nome_campanha"] == "RECEPTIVO 4004"]["qtd_contatos_abandonados"].sum()
    df_m["qtd_contatos_target"] = df_m["qtd_contatos_target"] + df_m["qtd_contatos_negocios"]
    df_m.loc[df_m["nome_skill"] == "RECEPTIVO 4004", "qtd_contatos_negocios"] = df_m.loc[df_m["nome_campanha"] == "RECEPTIVO 4004"]["qtd_contatos_negocios"].sum()
    df_m.loc[df_m["nome_skill"] == "RECEPTIVO 4004", "qtd_contatos_target"] = df_m.loc[df_m["nome_campanha"] == "RECEPTIVO 4004"]["qtd_contatos_target"].sum()
    df_m["per_abandono"] = round(df_m["qtd_contatos_abandonados"] / df_m["qtd_contatos_oferecidos"] * 100, 2)
    df_m["per_conversao"] = round(df_m["qtd_contatos_negocios"] / df_m["qtd_contatos_target"] * 100, 2)
    df_m.loc[df_m["nome_skill"] == "RECEPTIVO 4004", "data_atualizacao"] = df_m.loc[df_m["nome_campanha"] == "RECEPTIVO 4004"]["data_atualizacao"].max()
    df_m["hora_ultima_chamada"] = pd.to_datetime(df_m["data_atualizacao"]).dt.strftime("%H:%M:%S").fillna("")
    df_m = df_m.fillna(0)
    df_m = df_m.sort_values("ordem_skill")

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
        "agentes_trabalhando": str(agentes_trabalhando),
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
        "json_skills": df_m.to_json(orient="records"),
      },
      "updated": datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
    }
    return JsonResponse(data_response)
  else:
    return HttpResponseNotFound('Not Found')

def realtime_dispositions(request):
  if request.method == 'GET':
    df = get_dispositions()
    df_rec = df.loc[df['nome_campanha'] == 'RECEPTIVO'].sort_values('qtd_contatos_oferecidos', ascending=False)
    df_rec['per_tabulacao'] = (df_rec['qtd_contatos_oferecidos'] / df_rec['qtd_contatos_oferecidos'].sum() * 100).round(2)
    df_rec = df_rec.loc[~df_rec['tabulacao'].isnull()].head(10)
    df_dig = df.loc[df['nome_campanha'] == 'COB - RECEPTIVO DIGITAL'].sort_values('qtd_contatos_oferecidos', ascending=False)
    df_dig['per_tabulacao'] = (df_dig['qtd_contatos_oferecidos'] / df_dig['qtd_contatos_oferecidos'].sum() * 100).round(2)
    df_dig = df_dig.loc[~df_dig['tabulacao'].isnull()].head(10)
    data_response = {
      "data": {
        "json_receptivo": df_rec.to_json(orient="records"),
        "json_digital": df_dig.to_json(orient="records"),
      },
      "updated": datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
    }
    return JsonResponse(data_response)
  else:
    return HttpResponseNotFound('Not Found')
  
def realtime_whatsapp(request):
  if request.method == 'GET':
    status_times = get_tickets_times()
    tickets_agents = get_tickets_agents()
    tickets_tags = get_tickets_tags()
    status_bot = get_contacts_bot()
    nps = get_nps()
    status_agents = get_agents_status()
    status_tickets = get_tickets_status()
    
    info_wpp = status_agents | status_tickets | status_times | tickets_agents | tickets_tags | status_bot | nps
    info_wpp["updated"] = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    info_wpp["percentualConversao"] = 0 if info_wpp["ticketsNegocio"] == "0" else round((int(info_wpp["ticketsNegocio"]) / (int(info_wpp["ticketsNegocio"]) + int(info_wpp["ticketsTarget"]))) * 100, 2)
    info_wpp["ticketsPerAttendant"] = round(float(info_wpp["ticketsPerAttendant"]), 2)

    info_wpp["nota_00"] = info_wpp["nota_00"] if "nota_00" in info_wpp.keys() else 0
    info_wpp["nota_01"] = info_wpp["nota_01"] if "nota_01" in info_wpp.keys() else 0
    info_wpp["nota_02"] = info_wpp["nota_02"] if "nota_02" in info_wpp.keys() else 0
    info_wpp["nota_03"] = info_wpp["nota_03"] if "nota_03" in info_wpp.keys() else 0
    info_wpp["nota_04"] = info_wpp["nota_04"] if "nota_04" in info_wpp.keys() else 0
    info_wpp["nota_05"] = info_wpp["nota_05"] if "nota_05" in info_wpp.keys() else 0
    info_wpp["nota_06"] = info_wpp["nota_06"] if "nota_06" in info_wpp.keys() else 0
    info_wpp["nota_07"] = info_wpp["nota_07"] if "nota_07" in info_wpp.keys() else 0
    info_wpp["nota_08"] = info_wpp["nota_08"] if "nota_08" in info_wpp.keys() else 0
    info_wpp["nota_09"] = info_wpp["nota_09"] if "nota_09" in info_wpp.keys() else 0
    info_wpp["nota_10"] = info_wpp["nota_10"] if "nota_10" in info_wpp.keys() else 0
    info_wpp["nota_total"] = info_wpp["nota_total"] if "nota_total" in info_wpp.keys() else 0
    
    info_wpp["npsPromotor"] = round((info_wpp["nota_10"] + info_wpp["nota_09"]) / info_wpp["nota_total"] * 100, 2) if info_wpp["nota_total"] > 0 else 0
    info_wpp["npsNeutro"] = round((info_wpp["nota_08"] + info_wpp["nota_07"]) / info_wpp["nota_total"] * 100, 2) if info_wpp["nota_total"] > 0 else 0
    info_wpp["npsDetrator"] = round((info_wpp["nota_00"] + info_wpp["nota_01"] + info_wpp["nota_02"] + info_wpp["nota_03"] + info_wpp["nota_04"] + info_wpp["nota_05"] + info_wpp["nota_06"]) / info_wpp["nota_total"] * 100, 2) if info_wpp["nota_total"] > 0 else 0
    info_wpp["npsTotal"] = round(info_wpp["npsPromotor"] - info_wpp["npsDetrator"], 2)
  
    data_response = {
      "data": info_wpp,
      "updated": datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
    }
    return JsonResponse(data_response)
  else:
    return HttpResponseNotFound('Not Found')
  
def dashboard_credito(request):
  if request.method == 'GET':
    data = datetime.strftime(datetime.now() + relativedelta(days=-1), "%d/%m/%Y")
    encerradas = PortalRealizeEncerradas.objects.filter(dataFim=data)
    encerradas_serialized = serializers.serialize('json', encerradas)
    encerradas_json = []
    for x in json.loads(encerradas_serialized):
      encerradas_json.append(x["fields"])

    df = pd.json_normalize(encerradas_json)
    df['hora'] = df['horaFim'].str[:2]
    df['data'] = pd.to_datetime(df['dataFim'], format='%d/%m/%Y')
    df['tempoFila'] = pd.to_datetime(df['tempoFila'], format='%H:%M:%S')
    df['tempoAnalise'] = pd.to_datetime(df['tempoAnalise'], format='%H:%M:%S')
    df['tempoTotal'] = pd.to_datetime(df['tempoTotal'], format='%H:%M:%S')
    df['tempoSla'] = pd.to_datetime('00:04:00', format='%H:%M:%S')
    df['qtdProposta'] = 1
    # df['qtdDentroSla'] = [print(x) for x in df['tempoTotal']]
    df = df.assign(qtdDentroSla=df.apply(lambda x: 1 if x['tempoTotal'] <= x['tempoSla'] else 0, axis=1))
    df = df.assign(qtdConcessao=df.apply(lambda x: 1 if x['tempoTotal'] <= x['tempoSla'] else 0, axis=1))
    df = df.assign(qtdEmprestimo=df.apply(lambda x: 1 if x['tipoAnalise'] == 'Concessão' and x['produto'] == 'Empréstimo' else 0, axis=1))
    df = df.assign(qtdLimite=df.apply(lambda x: 1 if x['tipoAnalise'] == 'Manutenção_Limites' else 0, axis=1))
    df = df.assign(qtdAnalise=df.apply(lambda x: 1 if x['tipoAnalise'] == 'Solicitação Análise' else 0, axis=1))
    df = df.assign(qtdDesbloqueio=df.apply(lambda x: 1 if x['tipoAnalise'][:4] == 'DESB' else 0, axis=1))
    df = df.assign(qtdAprovado=df.apply(lambda x: 1 if x['situacao'] == 'APROVADO' else 0, axis=1))
    df = df.assign(qtdNegado=df.apply(lambda x: 1 if x['situacao'] == 'NEGADO' else 0, axis=1))
    df = df.assign(qtdRetornadoLoja=df.apply(lambda x: 1 if x['situacao'] == 'RETORNADO_LOJA' else 0, axis=1))

    clientes = df['cpf'].nunique()
    propostas = df['qtdProposta'].sum()
    hc = df['nome'].nunique()
    nivel_servico = round(df['qtdDentroSla'].sum() / propostas * 100, 1)
    concessao = df['qtdConcessao'].sum()
    emprestimo = df['qtdEmprestimo'].sum()
    limite = df['qtdLimite'].sum()
    analise = df['qtdAnalise'].sum()
    desbloqueio = df['qtdDesbloqueio'].sum()
    taxa_aprovacao = round(df['qtdAprovado'].sum() / propostas * 100, 1)
    taxa_reprovacao = round(df['qtdNegado'].sum() / propostas * 100, 1)
    taxa_retorno_loja = round(df['qtdRetornadoLoja'].sum() / propostas * 100, 1)

    ns_hora = pd.DataFrame({
      'propostas': df.groupby('hora').apply(lambda x: x['qtdProposta'].sum()),
      'ns': df.groupby('hora').apply(lambda x: round(x['qtdDentroSla'].sum() / x['qtdProposta'].sum() * 100, 1))
    }).reset_index()
    
    data_response = {
      "data": {
        "clientes": str(clientes),
        "propostas": str(propostas),
        "hc": str(hc),
        "nivel_servico": str(nivel_servico),
        "concessao": str(concessao),
        "emprestimo": str(emprestimo),
        "limite": str(limite),
        "analise": str(analise),
        "desbloqueio": str(desbloqueio),
        "taxa_aprovacao": str(taxa_aprovacao),
        "taxa_reprovacao": str(taxa_reprovacao),
        "taxa_retorno_loja": str(taxa_retorno_loja),
        "json_hora": ns_hora.to_json(orient="records")
      },
      "updated": datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")
    }
    return JsonResponse(data_response)
  else:
    return HttpResponseNotFound('Not Found')