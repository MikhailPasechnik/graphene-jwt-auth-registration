from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from djoser.email import ActivationEmail, PasswordResetEmail

from djoser import utils

from .graphql_schema import schema

from .testcases import Gjwt_authTestCase


User = get_user_model()



class TestGjwt_auth_mutations(Gjwt_authTestCase):

    # ########
    # REGISTER
    # ########
    def test_register_mutation_success(self):
        request = self.rf.request()
        query = """
        mutation {
          register(
                email: "laffe@giraffe.de",
                password: "123",
                passwordRepeat: "123"
            )
          {
            success
            errors
          }
        }
        """

        expectation = {
                'register': {
                    'success': True,
                    'errors': None
                    }
                }
        result = schema.execute(query, context_value=request)
        result = schema.execute(query, context_value=request)
        assert not result.errors
        assert result.data == expectation

    def test_register_mutation_password_error(self):
        request = self.rf.request()
        query = """
        mutation {
          register(
            email: "affe@giraffe.de",
            password: "123",
            passwordRepeat: "1234"
          ) {
            success
            errors
          }
        }
        """

        expectation = {
                'register': {
                    'success': False,
                    'errors': ['password', "Passwords don't match."]
                    }
                }
        result = schema.execute(query, context_value=request)
        assert not result.errors
        assert result.data == expectation

    def test_register_mutation_user_error(self):
        request = self.rf.request()
        query = """
        mutation {
          register(
            email: "affe@giraffe.de",
            password: "123",
            passwordRepeat: "123"
          ) {
            success
            errors
          }
        }
        """

        expectation = {
                'register': {
                    'success': False,
                    'errors': ['email', 'Email already registered.']
                    }
                }
        schema.execute(query)
        second_result = schema.execute(query, context_value=request)
        assert not second_result.errors
        assert second_result.data == expectation


    # ########
    # ACTIVATE
    # ########
    def test_activation_success(self):
        request = self.rf.request()
        self.user.is_active = False
        self.user.save()
        email_factory = ActivationEmail(
            request, {'user': self.user})
        context = email_factory.get_context_data()
        token = context.get('token')
        uid = context.get('uid')

        query = """
        mutation {
            activate(
                token: "%s",
                uid: "%s",
            ) {
                success
                errors
            }
        }
        """ % (token, uid)

        expectation = {
                'activate': {
                    'success': True,
                    'errors': None
                    }
                }

        result = schema.execute(query, context_value=request)
        assert not result.errors
        assert result.data == expectation

        self.user.refresh_from_db()
        assert self.user.is_active is True

        # TODO: test error case


    # ##############
    # PASSWORD RESET
    # #############
    def test_reset_password_success(self):
        """
        successfully request a password reset
        """
        query = """
        mutation {
            resetPassword(
                email: "eins@zwei.de"
            ) {
                success
            }
        }
        """
        query = "/graphql?query=%s" % query
        response = self.client.post(query)
        result = response.json()
        assert type(result['data']['resetPassword']['success'])

    # ######################
    # PASSWORD RESET CONFIRM
    # #####################
    def test_reset_password_confirm_success(self):
        """
        successfully confirm a password reset
        """

        uid = utils.encode_uid(self.user.pk)
        token = default_token_generator.make_token(self.user)

        query = """
        mutation {
            resetPasswordConfirm(
                email: "eins@zwei.de"
                uid: "%s"
                token: "%s"
                newPassword: "666"
                reNewPassword: "666"
            ) {
                success
            }
        }
        """ % (uid, token)
        query = "/graphql?query=%s" % query
        response = self.client.post(query)
        result = response.json()
        assert type(result['data']['resetPasswordConfirm']['success'])

    def test_reset_password_confirm_password_error(self):
        """
        confirm password reset error password missmatch
        """

        uid = utils.encode_uid(self.user.pk)
        token = default_token_generator.make_token(self.user)

        query = """
        mutation {
            resetPasswordConfirm(
                email: "eins@zwei.de"
                uid: "%s"
                token: "%s"
                newPassword: "666"
                reNewPassword: "6667"
            ) {
                success
            }
        }
        """ % (uid, token)
        query = "/graphql?query=%s" % query
        response = self.client.post(query)
        result = response.json()
        assert not result['data']['resetPasswordConfirm']['success']

    def test_reset_password_confirm_token_error(self):
        """
        confirm password reset token error
        """

        uid = utils.encode_uid(self.user.pk)
        token = "Angela Merkel"

        query = """
        mutation {
            resetPasswordConfirm(
                email: "eins@zwei.de"
                uid: "%s"
                token: "%s"
                newPassword: "666"
                reNewPassword: "666"
            ) {
                success
            }
        }
        """ % (uid, token)
        query = "/graphql?query=%s" % query
        response = self.client.post(query)
        result = response.json()
        assert not result['data']['resetPasswordConfirm']['success']

    def test_reset_password_confirm_uid_error(self):
        """
        confirm password reset uid error
        """

        uid = "Angela Merkel"
        token = default_token_generator.make_token(self.user)

        query = """
        mutation {
            resetPasswordConfirm(
                email: "eins@zwei.de"
                uid: "%s"
                token: "%s"
                newPassword: "666"
                reNewPassword: "666"
            ) {
                success
            }
        }
        """ % (uid, token)
        query = "/graphql?query=%s" % query
        response = self.client.post(query)
        result = response.json()
        assert not result['data']['resetPasswordConfirm']['success']

    # ################
    # PROFILE UPDATE
    # ################

    # ################
    # DELETE ACCOUNT
    # ###############
    def test_delete_account_unauthenticated_error(self):
        """
        error because unauthenticated
        """
        query = """
        mutation {
            deleteAccount(
                email: "eins@zwei.de",
                password: "123"
            ) {
                success
                errors
            }
        }
        """
        query = "/graphql?query=%s" % query
        response = self.client.post(query)
        result = response.json()
        assert response.status_code == 200
        assert not result['data']['deleteAccount']['success']

    def test_delete_account_authenticated_user_error(self):
        """
        error because authenticated as wrong user
        """
        query = """
        mutation {
            deleteAccount(
                email: "wrong@user.de",
                password: "123"
            ) {
                success
                errors
            }
        }
        """
        query = "/graphql?query=%s" % query
        response = self.client.post(query, HTTP_AUTHORIZATION=self.get_jwt_token())
        result = response.json()
        assert response.status_code == 200
        assert not result['data']['deleteAccount']['success']

    def test_delete_account_authenticated_password_error(self):
        """
        error because authenticated user provides wrong password
        """
        query = """
        mutation {
            deleteAccount(
                email: "eins@zwei.de",
                password: "wrong_password"
            ) {
                success
                errors
            }
        }
        """
        query = "/graphql?query=%s" % query
        response = self.client.post(query, HTTP_AUTHORIZATION=self.get_jwt_token())
        result = response.json()
        assert response.status_code == 200
        assert not result['data']['deleteAccount']['success']
        assert result['data']['deleteAccount']['errors'] == ['wrong password']

    def test_delete_account_authenticated_success(self):
        """
        authenticated user can successfully delete their account
        """
        query = """
        mutation {
            deleteAccount(
                email: "eins@zwei.de",
                password: "123"
            ) {
                success
                errors
            }
        }
        """
        query = "/graphql?query=%s" % query
        response = self.client.post(query, HTTP_AUTHORIZATION=self.get_jwt_token())
        result = response.json()
        assert response.status_code == 200
        assert result['data']['deleteAccount']['success']
        assert not User.objects.filter(email=self.user.email).count()
