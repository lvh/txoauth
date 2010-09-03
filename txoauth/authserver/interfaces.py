"""
Interfaces for authorization servers.
"""
from twisted.cred.credentials import ICredentials

from zope.interface import Interface, Attribute


class IClient(Interface):
    """
    A representation of an OAuth client.
    """

    def getCallbackURL():
        """
        Gets the registered callback URL for this client.

        @rtype: C{Deferred}
        @return: A C{Deferred} which will fire with the URL, or C{None} if no
        URL has been registered.
        """



class ICallbackURLFactory(Interface):
    """
    A factory for client callback URLs.

    This typically is just a fancy storage mechanism.
    """
    def get(clientIdentifier):
        """
        Gets the callback URL for a particular client.

        @return: A C{Deferred} that will fire with the callback URL (C{str})
        or C{None}, if no URL has been registered.
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


    callbackURL = Attribute(
        """
        The callback URL presented in a request.

        If the callback URL was not present in the request, C{None}.

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
