"""
Simple implementations of some txOAuth interfaces.
"""
from txoauth.interfaces import IRedirectURIFactory

from twisted.internet import defer

from zope.interface import implements


class SimpleRedirectURIFactory(object):
    """
    A simplistic, in-memory redirect URI factory.

    This is a wrapper around a dictionary.
    """
    implements(IRedirectURIFactory)

    def __init__(self, **redirectURIs):
        """
        Initializes this URI factory.

        TODO: finish docstring
        """
        self._uris = redirectURIs


    def getRedirectURI(self, clientIdentifier):
        uri = self._uris.get(clientIdentifier)
        return defer.succeed(uri)
