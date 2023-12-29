from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
import logging
logger = logging.getLogger(__name__)

class CheckAuthenticatedUser(BasePermission):
    def has_permission(self, request, view):
        try:
            access_token = request.headers.get(
                'Authorization', '').split('Bearer ')[-1].strip()
            
            logger.debug(f'acc: , {access_token}')
            print('access', access_token)

            if access_token:
                try:
                    print('access', type(access_token))
                    # RefreshToken(access_token)
                    return True

                except Exception as e:
                    print(e)
                    # Access token is invalid or expired, try refreshing
                    refresh_token = request.data.get('refresh', None)
                    if refresh_token:
                        try:
                            refresh = RefreshToken(refresh_token)
                            # print('fefe', str(refresh.access_token))
                            new_access_token = str(refresh.access_token)

                            # Set the new access token in the request header
                            request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
                            # print('access', request.META['HTTP_AUTHORIZATION'])

                            # Set the refresh token in the request data
                            request.data['refresh'] = refresh_token
                            print('req', request.data['refresh'])

                            return True

                        except Exception as e:
                            # Handle TokenError if refreshing fails
                            # print(e)
                            return False
        except Exception as e:
            print(e)
            return False
