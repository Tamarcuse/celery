import os
import boto3
from celery import Celery
from celery.schedules import crontab
from datetime import datetime

access_key = os.getenv('ACCESS_KEY')
access_secret = os.getenv('ACCESS_SECRET')
AWS_REGION = "us-east-1"

broker_url = f"sqs://{access_key}:{access_secret}@"

app = Celery('tasks', broker=broker_url)
app.conf.broker_connection_retry_on_startup = True
app.conf.beat_schedule = {
  'run-every-minute': {
    'task': 'tasks.time',
    'schedule': crontab(minute='*'),
  },
  'run-weekly-task': {
    'task': 'tasks.send_ping_pong_email',
    'schedule': crontab(day_of_week=1, hour=19, minute=58),
  },
}

app.conf.timezone = 'Asia/Jerusalem'

ses = boto3.client(
    'ses',
    aws_access_key_id = access_key,
    aws_secret_access_key = access_secret,
    region_name = AWS_REGION
)

@app.task
def time():
  now = datetime.now()
  print(f"Current Time is: {now}")
  return now

@app.task
def send_ping_pong_email():
  SENDER    = "tamarcuse+123@gmail.com"
  RECIPIENT = "tamarcuse+321@gmail.com"
  SUBJECT   = "It's Time to Ping & Pong!"
  BODY_TEXT = "Ping Pong session!!"
  CHARSET   = "UTF-8"

  response = ses.send_email(
    Source=SENDER,
    Destination={ 'ToAddresses': [RECIPIENT] },
    Message={
      'Subject': { 'Data': SUBJECT, 'Charset': CHARSET },
      'Body': { 'Text': { 'Data': BODY_TEXT, 'Charset': CHARSET } }
    }
  )
  print("Email sent! Message ID is:", response['MessageId'])