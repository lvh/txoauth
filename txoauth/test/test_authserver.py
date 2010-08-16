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


    def _genericMemoizationTest(self, identifier, expectedURL):
        c = cred.Client(identifier, urlFactory)
        v = {"old": c._url, "actual": None} # please backport nonlocal
        d = c.getCallbackURL()

        @d.addCallback
        def testMemoization(url):
            self.assertNotEqual(v["old"], url)
            v["actual"] = url # please, please backport nonlocal
            return c.getCallbackURL()
        @d.addCallback
        def testMemoized(url):
            self.assertNotEqual(v["old"], url)
            self.assertEqual(v["actual"], url)

        return d


    def test_memoization_simple(self):
        self._genericMemoizationTest(IDENTIFIER, URL)


    def test_memoization_missingURL(self):
        self._genericMemoizationTest(BOGUS_IDENTIFIER, None)



class SimpleCallbackURLFactoryTestCase(TestCase):
    def setUp(self):
        self.empty = cred.SimpleCallbackURLFactory()
        self.withURLs = cred.SimpleCallbackURLFactory(spam="eggs")


    def test_interface(self):
        self.assertTrue(interfaces.ICallbackURLFactory
                        .implementedBy(cred.SimpleCallbackURLFactory))


    def _genericFactoryTest(self, factory, identifier, expectedURL):
        d = factory.get(identifier)
        @d.addCallback
        def cb(url):
            self.assertEquals(url, expectedURL)
        return d


    def test_empty(self):
        self._genericFactoryTest(self.empty, IDENTIFIER, None)


    def test_registeredURL(self):
        self._genericFactoryTest(urlFactory, IDENTIFIER, URL)


    def test_missingURL(self):
        self._genericFactoryTest(urlFactory, BOGUS_IDENTIFIER, None)



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
