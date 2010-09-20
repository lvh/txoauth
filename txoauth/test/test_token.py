"""
Tests for token endpoints.
"""
from txoauth import token, clientcred as cred
from txoauth.test.test_clientcred import IDENTIFIER, BOGUS_IDENTIFIER, URI

from twisted.trial.unittest import TestCase


class _TokenRequestTests(TestCase):
    interface, implementer = None, None

    def setUp(self):
        self.credentials = cred.ClientIdentifier(IDENTIFIER, URI)
        self.bogusCredentials = cred.ClientIdentifier(BOGUS_IDENTIFIER, URI)
        self.tokenRequest = self.implementer(self.credentials,
                                             *self.args, **self.kwargs)


    def test_interface(self):
        self.assertTrue(token.ITokenRequest.implementedBy(self.implementer))
        self.assertTrue(self.interface.implementedBy(self.implementer))


    def test_keepCredentials(self):
        actual = self.tokenRequest.clientCredentials
        self.assertEqual(actual, self.credentials)


    def test_notCredentials(self):
        self.assertRaises(TypeError,
                          self.implementer, None, *self.args, **self.kwargs)


    def test_clientCredentialsImmutability_same(self):
        def mutateClient():
            self.assertion.clientCredentials = self.credentials
        self.assertRaises(AttributeError, mutateClient)


    def test_clientCredentialsImmutability_different(self):
        def mutateClient():
            self.assertion.clientCredentials = self.bogusCredentials
        self.assertRaises(AttributeError, mutateClient)



class BaseTokenRequestTestCase(_TokenRequestTests):
    interface, implementer = token.ITokenRequest, token._BaseTokenRequest
    args, kwargs = (), {}

TYPE, ASSERTION = "", ""
BOGUS_TYPE, BOGUS_ASSERTION = "", ""


class AssertionTests(_TokenRequestTests):
    interface, implementer = token.IAssertion, token.Assertion
    args, kwargs = (TYPE, ASSERTION), {}

    def test_simple(self):
        self.assertEqual(self.tokenRequest.assertionType, TYPE)
        self.assertEqual(self.tokenRequest.assertion, ASSERTION)


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
