from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from datetime import timedelta

class SessionAuthentication(BaseAuthentication):
    authentication_classes = [] 
    def authenticate(self, request):
        # Retrieve the token from the session
        token = request.session.get('access_token')
        if not token:
            raise AuthenticationFailed('No access token found in session.')

        try:
            # Validate and decode the token
            access_token = AccessToken(token)

            # Fetch the user based on the token's user_id
            user_model = get_user_model()  # Use the custom user model
            user = user_model.objects.get(id=access_token['user_id'])

        except Exception as e:
            raise AuthenticationFailed(f'Token is invalid: {str(e)}')

        # Return the user and the token (if authentication is successful)
        return (user, access_token)
