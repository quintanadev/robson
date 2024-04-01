from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='dashboard-index'),
    path('inbound/', views.inbound, name='dashboard-inbound'),
    path('whatsapp/', views.whatsapp, name='dashboard-whatsapp'),
]
