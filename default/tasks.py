from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.core.mail import EmailMultiAlternatives

@shared_task
def send_mail_task(to_mail,link):
    subject, from_email, to = 'hello', 'elxjd.2014@gmail.com', to_mail
    text_content = 'Кликните по ссылке,чтобы активировать аккаунт'
    html_content = f'<a href="{link}">Link</a>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
@shared_task
def toplama(a,b):
    print(a+b)
