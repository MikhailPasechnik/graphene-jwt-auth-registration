from .testcases import Gjwt_authTestCase

class TestGjwt_auth_middleware(Gjwt_authTestCase):

    def test_unauthenticated_user(self):
        query = "/graphql?query={viewer{user{id, email}}}"
        response = self.client.post(query)
        assert response.status_code == 200
        result = response.json()
        assert result['data']['viewer'] is None

    def test_authenticated_user(self):
        query = "/graphql?query={viewer{user{id, email}}}"
        response = self.client.post(query, HTTP_AUTHORIZATION=self.get_jwt_token())
        assert response.status_code == 200
        result = response.json()
        assert result['data']['viewer']['user']['email'] == self.user.email
