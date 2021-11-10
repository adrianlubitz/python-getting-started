#!/usr/bin/python

__author__ = 'Adrian Lubitz'

"""
Generates my users
"""
import os, sys
import django
django.setup()

from django.contrib.auth.models import User


USERS = {'Adrian':'init_pw', 'Valeska':'init_pw', 'Sina':'init_pw', 'Marius':'init_pw'}


if __name__ == "__main__":
    # sys.path.append('/workspace/wichteln/gettingstarted/')
    os.environ["DJANGO_SETTINGS_MODULE"] = "gettingstarted.settings"
    for user, pw in USERS.items():
        new_user = User.objects.create_user(user, password=pw)
        new_user.save()
        print(f'created {user}')