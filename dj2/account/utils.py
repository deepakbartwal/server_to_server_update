from django.contrib.auth.models import *
from core.models import *


def RegistrationUtil(data_dict):
    """ Util function for registering student """
    # first_name = data_dict["first_name"]
    # last_name = data_dict["last_name"]
    email = data_dict['user_email']
    username = data_dict['username']
    password = data_dict["password"]
    registered_user = User.objects.create_user(username = username, email = email, password = password)
    p = UserProfile()
    p.user = registered_user
    p.user_nicename = data_dict['user_nicename']
    p.user_url = data_dict['user_url']
    p.display_name = ['display_name']
    p.save()
    return True

def UpdateInfoUtil(data_dict, user):
    """ Utility to update the user information """
    user.first_name = data_dict["first_name"]
    user.last_name = data_dict["last_name"]
    user.email = data_dict['user_email']
    user.username = user.email
    user.save()
    return True
