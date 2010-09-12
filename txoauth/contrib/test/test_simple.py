"""
Tests for simple txOAuth implementations.
"""
from txoauth import interfaces
from txoauth.contrib import simple
from txoauth.test.test_clientcred import IDENTIFIER, BOGUS_IDENTIFIER, URI

from twisted.trial.unittest import TestCase


class SimpleRedirectURIFactoryTestCase(TestCase):
    def setUp(self):
        self.empty = simple.SimpleRedirectURIFactory()
        self.withURLs = simple.SimpleRedirectURIFactory(**{IDENTIFIER: URI})


    def test_interface(self):
        self.assertTrue(interfaces.IRedirectURIFactory
                        .implementedBy(simple.SimpleRedirectURIFactory))


    def _genericFactoryTest(self, factory, identifier, expectedURL):
        d = factory.getRedirectURI(identifier)
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



class SimpleAssertionStoreTestCase(TestCase):
    def setUp(self):
        self.store = simple.SimpleAssertionStore()
        self.noInvalidationStore = simple.SimpleAssertionStore

    def test_interface(self):
        self.assertTrue(interfaces.IAssertionStore
                        .implementedBy(simple.SimpleAssertionStore))
