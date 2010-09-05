"""
Tests for contributed txOAuth code.
"""
from txoauth.authserver import interfaces
from txoauth.contrib.simple import SimpleCallbackURLFactory
from txoauth.test.test_authserver import IDENTIFIER, BOGUS_IDENTIFIER, URI

from twisted.trial.unittest import TestCase


class SimpleCallbackURLFactoryTestCase(TestCase):
    def setUp(self):
        self.empty = SimpleCallbackURLFactory()
        self.withURLs = SimpleCallbackURLFactory(**{IDENTIFIER: URI})


    def test_interface(self):
        self.assertTrue(interfaces.ICallbackURLFactory
                        .implementedBy(SimpleCallbackURLFactory))


    def _genericFactoryTest(self, factory, identifier, expectedURL):
        d = factory.get(identifier)
        @d.addCallback
        def cb(url):
            self.assertEquals(url, expectedURL)
        return d


    def test_empty(self):
        self._genericFactoryTest(self.empty, IDENTIFIER, None)


    def test_registeredURL(self):
        self._genericFactoryTest(self.withURLs, IDENTIFIER, URI)


    def test_missingURL(self):
        self._genericFactoryTest(self.withURLs, BOGUS_IDENTIFIER, None)
