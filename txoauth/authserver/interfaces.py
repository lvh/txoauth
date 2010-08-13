"""
Interfaces for authorization servers.
"""
from zope.interface import Attribute, Interface


class IClient(Interface):
    """
    A representation of an OAuth client.
    """
    callbackURL = Attribute(
        """
        The registered callback URL for this client.
        """)



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