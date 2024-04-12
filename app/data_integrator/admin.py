from django.contrib import admin
from .models import Contact, Mailing, AgentState

admin.site.register(Contact)
admin.site.register(Mailing)
admin.site.register(AgentState)