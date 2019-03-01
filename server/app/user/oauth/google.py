# coding = utf-8

import logging

from flask import current_app

import google.oauth2.credentials
import google_auth_oauthlib.flow

from app import auth, components
from app.user.oauth.model import UserAuthenticators


class GoogleAuthenticator(components.Singleton):
    def fetch_and_add_profile(service, auth_code):
        # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('client_secret.json',scope=['https://www.googleapis.com/auth/drive.metadata.readonly'])

        #  FK https://developers.google.com/api-client-library/python/start/get_started

        pass
    pass


googleAuthenticator = GoogleAuthenticator()


def google_auth_code(service, auth_code):
    return googleAuthenticator.fetch_and_add_profile(service, auth_code)
