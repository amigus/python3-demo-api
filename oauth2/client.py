from urllib.parse import urlencode

import json
import requests


class OAuth2ClientError(Exception):
    """ The authorization server did not grant access """

    def __init__(self, response=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = response


class OAuth2Client(object):
    @staticmethod
    def get_authorize_url(params, authorize_url):
        return f"{authorize_url}?{urlencode(params)}"

    @staticmethod
    def post_grant_request(token_url, grant_request):
        response = requests.post(token_url, data=grant_request)

        if response.status_code != 200:
            raise OAuth2ClientError(response)
        return response.content

    def _update_tokens(self, grant):
        self.access_token = grant["access_token"]
        self.refresh_token = grant["refresh_token"]
        if self.refresh_grant_callback is not None:
            self.refresh_grant_callback(grant)

    def __init__(
        self,
        client_id,
        client_secret,
        redirect_uri,
        token_url,
        refresh_token=None,
        access_token=None,
        refresh_grant_callback=None,
    ):
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token_url = token_url
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.refresh_grant_callback = refresh_grant_callback

    def get_client_info(self, scope):
        return {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": scope,
        }

    def get_auth_code_grant_request(self, auth_code, scopes):
        return dict(
            self.get_client_info(scopes),
            **{
                "client_secret": self.client_secret,
                "code": auth_code,
                "grant_type": "authorization_code",
            },
        )

    def get_refresh_grant_request(self, refresh_token):
        return {"grant_type": "refresh_token", "refresh_token": refresh_token}

    def post_authorize_request(self, auth_code, scopes):
        grant = self.post_grant_request(
            self.token_url, self.get_auth_code_grant_request(auth_code, scopes)
        )

        self._update_tokens(json.loads(grant))
        return grant

    def authorize(self, auth_code, scopes):
        return json.loads(self.post_authorize_request(auth_code, scopes))

    def post_refresh_grant_request(self, refresh_token):
        grant = self.post_grant_request(
            self.token_url, self.get_refresh_grant_request(refresh_token)
        )

        self._update_tokens(json.loads(grant))
        return grant

    def refresh(self):
        return self.post_refresh_grant_request(self.refresh_token)
