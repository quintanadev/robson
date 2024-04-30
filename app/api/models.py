from django.db import models

class NiceDisposition(models.Model):
  dispositionId = models.CharField(max_length=100, primary_key=True)
  dispositionName = models.CharField(max_length=100, null=True)
  notes = models.CharField(max_length=100, null=True)
  lastUpdated = models.CharField(max_length=100, null=True)
  classificationId = models.CharField(max_length=100, null=True)
  systemOutcome = models.CharField(max_length=100, null=True)
  isPreviewDisposition = models.CharField(max_length=100, null=True)

  def __str__(self) -> str:
    return self.dispositionName

class NiceClassification(models.Model):
  classificationId = models.CharField(max_length=100, primary_key=True)
  businessUnitId = models.CharField(max_length=100, null=True)
  classificationName = models.CharField(max_length=100, null=True)
  classificationTypeId = models.CharField(max_length=100, null=True)
  direction = models.CharField(max_length=100, null=True)
  dialingOutcomeId = models.CharField(max_length=100, null=True)
  reportingGroupId = models.CharField(max_length=100, null=True)
  description = models.CharField(max_length=100, null=True)
  showCommitmentAmount = models.CharField(max_length=100, null=True)
  showRescheduleDate = models.CharField(max_length=100, null=True)
  isAgentSpecific = models.CharField(max_length=100, null=True)
  isDestinationFinal = models.CharField(max_length=100, null=True)
  isContactFinal = models.CharField(max_length=100, null=True)
  excludeFromSerialDelivery = models.CharField(max_length=100, null=True)
  carryoverForCallback = models.CharField(max_length=100, null=True)

  def __str__(self) -> str:
    return self.classificationName

class NiceSkill(models.Model):
  skillId = models.CharField(max_length=100, primary_key=True)
  skillName = models.CharField(max_length=100, null=True)
  campaignId = models.CharField(max_length=100, null=True)
  campaignName = models.CharField(max_length=100, null=True)
  notes = models.CharField(max_length=100, null=True)
  scriptName = models.CharField(max_length=100, null=True)
  callSuppressionScriptId = models.CharField(max_length=100, null=True)
  agentless = models.CharField(max_length=100, null=True)

  def __str__(self) -> str:
    return self.skillName

class NiceAgent(models.Model):
  agentId = models.CharField(max_length=100, primary_key=True)
  userName = models.CharField(max_length=100, null=True)
  firstName = models.CharField(max_length=100, null=True)
  lastName = models.CharField(max_length=100, null=True)
  teamId = models.CharField(max_length=100, null=True)
  teamName = models.CharField(max_length=100, null=True)
  lastLogin = models.CharField(max_length=100, null=True)
  custom1 = models.CharField(max_length=100, null=True)
  custom2 = models.CharField(max_length=100, null=True)
  custom3 = models.CharField(max_length=100, null=True)
  custom4 = models.CharField(max_length=100, null=True)
  custom5 = models.CharField(max_length=100, null=True)
  profileName = models.CharField(max_length=100, null=True)
  notes = models.CharField(max_length=100, null=True)
  createDate = models.CharField(max_length=100, null=True)

  def __str__(self) -> str:
    return self.userName


class Mailing(models.Model):
  dataMailing = models.DateField()
  cpf = models.CharField(max_length=11)
  mailing = models.CharField(max_length=100, null=True)
  grupoCarteira = models.CharField(max_length=50, null=True)
  faixaAtraso = models.CharField(max_length=50, null=True)
  familia = models.CharField(max_length=50, null=True)
  segmento = models.CharField(max_length=50, null=True)
  grupoOperacao = models.CharField(max_length=50, null=True)
  momentoAtraso = models.CharField(max_length=50, null=True)
  propensao = models.CharField(max_length=50, null=True)
  statusTratador = models.CharField(max_length=50, null=True)
  valorAtraso = models.DecimalField(max_digits=12, decimal_places=2, null=True)
  valorSaldo = models.DecimalField(max_digits=12, decimal_places=2, null=True)

  def __str__(self) -> str:
    return self.cpf

class NiceContact(models.Model):
  abandoned = models.CharField(max_length=100, null=True)
  abandonSeconds = models.CharField(max_length=100, null=True)
  acwSeconds = models.CharField(max_length=100, null=True)
  agentId = models.CharField(max_length=100, null=True)
  agentSeconds = models.CharField(max_length=100, null=True)
  callbackTime = models.CharField(max_length=100, null=True)
  campaignId = models.CharField(max_length=100, null=True)
  campaignName = models.CharField(max_length=100, null=True)
  confSeconds = models.CharField(max_length=100, null=True)
  contactId = models.CharField(max_length=100, primary_key=True)
  contactStart = models.CharField(max_length=100, null=True)
  dateACWWarehoused = models.CharField(max_length=100, null=True)
  dateContactWarehoused = models.CharField(max_length=100, null=True)
  dispositionNotes = models.CharField(max_length=100, null=True)
  firstName = models.CharField(max_length=100, null=True)
  fromAddr = models.CharField(max_length=100, null=True)
  holdCount = models.CharField(max_length=100, null=True)
  holdSeconds = models.CharField(max_length=100, null=True)
  inQueueSeconds = models.CharField(max_length=100, null=True)
  isLogged = models.CharField(max_length=100, null=True)
  isOutbound = models.CharField(max_length=100, null=True)
  isRefused = models.CharField(max_length=100, null=True)
  isShortAbandon = models.CharField(max_length=100, null=True)
  isTakeover = models.CharField(max_length=100, null=True)
  lastName = models.CharField(max_length=100, null=True)
  lastUpdateTime = models.CharField(max_length=100, null=True)
  masterContactId = models.CharField(max_length=100, null=True)
  mediaType = models.CharField(max_length=100, null=True)
  mediaSubTypeId = models.CharField(max_length=100, null=True)
  mediaSubTypeName = models.CharField(max_length=100, null=True)
  mediaTypeName = models.CharField(max_length=100, null=True)
  pointOfContactId = models.CharField(max_length=100, null=True)
  pointOfContactName = models.CharField(max_length=100, null=True)
  postQueueSeconds = models.CharField(max_length=100, null=True)
  preQueueSeconds = models.CharField(max_length=100, null=True)
  primaryDispositionId = models.CharField(max_length=100, null=True)
  refuseReason = models.CharField(max_length=100, null=True)
  refuseTime = models.CharField(max_length=100, null=True)
  releaseSeconds = models.CharField(max_length=100, null=True)
  routingTime = models.CharField(max_length=100, null=True)
  secondaryDispositionId = models.CharField(max_length=100, null=True)
  serviceLevelFlag = models.CharField(max_length=100, null=True)
  skillId = models.CharField(max_length=100, null=True)
  skillName = models.CharField(max_length=100, null=True)
  teamId = models.CharField(max_length=100, null=True)
  teamName = models.CharField(max_length=100, null=True)
  toAddr = models.CharField(max_length=100, null=True)
  totalDurationSeconds = models.CharField(max_length=100, null=True)
  transferIndicatorId = models.CharField(max_length=100, null=True)
  transferIndicatorName = models.CharField(max_length=100, null=True)
  isAnalyticsProcessed = models.CharField(max_length=100, null=True)
  analyticsProcessedDate = models.CharField(max_length=100, null=True)
  endReason = models.CharField(max_length=100, null=True)

  def __str__(self) -> str:
    return self.contact_id

class NiceAgentState(models.Model):
  stateIndex = models.CharField(max_length=100, null=True)
  startDate = models.CharField(max_length=100, null=True)
  agentId = models.CharField(max_length=100, null=True)
  agentStateId = models.CharField(max_length=100, null=True)
  agentStateName = models.CharField(max_length=100, null=True)
  agentSessionId = models.CharField(max_length=100, null=True)
  contactId = models.CharField(max_length=100, null=True)
  skillId = models.CharField(max_length=100, null=True)
  skillName = models.CharField(max_length=100, null=True)
  mediaTypeId = models.CharField(max_length=100, null=True)
  mediaTypeName = models.CharField(max_length=100, null=True)
  fromAddress = models.CharField(max_length=100, null=True)
  toAddress = models.CharField(max_length=100, null=True)
  outStateId = models.CharField(max_length=100, null=True)
  outStateDescription = models.CharField(max_length=100, null=True)
  duration = models.CharField(max_length=100, null=True)
  isOutbound = models.CharField(max_length=100, null=True)
  isNaturalCalling = models.CharField(max_length=100, null=True)
  stationId = models.CharField(max_length=100, null=True)
  stationName = models.CharField(max_length=100, null=True)
  teamNo = models.CharField(max_length=100, null=True)

  def __str__(self) -> str:
    return f"{self.agentId} - {self.stateIndex} - {self.agentSessionId}"

class Forecast(models.Model):
  data = models.DateField()
  intervalo = models.CharField(max_length=8)
  volume = models.DecimalField(max_digits=20, decimal_places=13)
  tmo = models.DecimalField(max_digits=20, decimal_places=13)
  abandono = models.DecimalField(max_digits=20, decimal_places=13)
  agentesSemIndisp = models.DecimalField(max_digits=20, decimal_places=13)
  agentesComIndisp = models.DecimalField(max_digits=20, decimal_places=13)
  nivelServico = models.DecimalField(max_digits=20, decimal_places=13)
  trafego = models.DecimalField(max_digits=20, decimal_places=13)
  atendidasNivelServico = models.DecimalField(max_digits=20, decimal_places=13)

  def __str__(self) -> str:
    return f"{self.data} - {self.intervalo}"
  
class PortalRealizeEncerradas(models.Model):
  cpf = models.CharField(max_length=14, null=True)
  nome = models.CharField(max_length=100, null=True)
  tipoAnalise = models.CharField(max_length=100, null=True)
  produto = models.CharField(max_length=100, null=True)
  cartao = models.CharField(max_length=100, null=True)
  canal = models.CharField(max_length=100, null=True)
  captacao = models.CharField(max_length=100, null=True)
  numeroProposta = models.CharField(max_length=100, null=True)
  situacao = models.CharField(max_length=100, null=True)
  dataInicio = models.CharField(max_length=100, null=True)
  horaInicio = models.CharField(max_length=100, null=True)
  dataFim = models.CharField(max_length=100, null=True)
  horaFim = models.CharField(max_length=100, null=True)
  tempoFila = models.CharField(max_length=100, null=True)
  tempoAnalise = models.CharField(max_length=100, null=True)
  tempoTotal = models.CharField(max_length=100, null=True)

  def __str__(self) -> str:
    return self.cpf
  
class DatabricksFatoMailing(models.Model):
  periodo = models.IntegerField(null=True)
  dataMailing = models.DateField(null=True)
  familia = models.CharField(max_length=10, null=True)
  segmento = models.CharField(max_length=20, null=True)
  faixaAtraso = models.CharField(max_length=10, null=True)
  momentoAtraso = models.CharField(max_length=20, null=True)
  propensao = models.CharField(max_length=20, null=True)
  qtdClientes = models.IntegerField(null=True)
  valorAtraso = models.FloatField(null=True)
  valorSaldo = models.FloatField(null=True)
  qtdTentativas = models.IntegerField(null=True)
  qtdAlo = models.IntegerField(null=True)
  qtdLocalizado = models.IntegerField(null=True)
  qtdCpc = models.IntegerField(null=True)
  qtdTarget = models.IntegerField(null=True)
  qtdSucesso = models.IntegerField(null=True)
  qtdTentativasUnique = models.IntegerField(null=True)
  qtdAloUnique = models.IntegerField(null=True)
  qtdLocalizadoUnique = models.IntegerField(null=True)
  qtdCpcUnique = models.IntegerField(null=True)
  qtdTargetUnique = models.IntegerField(null=True)
  qtdSucessoUnique = models.IntegerField(null=True)
  qtdPagamentoUnique = models.IntegerField(null=True)
  qtdDiasMailing = models.IntegerField(null=True)

  def __str__(self) -> str:
    return f"{self.dataMailing} - {self.segmento} - {self.familia} - {self.faixaAtraso}"

class DatabricksAnaliticoNegocio(models.Model):
  periodo = models.IntegerField(null=True)
  periodoNegocio = models.IntegerField(null=True)
  periodoVencimento = models.IntegerField(null=True)
  periodoPagamento = models.IntegerField(null=True)
  tipoNegocio = models.CharField(max_length=20, null=True)
  dataNegocio = models.DateField(null=True)
  dataVencimento = models.DateField(null=True)
  dataPagamento = models.DateField(null=True)
  cpf = models.CharField(max_length=11, null=True)
  usuario = models.CharField(max_length=20, null=True)
  diasAtraso = models.IntegerField(null=True)
  segmento = models.CharField(max_length=20, null=True)
  familia = models.CharField(max_length=20, null=True)
  faixaAtraso = models.CharField(max_length=10, null=True)
  canal = models.CharField(max_length=20, null=True)
  qtdNegocios = models.IntegerField(null=True)
  qtdPagamentos = models.IntegerField(null=True)
  qtdQuebras = models.IntegerField(null=True)
  parcelamento = models.IntegerField(null=True)
  faixaParcelamento = models.CharField(max_length=20, null=True)
  diasVencimento = models.IntegerField(null=True)
  nomeColaborador = models.CharField(max_length=100, null=True)
  nomeLider = models.CharField(max_length=100, null=True)
  tipoCargo = models.CharField(max_length=50, null=True)
  valorDivida = models.FloatField(null=True)
  valorNegociado = models.FloatField(null=True)
  valorPagamento = models.FloatField(null=True)
  valorSaldoCadoc = models.FloatField(null=True)
  faixaAtrasoCadoc = models.CharField(max_length=10, null=True)

  def __str__(self) -> str:
    return f"{self.cpf} - {self.tipoNegocio}"