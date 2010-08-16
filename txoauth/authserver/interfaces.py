"""
Interfaces for authorization servers.
"""
from zope.interface import Interface


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

        @return: A C{Deferred} that will fire with the callback URL (C{str}).
        """
