# coding = utf-8

import logging

from flask import current_app

from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import Flow
# from google.oauth2 import service_account
from google.oauth2.credentials import Credentials

from app import auth, components
from app.user.oauth.model import UserAuthenticators


class GoogleAuthenticator(components.Singleton):
    APP_INTEGRATIONS = "APP_INTEGRATIONS"
    name = "oauth-google"

    def fetch_and_add_profile(self, service, auth_code):
        assert current_app.config[self.APP_INTEGRATIONS]
        assert current_app.config[self.APP_INTEGRATIONS][self.name]
        # a pelyhes lofaszt mindenbe bele
        config = current_app.config[self.APP_INTEGRATIONS][self.name]

        # TODO: Refresh token https://www.npmjs.com/package/vue-google-oauth2
        # https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html#google.oauth2.credentials.Credentials

        # credentials = Credentials(
        #     token,
        #     refresh_token,
        #     id_token,
        #     client_id,
        #     client_secret,
        #     scopes
        # )
        # service = build('userinfo.profile', 'api_version')

    # service = build('admin', 'directory_v1', credentials=credentials)

    pass
    pass


googleAuthenticator = GoogleAuthenticator()


def google_auth_code(service, auth_code):
    return googleAuthenticator.fetch_and_add_profile(service, auth_code)
