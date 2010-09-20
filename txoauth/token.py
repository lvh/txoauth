"""
OAuth token endpoint support.
"""
from txoauth.clientcred import IClientIdentifier
from txoauth._twisted import FancyHashMixin

from zope.interface import Attribute, Interface, implements


class ITokenRequest(Interface):
    clientCredentials = Attribute(
        """
        The client credentials used in the request.

        @type: L{txoauth.clientcred.IClientIdentifier}
        """)



class IAssertion(ITokenRequest):
    """
    A token request in the form of an assertion.
    """
    assertionType = Attribute(
        """
        The type of this assertion.

        @type: C{str}
        """)

    assertion = Attribute(
        """
        The value of this assertion.

        @type: C{str}
        """)



class _BaseTokenRequest(object, FancyHashMixin):
    implements(ITokenRequest)
    compareAttributes = hashAttributes = ("clientCredentials",)

    def __init__(self, clientCredentials):
        self._clientCredentials = IClientIdentifier(clientCredentials)


    @property
    def clientCredentials(self):
        return self._clientCredentials



class Assertion(_BaseTokenRequest):
    """
    A token request in the form of an assertion.
    """
    implements(IAssertion)
    compareAttributes = hashAttributes = ("clientCredentials",
                                          "assertion",
                                          "assertionType")

    def __init__(self, clientCredentials, assertionType, assertion):
        super(Assertion, self).__init__(clientCredentials)
        self._assertionType = assertionType
        self._assertion = assertion


    @property
    def assertionType(self):
        return self._assertionType


    @property
    def assertion(self):
       return self._assertion



class EnforcedInvalidationException(Exception):
    """
    Raised when attempting to check an assertion while not invalidating the
    assertion, if the L{txoauth.interfaces.IAssertionStore} does not allow
    that operation.
    """



class AssertionNotFound(Exception):
    """
    Raised when an assertion which was attempted to be checked wasn't found.
    """
