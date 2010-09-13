"""
Public OAuth interfaces.

These are interfaces you are likely to have to implement when building
applications powered by OAuth.
"""
from twisted.cred.credentials import ICredentials

from zope.interface import Interface, Attribute


class IClient(Interface):
    """
    A representation of an OAuth client.
    """
    identifier = Attribute(
        """
        The identifier for this client

        @type: C{str}
        """)

    def getRedirectURI():
        """
        Gets the registered redirect URI for this client.

        @rtype: C{Deferred}
        @return: A C{Deferred} which will fire with the URI, or C{None} if no
        URI has been registered.
        """



class IRedirectURIFactory(Interface):
    """
    A factory for client redirect URIs.

    This typically is just a fancy storage mechanism.
    """
    def getRedirectURI(clientIdentifier):
        """
        Gets the redirect URI for a particular client.

        @return: A C{Deferred} that will fire with the redirect URI (C{str})
        or C{None}, if no URI has been registered.
        """



class IClientIdentifier(ICredentials):
    """
    A client identifier.
    """
    identifier = Attribute(
        """
        The client identifier for a particular client.

        @type: C{str}
        """)


    redirectURI = Attribute(
        """
        The redirect URI presented in a request.

        If no redirect URI was present in the request, C{None}.

        @type: C{str} or C{None}
        """)



class IClientIdentifierSecret(IClientIdentifier):
    """
    A client identifier plus a shared secret.
    """
    secret = Attribute(
        """
        The shared secret of this client.

        @type: C{str}
        """)



class IRequest(Interface):
    """
    An OAuth request.
    """
    clientIdentifier = Attribute(
        """
        The identifier for the client on behalf of which this request is made.

        This object always provides  L{ICredentials}, so it can be used as
        credentials for Twisted Cred.

        @type clientIdentifier: L{IClientIdentifier}
        """)



class IAssertionStore(Interface):
    """
    A place to store and check grant assertions.

    Assertions can be exchanged at a token endpoint for an access token. They
    are predominantly intended for interfacing OAuth with existing auth
    systems.
    """
    def addAssertion(assertion):
        """
        Adds an assertion to this assertion store.

        @param assertion: The assertion to be added to the store.
        @type assertion: L{txoauth.token.IAssertion}
        """

    def checkAssertion(assertion, invalidate=True):
        """
        Checks an assertion in this assertion store.

        @param assertion: The assertion to be checked.
        @type assertion: L{txoauth.token.IAssertion}
        @param invalidate: If true, the assertion will be invalidated after
        checking. Note that the specification believes this should always be
        the case. Implementations may refuse to accept requests to keep the
        assertion valid.
        @type invalidate: C{bool}
        """
