"""
Simple implementations of some txOAuth interfaces.
"""
from txoauth.authserver.interfaces import IRedirectURIFactory

from twisted.internet import defer

from zope.interface import implements


class SimpleRedirectURIFactory(object):
    """
    A simplistic, in-memory redirect URI factory.

    This is a wrapper around a dictionary.
    """
    implements(IRedirectURIFactory)

    def __init__(self, **redirectionURIs):
        """
        Initializes this URI factory.

        TODO: finish docstring
        """
        self._uris = redirectionURIs


    def getRedirectURI(self, clientIdentifier):
        uri = self._uris.get(clientIdentifier)
        return defer.succeed(uri)
