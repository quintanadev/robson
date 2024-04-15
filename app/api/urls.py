from django.urls import path

from . import views

urlpatterns = [
    path('inbound/cards/', views.inbound_cards, name='inbound_cards'),
    path('inbound/dispositions/', views.get_dispositions_list, name='get_dispositions_list'),
]
