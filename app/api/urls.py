from django.urls import path

from . import views

urlpatterns = [
    path('inbound/cards/', views.realtime_inbound_cards, name='realtime_inbound_cards'),
    path('inbound/dispositions/', views.realtime_dispositions, name='realtime_dispositions'),
    path('inbound/whatsapp/', views.realtime_whatsapp, name='realtime_whatsapp'),
]
