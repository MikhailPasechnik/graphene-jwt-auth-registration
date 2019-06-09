
from django.core import mail
from gjwt_auth.utils import send_activation_email, send_password_reset_email
from .testcases import Gjwt_authTestCase


class TestGjwt_auth_utils(Gjwt_authTestCase):

    def test_send_activtion_email(self):
        request = self.rf.request()
        send_activation_email(self.user, request)
        assert len(mail.outbox) == 1

    def test_send_password_reset_email(self):
        request = self.rf.request()
        send_password_reset_email(self.user, request)
        assert len(mail.outbox) == 1
