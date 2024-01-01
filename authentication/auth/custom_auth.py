from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
import logging
# from authentication.models import User
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

class CustomAuthentication(JWTAuthentication):


    # def verify_user(self, payload):
    #     """
    #     Custom method to verify the user based on the token payload.
    #     """
    #     try:
    #         return super().verify_user(payload)
    #     except self.token_class.TokenError as e:
    #         logger.exception("Error during user verification")
    #         raise AuthenticationFailed("User verification failed")

    def verify_token(token, self):
        """
        Custom method to verify the token.
        """
        try:
            super().verify_token(token)
            # Your custom token verification logic here
        except self.token_class.TokenError as e:
            # Token is invalid, try refreshing using the refresh token
            refresh_token = self.get_refresh_token_from_request()
            if refresh_token:
                try:
                    refresh = RefreshToken(refresh_token)
                    new_access_token = str(refresh.access_token)

                    # Set the new access token in the request header
                    self.request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'

                    # Set the refresh token in the request data
                    self.request.data['refresh'] = refresh_token

                    # Token has been refreshed, update the user and return
                    self.user = self.verify_user(refresh.payload)
                    return

                except self.token_class.TokenError as e:
                    logger.exception("Error during token refresh")
                    raise AuthenticationFailed("Token refresh failed")

            # If no valid refresh token is present, raise AuthenticationFailed
            logger.exception("Error during token verification")
            raise AuthenticationFailed("Token verification failed")

    def get_refresh_token_from_request(self):
        """
        Custom method to extract the refresh token from the request.
        Modify this method according to how you store or pass the refresh token in your requests.
        """
        return self.request.data.get('refresh')  # Adjust this based on your use case
