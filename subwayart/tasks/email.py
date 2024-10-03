import http.client

from celery import shared_task
from django.conf import settings

from ..utils import get_app_directory
from .slack import send_slack, send_slack_exception
from ..forms import ContactForm


@shared_task
def handleEmail(post):
    form = ContactForm(post)
    if form.is_valid():
        send_slack(
            get_app_directory()
            + " email: \n"
            + str(form.cleaned_data.get("email"))
        )
        sendGridSignup(form.cleaned_data.get("email"))
        send_slack("Added to Sendgrid: " + form.cleaned_data.get("email"))
        form.save()


def sendGridSignup(email):
    try:

        conn = http.client.HTTPSConnection("api.sendgrid.com")

        payload = '{"contacts":[{"email":"' + email + '"}]}'

        headers = {
            "authorization": "Bearer " + settings.SENDGRID_API_KEY,
            "content-type": "application/json",
        }

        conn.request("PUT", "/v3/marketing/contacts", payload, headers)

        res = conn.getresponse()
        res.read()
    except Exception as e:
        send_slack_exception.delay(e)
