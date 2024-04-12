from django.db import models

class Mailing(models.Model):
  dataMailing = models.DateField()
  cpf = models.CharField(max_length=11)
  mailing = models.CharField(max_length=100)
  grupoCarteira = models.CharField(max_length=50)
  faixaAtraso = models.CharField(max_length=50)
  familia = models.CharField(max_length=50)
  segmento = models.CharField(max_length=50)
  grupoOperacao = models.CharField(max_length=50)
  momentoAtraso = models.CharField(max_length=50)
  propensao = models.CharField(max_length=50)
  statusTratador = models.CharField(max_length=50)
  valorAtraso = models.DecimalField(max_digits=12, decimal_places=2)
  valorSaldo = models.DecimalField(max_digits=12, decimal_places=2)

  def __str__(self) -> str:
    return self.cpf

class NiceDisposition(models.Model):
  dispositionId = models.CharField(max_length=100, primary_key=True)
  dispositionName = models.CharField(max_length=100)
  notes = models.CharField(max_length=100)
  lastUpdated = models.CharField(max_length=100)
  classificationId = models.CharField(max_length=100)
  systemOutcome = models.CharField(max_length=100)
  isPreviewDisposition = models.CharField(max_length=100)

  def __str__(self) -> str:
    return self.dispositionName

class NiceContact(models.Model):
  abandoned = models.CharField(max_length=100)
  abandonSeconds = models.CharField(max_length=100)
  acwSeconds = models.CharField(max_length=100)
  agentId = models.CharField(max_length=100)
  agentSeconds = models.CharField(max_length=100)
  callbackTime = models.CharField(max_length=100)
  campaignId = models.CharField(max_length=100)
  campaignName = models.CharField(max_length=100)
  confSeconds = models.CharField(max_length=100)
  contactId = models.CharField(max_length=100, primary_key=True)
  contactStart = models.CharField(max_length=100)
  dateACWWarehoused = models.CharField(max_length=100)
  dateContactWarehoused = models.CharField(max_length=100)
  dispositionNotes = models.CharField(max_length=100)
  firstName = models.CharField(max_length=100)
  fromAddr = models.CharField(max_length=100)
  holdCount = models.CharField(max_length=100)
  holdSeconds = models.CharField(max_length=100)
  inQueueSeconds = models.CharField(max_length=100)
  isLogged = models.CharField(max_length=100)
  isOutbound = models.CharField(max_length=100)
  isRefused = models.CharField(max_length=100)
  isShortAbandon = models.CharField(max_length=100)
  isTakeover = models.CharField(max_length=100)
  lastName = models.CharField(max_length=100)
  lastUpdateTime = models.CharField(max_length=100)
  masterContactId = models.CharField(max_length=100)
  mediaType = models.CharField(max_length=100)
  mediaSubTypeId = models.CharField(max_length=100)
  mediaSubTypeName = models.CharField(max_length=100)
  mediaTypeName = models.CharField(max_length=100)
  pointOfContactId = models.CharField(max_length=100)
  pointOfContactName = models.CharField(max_length=100)
  postQueueSeconds = models.CharField(max_length=100)
  preQueueSeconds = models.CharField(max_length=100)
  primaryDispositionId = models.ForeignKey(NiceDisposition, blank=True, null=True, on_delete=models.CASCADE)
  refuseReason = models.CharField(max_length=100)
  refuseTime = models.CharField(max_length=100)
  releaseSeconds = models.CharField(max_length=100)
  routingTime = models.CharField(max_length=100)
  secondaryDispositionId = models.CharField(max_length=100)
  serviceLevelFlag = models.CharField(max_length=100)
  skillId = models.CharField(max_length=100)
  skillName = models.CharField(max_length=100)
  teamId = models.CharField(max_length=100)
  teamName = models.CharField(max_length=100)
  toAddr = models.CharField(max_length=100)
  totalDurationSeconds = models.CharField(max_length=100)
  transferIndicatorId = models.CharField(max_length=100)
  transferIndicatorName = models.CharField(max_length=100)
  isAnalyticsProcessed = models.CharField(max_length=100)
  analyticsProcessedDate = models.CharField(max_length=100)
  endReason = models.CharField(max_length=100)

  def __str__(self) -> str:
    return self.contact_id

class NiceSkill(models.Model):
  skillId = models.CharField(max_length=100, primary_key=True)
  skillName = models.CharField(max_length=100)
  campaignId = models.CharField(max_length=100)
  campaignName = models.CharField(max_length=100)
  notes = models.CharField(max_length=100)
  scriptName = models.CharField(max_length=100)
  callSuppressionScriptId = models.CharField(max_length=100)
  agentless = models.CharField(max_length=100)

  def __str__(self) -> str:
    return self.skillName

class NiceAgentState(models.Model):
  stateIndex = models.CharField(max_length=100)
  startDate = models.CharField(max_length=100)
  agentId = models.CharField(max_length=100)
  agentStateId = models.CharField(max_length=100)
  agentStateName = models.CharField(max_length=100)
  agentSessionId = models.CharField(max_length=100)
  contactId = models.CharField(max_length=100)
  skillId = models.CharField(max_length=100)
  skillName = models.CharField(max_length=100)
  mediaTypeId = models.CharField(max_length=100)
  mediaTypeName = models.CharField(max_length=100)
  fromAddress = models.CharField(max_length=100)
  toAddress = models.CharField(max_length=100)
  outStateId = models.CharField(max_length=100)
  outStateDescription = models.CharField(max_length=100)
  duration = models.CharField(max_length=100)
  isOutbound = models.CharField(max_length=100)
  isNaturalCalling = models.CharField(max_length=100)
  stationId = models.CharField(max_length=100)
  stationName = models.CharField(max_length=100)
  teamNo = models.CharField(max_length=100)

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