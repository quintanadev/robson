from django.core.management.base import BaseCommand
from django.utils import timezone
import time
# from services.control_desk.nicecxone.main import zera_fila

class Command(BaseCommand):
  help = 'Run Control Desk module to automate planning work'

  def add_arguments(self, parser):
    parser.add_argument(
      '--zerafila',
      action='store',
      # dest='skill',
      type=int,
      help='Inclui skill do receptivo nos agentes quando tiver fila',
    )
  
  def handle(self, *args, **options):
    if options['zerafila']:
      skill = options['zerafila']
      hour = timezone.now().strftime('%X')
      self.stdout.write(self.style.SUCCESS(f'Zerando a fila do skill: {skill} >>> %s' % hour))
      time.sleep(60.0)