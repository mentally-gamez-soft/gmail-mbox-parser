import unittest
from core.helpers import is_email


class TestHelpers(unittest.TestCase):
    def setUp(self) -> None:
        self.wrong_email = []
        self.wrong_email.append('hello_world@gmail..com')
        self.wrong_email.append('hello_world@gmailcom')
        self.wrong_email.append('hello_worldgmailcom')

     
    def test_validemail(self):
        email = 'hello_world@gmail.com'
        self.assertTrue(is_email(email), 'The email is invalid')

    def test_invalid_email(self):
        for email in self.wrong_email:
            self.assertFalse(is_email(email), 'The email is invalid')

