import requests
import json

from celery import shared_task
from django.conf import settings


@shared_task
def send_slack(message):
    slack_msg = {"text": message}
    requests.post(settings.SLACK_GENERAL, data=json.dumps(slack_msg))


@shared_task
def send_slack_exception(message):
    slack_msg = {"text": message}
    requests.post(settings.SLACK_EXCEPTIONS, data=json.dumps(slack_msg))
