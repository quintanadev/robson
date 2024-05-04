from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard-index'),
    path('inbound/', views.inbound, name='dashboard-inbound'),
    path('outbound/', views.inbound, name='dashboard-outbound'),
    path('whatsapp/', views.whatsapp, name='dashboard-whatsapp'),
    path('credito/', views.credito, name='dashboard-credito'),
]
