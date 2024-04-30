from django.urls import path

from . import views

urlpatterns = [
    path('clearqueue/<int:skill>/', views.clearqueue, name='controldesk-clearqueue'),
]
