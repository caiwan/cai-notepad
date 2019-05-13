# coding = utf-8

import logging
import json

from flask import current_app

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from app import components
from app.user.oauth.model import UserAuthenticator


# Some Google api doc stuff
# TODO: Refresh token https://www.npmjs.com/package/vue-google-oauth2
# https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html#google.oauth2.credentials.Credentials


class GoogleAuthenticator(metaclass=components.Singleton):
    APP_INTEGRATIONS = "APP_INTEGRATIONS"
    name = "oauth-google"
    idp_id = "google"

    def fetch_and_add_profile(self, service, token_obj):
        config = self._config()

        current_user = components.current_user()
        credentials = Credentials(
            token_obj["access_token"],
            refresh_token=token_obj["access_token"],
            id_token=token_obj["id_token"],
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            scopes=[
                "email",
                "profile",
                "https://www.googleapis.com/auth/userinfo.email",
                "openid",
                "https://www.googleapis.com/auth/userinfo.profile"
            ]
        )

        user_info = build(
            "oauth2", "v2", credentials=credentials).userinfo().get().execute()
        user_info_string = json.dumps(user_info)

        # Check if had been added before
        authenticator = None
        try:
            current_user_id = components.current_user_id()

            # Only one instance is supported ATM
            authenticator = UserAuthenticator.select(UserAuthenticator).join(components.BaseUser).where(
                UserAuthenticator.owner.id == current_user_id,
                UserAuthenticator.idp_id == GoogleAuthenticator.idp_id
            ).get()

            # If exists, then renew
            authenticator.access_token = token_obj["access_token"]
            authenticator.expires_at = token_obj["expires_at"]
            authenticator.profile = user_info_string
            authenticator.save()

        except UserAuthenticator.DoesNotExist:
            # If not exists, insert
            try:
                authenticator = UserAuthenticator(
                    owner=current_user,
                    idp_id="google",
                    access_token=token_obj["access_token"],
                    id_token=token_obj["id_token"],
                    expires_at=token_obj["expires_at"],
                    profile=user_info_string,
                )
                authenticator.save()
                return True

            except:
                logging.exception("Could not get user info")
                return False
        except:
            logging.exception("Could not get user info")
            return False

    # --------------------------------------
    def renew_token(self, user_id):
        # TODO
        pass

    def get_user_token(self, user_id):
        try:
            return UserAuthenticator.select(UserAuthenticator).join(components.BaseUser).where(
                UserAuthenticator.is_deleted == False,
                UserAuthenticator.owner.id == user_id,
                UserAuthenticator.idp_id == GoogleAuthenticator.idp_id
            ).get()
        except UserAuthenticator.DoesNotExist:
            return None
        pass

    def get_user_credentials(self, user_id, scopes):
        authenticator = self.get_user_token(user_id)
        if not authenticator:
            return None
        config = self._config()

        # TODO: RENEW

        return Credentials(
            authenticator.access_token,
            refresh_token=authenticator.access_token,
            id_token=authenticator.id_token,
            client_id=config["client_id"],
            client_secret=config["client_secret"],
            scopes=scopes
        )

    # --------------------------------------
    def _config(self):
        assert current_app.config[GoogleAuthenticator.APP_INTEGRATIONS]
        assert current_app.config[GoogleAuthenticator.APP_INTEGRATIONS][GoogleAuthenticator.name]
        return current_app.config[GoogleAuthenticator.APP_INTEGRATIONS][GoogleAuthenticator.name]


googleAuthenticator = GoogleAuthenticator()


def google_auth_code(service, auth_code):
    return googleAuthenticator.fetch_and_add_profile(service, auth_code)
