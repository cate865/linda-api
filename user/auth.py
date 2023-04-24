from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from knox.auth import TokenAuthentication

class TokenAuthenticationWithSession(TokenAuthentication):
    def authenticate(self, request):
        user, auth_token = super().authenticate(request)

        if user is not None:
            session = SessionStore(session_key=request.session.session_key)
            session['auth_token'] = auth_token
            session.save()

        return user, auth_token
