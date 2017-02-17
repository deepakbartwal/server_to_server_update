# from rest_framework import viewsets
from rest_framework import status
# from rest_framework.authtoken.models import Token
# from api.models import *
# from api.serializers import *
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication
from pprint import pprint
import json
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from django.contrib.auth.models import User
from core.models import *

@api_view(['POST', 'GET'])
@permission_classes((permissions.AllowAny,))
def RegisterFromServer(request):
    """
    view to register user in current as well as other server
    """
    if request.method == 'POST':
        username = request.data['username']
        user_email = request.data['user_email']
        if not(User.objects.filter(username=username).exists() or User.objects.filter(email=user_email).exists()):
            password = request.data['password']
            confirm_password = request.data['confirm_password']
            if password == confirm_password:
                current_user = User.objects.create_user(username = username, email = user_email, password = password)
                p = UserProfile()
                p.user = current_user
                p.user_nicename = request.data['user_nicename']
                p.user_url = request.data['user_url']
                p.display_name = request.data['display_name']
                p.save()
                return Response(data={'status': True}, status=status.HTTP_200_OK)
        return Response(data={'status': False}, status=status.HTTP_200_OK)

class UpdateFromServerView(APIView):
    """
    View update the user profile from other server
    """
    authentication_classes = (TokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        #work here later ... its okey for now
        user = request.user
        p = UserProfile.objects.get(user = user)

        user_email = request.data['user_email']
        user.email = user_email
        pprint(user.save())

        p.user_nicename = request.data['user_nicename']
        p.display_name = request.data['user_nicename']
        p.user_url = request.data['user_url']
        p.save()
        return Response(data={'status': True}, status=status.HTTP_200_OK)

class ChangePasswordFromServerView(APIView):
    """
    View to change the user password from other server
    """
    authentication_classes = (TokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = User.objects.get(username=request.user.username)
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        confirm_new_password = request.data['confirm_new_password']
        if new_password == old_password:
            return Response(data={'status': False}, status=status.HTTP_200_OK)#error
        else:
            DatabasePassword = request.user.password
            from django.contrib.auth.hashers import check_password
            chk = check_password(password=old_password, encoded = DatabasePassword)
            if chk == True:
                    user.set_password(new_password)
                    user.save()
                    return Response(data={'status': True}, status=status.HTTP_200_OK)
        return Response(data={'status': False}, status=status.HTTP_200_OK)

class ChangeUsernameFromServerView(APIView):
    """
    View to change the username from other server
    """
    authentication_classes = (TokenAuthentication,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = User.objects.get(username=request.user.username)
        new_username = request.data['new_username']
        if new_username == user.username:
            return Response(data={'status': False}, status=status.HTTP_200_OK)#error
        else:
            user.username = new_username
            user.save()
            return Response(data={'status': True}, status=status.HTTP_200_OK)
        return Response(data={'status': False}, status=status.HTTP_200_OK)
