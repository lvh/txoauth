"""
Tests for txOAuth authentication servers.
"""
from txoauth.authserver import interfaces, cred

from twisted.trial.unittest import TestCase
from twisted.cred.portal import IRealm


class ClientTestCase(TestCase):
    def test_interface(self):
        self.assertTrue(interfaces.IClient.implementedBy(cred.Client))



class SimpleCallbackURLFactoryTestCase(TestCase):
    def setUp(self):
        self.empty = cred.SimpleCallbackURLFactory()
        self.withURLs = cred.SimpleCallbackURLFactory(spam="eggs")


    def test_interface(self):
        self.assertTrue(interfaces.ICallbackURLFactory
                        .implementedBy(cred.SimpleCallbackURLFactory))


    def test_missingURL(self):
        d = self.empty.get("blah")
        def cb(url):
            self.assertEquals(url, None)
        d.addCallback(cb)
        return d


    def test_registeredURL(self):
        d = self.withURLs.get("spam")
        def cb(url):
            self.assertEquals(url, "eggs")
        d.addCallback(cb)
        return d



class ClientRealmTestCase(TestCase):
    def setUp(self):
        self.urlFactory = cred.SimpleCallbackURLFactory(spam="eggs")


    def test_interface(self):
        self.assertTrue(IRealm.implementedBy(cred.ClientRealm))


    def test_simple(self):
        r = cred.ClientRealm(self.urlFactory)

        d = r.requestAvatar("spam", None, interfaces.IClient)
        def interfaceCheck(client):
            self.assertTrue(interfaces.IClient.providedBy(client))
            return client.getCallbackURL()
        d.addCallback(interfaceCheck)

        def callbackURLCheck(url):
            self.assertEquals(url, "eggs")
        d.addCallback(callbackURLCheck)

        return d


    def test_missingURL(self):
        r = cred.ClientRealm(self.urlFactory)

        d = r.requestAvatar("parrot", None, interfaces.IClient)
        def interfaceCheck(client):
            self.assertTrue(interfaces.IClient.providedBy(client))
            return client.getCallbackURL()
        d.addCallback(interfaceCheck)

        def callbackURLCheck(url):
            self.assertEquals(url, None)
        d.addCallback(callbackURLCheck)

        return d


    def test_multipleInterfaces(self):
        r = cred.ClientRealm(self.urlFactory)

        d = r.requestAvatar("spam", None, interfaces.IClient, object())
        def interfaceCheck(client):
            self.assertTrue(interfaces.IClient.providedBy(client))
            return client.getCallbackURL()
        d.addCallback(interfaceCheck)

        def callbackURLCheck(url):
            self.assertEquals(url, "eggs")
        d.addCallback(callbackURLCheck)

        return d


    def test_badInterface(self):
        r = cred.ClientRealm(self.urlFactory)
        self.assertRaises(NotImplementedError,
                          r.requestAvatar, "spam", None, object())
