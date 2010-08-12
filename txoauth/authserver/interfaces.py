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