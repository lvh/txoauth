"""
OAuth token endpoint support.
"""
from zope.interface import Attribute, Interface


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
