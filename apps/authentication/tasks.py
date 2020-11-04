import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template

logger = logging.getLogger("celery")


@shared_task()
def send_email(subject: str, template_txt: str, template_html: str, context: dict, recipients: list):
    """
    Sending emails
    :param subject: message title
    :param template_txt: name of txt template
    :param template_html: name of html template
    :param context: message data in dict format
    :param recipients: list of receivers
    :return:
    """
    text_content = render_to_string(get_template(template_txt), context)
    html_content = render_to_string(get_template(template_html), context)
    msg = EmailMultiAlternatives(subject, text_content, settings.BCRM_INFO_EMAIL, recipients)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    logger.info(f"Email sent to {recipients}")
