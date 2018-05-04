from rest_framework import viewsets, permissions, response, status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

CLIENT_ID = '78b9d80b-aab3-4615-8a23-5864573f967a'
CLIENT_SECRET = 'wdhfBEXO*@thfIXA01539;}'
URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
SCOPE = ['openid offline_access https://graph.microsoft.com/Notes.ReadWrite.All']


class OneNoteTokenView(APIView):
    """
    View to obtain OneNote token with code
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        """
        Obtains access token, requires code
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'code': request.data['code'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scope': SCOPE,
            'grant_type': 'authorization_code'
        }
        r = requests.get(URL, data=data, headers=headers)
        return Response(data=r.json(), status=status.HTTP_200_OK)


class OneNoteTokenRefreshView(APIView):
    """
    View to obtain OneNote token with refresh token
    """
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, format=None):
        """
        Obtains access token, requires refresh token
        """
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scope': SCOPE,
            'grant_type': 'refresh_token'
        }
        r = requests.get(URL, data=data, headers=headers)
        return Response(data=r.json(), status=status.HTTP_200_OK)

