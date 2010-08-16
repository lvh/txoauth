"""
Tests for txOAuth authentication servers.
"""
from txoauth.authserver import interfaces, cred

from twisted.trial.unittest import TestCase
from twisted.cred.portal import IRealm


IDENTIFIER, BOGUS_IDENTIFIER, URL = "spam", "parrot", "eggs"
urlFactory = cred.SimpleCallbackURLFactory(**{IDENTIFIER: URL})


class ClientTestCase(TestCase):
    def test_interface(self):
        self.assertTrue(interfaces.IClient.implementedBy(cred.Client))


    def _genericMemoizationTest(self, identifier):
        c = cred.Client(identifier, urlFactory)
        old = c._url
        d = c.getCallbackURL()
        @d.addCallback
        def testMemoization(url):
            self.assertNotEqual(old, url)


    def test_memoization_simple(self):
        self._genericMemoizationTest(IDENTIFIER)


    def test_memoization_missingURL(self):
        self._genericMemoizationTest(BOGUS_IDENTIFIER)



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
    def test_interface(self):
        self.assertTrue(IRealm.implementedBy(cred.ClientRealm))


    def _genericTest(self, identifier=IDENTIFIER, mind=None,
                     requestedInterfaces=(interfaces.IClient,),
                     expectedURL=URL):
        r = cred.ClientRealm(urlFactory)

        d = r.requestAvatar(identifier, mind, *requestedInterfaces)

        @d.addCallback
        def interfaceCheck(client):
            self.assertTrue(interfaces.IClient.providedBy(client))
            return client.getCallbackURL()

        @d.addCallback
        def callbackURLCheck(url):
            self.assertEquals(url, expectedURL)

        return d


    def test_simple(self):
        self._genericTest()


    def test_missingURL(self):
        self._genericTest(identifier="parrot", expectedURL=None)


    def test_multipleInterfaces(self):
        self._genericTest(requestedInterfaces=(interfaces.IClient, object()))


    def test_badInterface(self):
        r = cred.ClientRealm(urlFactory)
        self.assertRaises(NotImplementedError,
                          r.requestAvatar, "spam", None, object())
