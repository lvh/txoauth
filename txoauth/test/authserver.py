"""
Tests for txOAuth authentication servers.
"""
from txoauth.authserver import interfaces, cred

from twisted.trial.unittest import TestCase


class ClientTestCase(TestCase):
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



class SimpleCallbackURLFactoryTestCase(TestCase):
    def setUp(self):
        self.empty = cred.SimpleCallbackURLFactory()
        self.withURLs = cred.SimpleCallbackURLFactory(spam="eggs")


    def test_interface(self):
        for f in (self.empty, self.withURLs):
            self.assertTrue(interfaces.ICallbackURLFactory.providedBy(f))


    def test_simple_missingURL(self):
        d = self.empty.get("blah")
        def cb(url):
            self.assertEquals(url, None)
        d.addCallback(cb)
        return d


    def test_simple_registeredURL(self):
        d = self.withURLs.get("spam")
        def cb(url):
            self.assertEquals(url, "eggs")
        d.addCallback(cb)
        return d