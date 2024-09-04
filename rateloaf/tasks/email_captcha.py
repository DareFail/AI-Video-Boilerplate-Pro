import json

from celery import shared_task
from django.conf import settings
from google.cloud import recaptchaenterprise_v1
from google.oauth2 import service_account

from ..utils import get_app_directory
from .slack import send_slack
from .email import sendGridSignup
from .marketing.forms import ContactForm


@shared_task
def handleEmailCaptcha(post):
    form = ContactForm(post)
    if form.is_valid():
        send_slack(
            get_app_directory()
            + " email: \n"
            + str(form.cleaned_data.get("email"))
        )
        if passesCaptcha(post.get("g-recaptcha-response")):
            sendGridSignup(form.cleaned_data.get("email"))
            send_slack("Added to Sendgrid: " + form.cleaned_data.get("email"))
            form.save()
        else:
            send_slack("Failed Captcha: " + form.cleaned_data.get("email"))


def passesCaptcha(captcha):

    credentials_dict = json.loads(settings.GOOGLE_APPLICATION_CREDENTIALS)

    credentials = service_account.Credentials.from_service_account_info(
        credentials_dict
    )

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient(
        credentials=credentials
    )

    event = recaptchaenterprise_v1.Event()
    event.site_key = settings.CAPTCHA_SITE_KEY
    event.token = captcha

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event

    asrequest = recaptchaenterprise_v1.CreateAssessmentRequest()
    asrequest.assessment = assessment
    asrequest.parent = "projects/" + settings.CAPTCHA_PROJECT

    response = client.create_assessment(asrequest)

    if response.token_properties.valid:
        if response.risk_analysis.score > 0:
            return True

        send_slack.delay(
            "Captcha: "
            + str(response.risk_analysis.score)
            + " \n Reasons: "
            + str(response.risk_analysis.reasons)
        )
    else:
        send_slack.delay(
            "Invalid Captcha: " + str(response.token_properties.invalid_reason)
        )

    return False
