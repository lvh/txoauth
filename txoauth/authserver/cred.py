"""
Twisted Cred stuff for authorization servers.
"""
from txoauth.authserver.interfaces import IClient, ICallbackURLFactory

from twisted.internet import defer

from zope.interface import implements


class Client(object):
    """
    An OAuth client.
    """
    implements(IClient)

    def __init__(self, callbackURL):
        self._url = str(callbackURL)


    @property
    def callbackURL(self):
        return self._url



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


