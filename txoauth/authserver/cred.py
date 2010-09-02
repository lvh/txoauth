"""
Twisted Cred stuff for authorization servers.
"""
from txoauth.authserver.interfaces import (IClient, IClientIdentifier,
                                           IClientIdentifierSecret)

from twisted.cred.portal import IRealm
from twisted.internet import defer
from twisted.python.components import registerAdapter
from twisted.web.iweb import IRequest

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
            return defer.succeed((IClient, c, lambda: None))
        else:
            raise NotImplementedError("ClientRealm only produces IClients")



class ClientIdentifier(object):
    implements(IClientIdentifier)

    def __init__(self, identifier):
        self._identifier = identifier


    @property
    def identifier(self):
        return self._identifier



class ClientIdentifierSecret(ClientIdentifier):
    implements(IClientIdentifierSecret)

    def __init__(self, identifier, secret):
        super(ClientIdentifierSecret, self).__init__(identifier)
        self._secret = secret


    @property
    def secret(self):
        return self._secret


def _extractClientCredentials(request):
    """
    Extracts client credentials from a request.

    This will try to extract L{IClientIdentifierSecret}. If the secret is not
    present in the request, it will extract L{IClientIdentifier}. If neither
    the identifier nor the secret is present, it will raise C{TypeError}.
    """
    identifier = request.getUser() or request.args.get("client_id")
    if not identifier:
        raise TypeError("request doesn't contain client identifier")

    secret = request.getPassword() or request.args.get("client_secret")
    if not secret:
        return ClientIdentifier(identifier)
    return ClientIdentifierSecret(identifier, secret)


registerAdapter(_extractClientCredentials,
                IRequest,
                IClientIdentifier)


def _adaptToIClientIdentifierSecret(request):
    adapted = _extractClientCredentials(request)
    if not IClientIdentifierSecret.providedBy(adapted):
        raise TypeError("request doesn't contain client secret")
    return adapted


registerAdapter(_adaptToIClientIdentifierSecret,
                IRequest,
                IClientIdentifierSecret)
