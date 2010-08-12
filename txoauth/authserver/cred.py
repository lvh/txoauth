"""
Twisted Cred stuff for authorization servers.
"""
from txoauth.authserver.interfaces import IClient

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