from django.test import TestCase, RequestFactory
from django.utils import timezone
from core.models import Debtor
from users.models import Profile
from django.contrib.auth.models import User
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from . import views

class DebtorTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username="user1",
        )    
        self.debtor1 = Debtor.objects.create(
            name="Debtor 1",
            amount_owed=2000,
            email='debtor1@test.com',
            created_by=self.user.profile,
        )


    def test_sendmail(self):
        request = self.factory.get(f'/action_sendmail/{self.debtor1.id}')

        profile_email = self.user.profile.email = 'teste78458@gmail.com'
        profile_password = self.user.profile.password = 'qasde321'

        request.user = self.user

        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        middleware = MessageMiddleware()
        middleware.process_request(request)
        request.session.save()
    
        self.assertFalse(self.debtor1.last_email_sent)

        views.sendmail(request, profile_email, self.debtor1, profile_password)

        self.assertTrue(self.debtor1.last_email_sent)

        profile_email = self.user.profile.email = 'tes78458@gmail.com'
        self.debtor1.last_email_sent = False

        views.sendmail(request, profile_email, self.debtor1, profile_password)

        self.assertFalse(self.debtor1.last_email_sent)
