#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_graphene-jwt-auth
------------

Tests for `graphene-jwt-auth` models module.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class TestGjwt_auth(TestCase):

    def setUp(self):
	    self.user = User(email="eins@zwei.de")
	    user.set_password('123')
	    user.save()

    def test_token_valid(self):        
	    serializer = JSONWebTokenSerializer(
	        data={'email': user.email, 'password': '123'})
	    serializer.is_valid()
	    token = serializer.object['token']
	    return "JWT %s" % token

    def tearDown(self):
	    self.user.delete()
