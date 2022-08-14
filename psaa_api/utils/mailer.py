from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


class RegistrationMail:
    """
        Email class for sending registration mail
    """
    def __init__(self, data):
        self.user = data.get("user")
        self.school = data.get('name')

    def compose_mail(self):
        """
        Composes the email
        """
        html_body = render_to_string(
            template_name="mail.html",
            context={
                "name": self.user['username'],
                'school': self.school,
                "url": settings.URL_PREFIX+'login'
            }
        )
        self.message = EmailMultiAlternatives(
            subject="Welcome {}".format(self.user['username']),
            body="registration email",
            from_email=settings.DEFAULT_EMAIL,
            to=[self.user['email']]
        )
        self.message.attach_alternative(html_body, "text/html")

    def send_mail(self):
        """
        Sends the composed email
        """
        self.compose_mail()
        self.message.send()
