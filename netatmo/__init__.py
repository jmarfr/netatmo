"""Netatmo base class."""
import time

import requests
import logging
from http.client import HTTPConnection

# log = logging.getLogger("urllib3")
# log.setLevel(logging.DEBUG)
#
# HTTPConnection.debuglevel = 1

# TODO: Save token locally to reuse it. save/load methods needed


class Netatmo:

    def __init__(self, client_id, client_secret, username, password, scope=None):
        self._client_id = client_id
        self._client_secret = client_secret
        self._username = username
        self._password = password
        self.scope = scope
        self.token_expiration_time = None
        self._access_token = None
        self._refresh_token = None
        self.base_url = "https://api.netatmo.com"
        self._get_token()

    def _get_token(self):
        """Get oauth token from Netatmo API."""

        if self._access_token and self.token_expiration_time > time.time():
            return self._access_token

        if self.token_expiration_time is not None and \
                self.token_expiration_time < time.time():

            # Need to renew token
            data = {
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
                "client_id": self._client_id,
                "client_secret": self._client_secret
            }
        else:
            data = {
                "grant_type": "password",
                "client_id": self._client_id,
                "client_secret": self._client_secret,
                "username": self._username,
                "password": self._password
            }

        if self.scope is not None:
            data["scope"] = self.scope

        r = requests.post(f"{self.base_url}/oauth2/token", data=data)
        r.raise_for_status()
        json_resp = r.json()

        self._access_token = json_resp['access_token']
        self._refresh_token = json_resp['refresh_token']
        self.token_expiration_time = json_resp['expire_in'] + time.time()

        return self._access_token

    # TODO add GET/POST method here
