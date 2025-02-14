import datetime

from django.http import HttpRequest, HttpResponse
from django.views.generic import View

from sentry.models import Authenticator
from sentry.security.emails import generate_security_email

from .mail import MailPreview


class DebugMfaAddedEmailView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        authenticator = Authenticator(id=0, type=3, user=request.user)  # u2f

        email = generate_security_email(
            account=request.user,
            actor=request.user,
            type="mfa-added",
            ip_address=request.META["REMOTE_ADDR"],
            context={"authenticator": authenticator, "device_name": "Home computer"},
            # make this consistent for acceptance tests
            current_datetime=datetime.datetime(2017, 1, 20, 21, 39, 23, 30723),
        )
        return MailPreview(
            html_template=email.html_template, text_template=email.template, context=email.context
        ).render(request)
