# sgCPA/celeryconfig.py
from celery.schedules import crontab

app.conf.beat_schedule = {
    'check-and-send-emails-daily': {
        'task': 'sgCPA.celery.check_and_send_emails',
        'schedule': crontab(hour=0, minute=0),  # Ajusta el horario según sea necesario
    },
}