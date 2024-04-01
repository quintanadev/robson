from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound

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

def whatsapp(request):
  if request.method == 'GET':
    return render(request, 'whatsapp.html')
  
  else:
    return HttpResponseNotFound('Not Found')
