"""
OAuth token endpoint support.
"""
from zope.interface import Attribute, Interface, implements


class ITokenRequest(Interface):
    client = Attribute(
        """
        The authenticated client making the request.

        @type: L{txoauth.clientcred.IClient}
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



class Assertion(object):
    """
    A token request in the form of an assertion.
    """
    implements(IAssertion)

    def __init__(self, client, assertionType, assertion):
        self._client = client
        self._assertionType = assertionType
        self._assertion = assertion


    @property
    def client(self):
        return self._client


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

    The OAuth specification asserts that assertions should be invalidated.
    """
