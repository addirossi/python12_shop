from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_activation_mail(email, activation_code):
    message = f"""
            Благодарим Вас за регистрацию на нашем сайте.
            Ваш код активации: {activation_code}
            """
    send_mail('Активация аккаунта',
              message,
              'test@gmail.com',
              [email],
              )


@shared_task
def notify_user():
    send_mail('Вечерний дайджест',
              'Привет!',
              'test@gmail.com',
              ['addirossi@gmail.com'])

