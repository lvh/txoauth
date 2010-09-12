"""
Tests for simple txOAuth implementations.
"""
from txoauth import interfaces, token, clientcred
from txoauth.contrib import simple
from txoauth.test.test_clientcred import IDENTIFIER, BOGUS_IDENTIFIER, URI
from txoauth.test.test_token import TYPE, ASSERTION
from txoauth.test.test_token import BOGUS_TYPE, BOGUS_ASSERTION

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
        c = clientcred.ClientIdentifier(IDENTIFIER, URI)
        self.assertion = token.Assertion(c, TYPE, ASSERTION)
        self.bogusAssertion = token.Assertion(c, BOGUS_TYPE, BOGUS_ASSERTION)

        self.store = simple.SimpleAssertionStore()
        self.store.addAssertion(self.assertion)

        self.store2 = simple.SimpleAssertionStore(forceInvalidation=False)
        self.store2.addAssertion(self.assertion)


    def test_interface(self):
        self.assertTrue(interfaces.IAssertionStore
                        .implementedBy(simple.SimpleAssertionStore))


    def _test_simple(self, store):
        d = store.checkAssertion(self.assertion)

        @d.addCallback
        def cb(_):
            return store.checkAssertion(self.assertion)

        @d.addErrback
        def eb(failure):
            failure.trap("MISSING") # TODO: exceptions

        return d


    def test_simple(self):
        return self._test_simple(self.store)


    def test_simple_noForceInvalidation(self):
        return self._test_simple(self.store2)


    def _test_missing(self, store):
        d = store.checkAssertion(self.bogusAssertion)

        @d.addErrback
        def eb(failure):
            failure.trap("MISSING") # TODO: exceptions


    def test_missing(self):
        self._test_missing(self.store)


    def test_missing_noForceInvalidation(self):
        self._test_missing(self.store2)


    def test_noInvalidation(self):
        store = self.store2
        def getAssertion():
            return store.checkAssertion(self.assertion, invalidate=False)

        d = getAssertion()
        @d.addCallback
        def tryAgain(_):
            return getAssertion()


    def test_enforcedInvalidation(self):
        d = self.store.checkAssertion(self.assertion, invalidate=False)

        @d.addErrback
        def eb(failure):
            failure.trap(token.EnforcedInvalidationException)
