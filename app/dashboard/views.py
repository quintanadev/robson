from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
import folium.map

def index(request):
  if request.method == 'GET':
    return render(request, 'index.html')
  
  else:
    return HttpResponseNotFound('Not Found')

def inbound(request):
  if request.method == 'GET':
    return render(request, 'inbound.html')
  
  else:
    return HttpResponseNotFound('Not Found')

def outbound(request):
  if request.method == 'GET':
    return render(request, 'outbound.html')
  
  else:
    return HttpResponseNotFound('Not Found')

def whatsapp(request):
  if request.method == 'GET':
    return render(request, 'whatsapp.html')
  
  else:
    return HttpResponseNotFound('Not Found')

def users_online(request):
  if request.method == 'GET':
    return render(request, 'users-online.html')
  
  else:
    return HttpResponseNotFound('Not Found')

def credito(request):
  if request.method == 'GET':
    return render(request, 'credito.html')
  
  else:
    return HttpResponseNotFound('Not Found')

def users_map(request):
  if request.method == 'GET':
    return render(request, 'users-map.html')
  
  else:
    return HttpResponseNotFound('Not Found')

def maps(request):
  if request.method == 'GET':
    return render(request, 'maps.html')
  
  else:
    return HttpResponseNotFound('Not Found')
