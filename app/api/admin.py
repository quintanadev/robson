from django.contrib import admin
from .models import NiceContact, NiceAgentState, NiceDisposition, NiceSkill, Forecast, Mailing

admin.site.register(NiceContact)
admin.site.register(NiceAgentState)
admin.site.register(NiceDisposition)
admin.site.register(NiceSkill)
admin.site.register(Forecast)
admin.site.register(Mailing)
