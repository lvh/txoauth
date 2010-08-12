"""
Tests for txOAuth authentication servers.
"""
from txoauth.authserver import interfaces, cred

from twisted.trial.unittest import TestCase


class ClientTest(TestCase):
    def test_interface(self):
        c = cred.Client("")
        self.assertTrue(interfaces.IClient.providedBy(c))

    def test_simple(self):
        url = "http://hellowor.ld/cb"
        c = cred.Client(url)
        self.assertEquals(c.callbackURL, url)

    def test_immutability(self):
        c = cred.Client("")
        def mutate():
            c.callbackURL = "hi"
        self.assertRaises(AttributeError, mutate)
