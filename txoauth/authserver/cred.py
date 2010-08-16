"""
Twisted Cred stuff for authorization servers.
"""
from txoauth.authserver.interfaces import IClient, ICallbackURLFactory

from twisted.cred.portal import IRealm
from twisted.internet import defer

from zope.interface import implements


_UNSET = object()


class Client(object):
    """
    An OAuth client.
    """
    implements(IClient)

    def __init__(self, identifier, callbackURLFactory):
        self._identifier = identifier
        self._urlFactory = callbackURLFactory
        self._url = _UNSET


    def getCallbackURL(self):
        if self._url is _UNSET:
            d = self._urlFactory.get(self._identifier)

            @d.addCallback
            def memoize(url):
                self._url = url
                return url # Caller expects deferred to fire with URL

            return d
        else:
            return defer.succeed(self._url)



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



class ClientRealm(object):
    """
    A realm that produces clients.
    """
    implements(IRealm)
    def __init__(self, callbackURLFactory):
        """
        Initializes a client realm.

        TODO: finish docstring
        """
        self._urlFactory = callbackURLFactory


    def requestAvatar(self, clientIdentifier, mind=None, *interfaces):
        """
        Produces an avatar.

        TODO: finish docstring
        """
        if IClient in interfaces:
            c = Client(clientIdentifier, self._urlFactory)
            return defer.succeed(c)
        else:
            raise NotImplementedError("ClientRealm only produces IClients")
