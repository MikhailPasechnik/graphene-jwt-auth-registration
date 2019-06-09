#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from rest_framework_jwt.serializers import JSONWebTokenSerializer

User = get_user_model()

class Gjwt_authTestCase(TestCase):

    def setUp(self):
        self.rf = RequestFactory()
        self.user = User(email="eins@zwei.de")
        self.user.set_password('123')
        self.user.save()

    def get_jwt_token(self):        
        serializer = JSONWebTokenSerializer(
            data={'email': self.user.email, 'password': '123'})
        serializer.is_valid()
        token = serializer.object['token']
        return "JWT %s" % token