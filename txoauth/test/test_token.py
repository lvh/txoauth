"""
Tests for token endpoints.
"""
from txoauth import token, clientcred as cred
from txoauth.test.test_clientcred import IDENTIFIER, BOGUS_IDENTIFIER, URI

from twisted.trial.unittest import TestCase

TYPE, ASSERTION = "", ""
BOGUS_TYPE, BOGUS_ASSERTION = "", ""


class AssertionTests(TestCase):
    def setUp(self):
        self.credentials = cred.ClientIdentifier(IDENTIFIER, URI)
        self.bogusCredentials = cred.ClientIdentifier(BOGUS_IDENTIFIER, URI)
        self.assertion = token.Assertion(self.credentials, TYPE, ASSERTION)


    def test_interface(self):
        self.assertTrue(token.IAssertion.implementedBy(token.Assertion))


    def test_simple(self):
        self.assertEqual(self.assertion.client, self.credentials)
        self.assertEqual(self.assertion.assertionType, TYPE)
        self.assertEqual(self.assertion.assertion, ASSERTION)


    def test_clientImmutability_same(self):
        def mutateClient():
            self.assertion.client = self.credentials
        self.assertRaises(AttributeError, mutateClient)


    def test_clientImmutability_different(self):
        def mutateClient():
            self.assertion.client = self.bogusCredentials
        self.assertRaises(AttributeError, mutateClient)


    def test_assertionTypeImmutability_same(self):
        def mutateAssertionType():
            self.assertion.assertionType = TYPE
        self.assertRaises(AttributeError, mutateAssertionType)


    def test_assertionTypeImmutability_different(self):
        def mutateAssertionType():
            self.assertion.assertionType = BOGUS_TYPE
        self.assertRaises(AttributeError, mutateAssertionType)


    def test_assertionImmutability_same(self):
        def mutateAssertion():
            self.assertion.assertion = ASSERTION
        self.assertRaises(AttributeError, mutateAssertion)


    def test_assertionImmutability_different(self):
        def mutateAssertion():
            self.assertion.assertion = BOGUS_ASSERTION
        self.assertRaises(AttributeError, mutateAssertion)
