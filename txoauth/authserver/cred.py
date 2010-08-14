"""
Twisted Cred stuff for authorization servers.
"""
from txoauth.authserver.interfaces import IClient, ICallbackURLFactory

from twisted.cred.portal import IRealm
from twisted.internet import defer

from zope.interface import implements


class Client(object):
    """
    An OAuth client.
    """
    implements(IClient)

    def __init__(self, callbackURL):
        if callbackURL is None:
            self._url = None
        else:
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
            d = self._urlFactory.get(clientIdentifier)
            def makeClient(url):
                return Client(url)
            d.addCallback(makeClient)
            return d
        else:
            raise NotImplementedError("ClientRealm only produces IClients")
