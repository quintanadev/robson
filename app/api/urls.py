from django.urls import path

from . import views

urlpatterns = [
    path('inbound/cards/', views.realtime_inbound_cards, name='realtime_inbound_cards'),
    path('inbound/dispositions/', views.realtime_dispositions, name='realtime_dispositions'),
    path('inbound/whatsapp/', views.realtime_whatsapp, name='realtime_whatsapp'),
    path('inbound/credito/', views.dashboard_credito, name='dashboard_credito'),
    path('users/dashboard/', views.realtime_users_dashboard, name='realtime_users_dashboard'),
    path('outbound/dashboard/', views.realtime_outbound_dashboard, name='realtime_outbound'),
    path('users/map/', views.users_map, name='api_users_map'),
]
