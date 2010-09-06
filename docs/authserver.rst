Authentication servers
======================

End-user authentication endpoint
--------------------------------
Authentication servers are responsible for authenticating users and requesting
their authorization for allowing a third-party client to access resources on
their behalf.

txOAuth provides you with tools for implementing these endpoints, but does not
actually implement them itself. This is mostly because there are too many
different ways to authenticate users (completely outside of OAuth) for txOAuth
to provide a more sensible API.

Authenticating end-users is entirely outside the scope of (tx)OAuth, and
happens through ordinary mechanisms (``nevow.guard`` for example). txOAuth
helps you parse the OAuth-specific parts of the request into a nicer interface
(``txoauth.interfaces.IRequest``) which should make it easier to show the user
what it is exactly he's agreeing to.

That request object also allows you to respond (negatively or positively to
the client). It is responsible for maintaining parts of the specification you
don't care about, such as:

      - maintaining the ``state`` parameter


Token endpoints
---------------
The second part of an authentication server is the token endpoint. Token
endpoints are responsible for turning all sorts of credentials that amount to
an access grant into a token that will actually let you access something.

Unlike the end-user authentication endpoint, a class implementing the token
endpoint is provided.

The token endpoint authenticates a client, and then tries to parse the rest of
the request into a set of credentials.

These credentials are then passed on to a Portal, which has credentials
checkers for all the kinds of credential you want to allow. The TokenRealm
then returns an ``IResource`` that tells the client about its new token.

If that last bit seems a bit arcane to you, you might want to read JP
Calderone's `article`_ on ``twisted.cred`` in combination with
``twisted.web``.

.. _article: http://jcalderone.livejournal.com/53074.html
