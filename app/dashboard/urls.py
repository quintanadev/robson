from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard-index'),
    path('inbound/', views.inbound, name='dashboard-inbound'),
    path('outbound/', views.outbound, name='dashboard-outbound'),
    path('whatsapp/', views.whatsapp, name='dashboard-whatsapp'),
    path('users/', views.users, name='dashboard-users'),
    path('credito/', views.credito, name='dashboard-credito'),
    path('users-map/', views.users_map, name='users-map'),
]
