from django.http import JsonResponse

from .helpers import run_clear_queue

def clearqueue(request, skill):
  json_result = run_clear_queue(skill)
  return JsonResponse(json_result)
