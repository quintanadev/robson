from django.urls import path

from . import views

urlpatterns = [
    path('inbound/cards/', views.inbound_cards, name='inbound_cards'),
]
