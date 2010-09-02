"""
Simple implementations of some txOAuth interfaces.
"""
from txoauth.authserver.interfaces import ICallbackURLFactory

from twisted.internet import defer

from zope.interface import implements


class SimpleCallbackURLFactory(object):
    """
    A simplistic, in-memory callback URL factory.

    This is a wrapper around a dictionary.
    """
    implements(ICallbackURLFactory)

    def __init__(self, **callbackURLs):
        """
        Initializes a SimpleCallbackURLFactory.

        TODO: finish docstring
        """
        self._urls = callbackURLs


    def get(self, clientIdentifier):
        url = self._urls.get(clientIdentifier)
        return defer.succeed(url)
