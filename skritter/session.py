from base64 import b64encode
from .exceptions import ConnectionError

import json
import logging
import requests

OAUTH_TOKEN_URL = 'https://www.skritter.com/api/v0/oauth2/token'
logger = logging.getLogger(__name__)


class Session(object):
    def __init__(self,
                 OAUTH_CLIENT_NAME=None, OAUTH_CLIENT_SECRET=None,
                 session=None):

        # Requests session used for networks requests
        if session is None:
            self.session = requests.session()
        else:
            self.session = session

        # OAuth client name for this API client
        self.oauth_client_name = OAUTH_CLIENT_NAME

        # OAuth client secret for this API client
        self.oauth_client_secret = OAUTH_CLIENT_SECRET

    def login(self, user, password):
        """Connect to Skritter OAuth2 endpoint, and login the current user"""

        if not self.has_oauth_details():
            raise ConnectionError('OAuth client details not supplied')

        params = {
            'grant_type':  'password',
            'client_id':   self.oauth_client_name,
            'username':    user,
            'password':    password
            }

        credentials = "%s:%s" % (self.oauth_client_name,
                                 self.oauth_client_secret)
        credentials = b64encode(credentials)
        credentials = "basic %s" % credentials

        headers = {
            'AUTHORIZATION': credentials
            }

        r = self.session.get(OAUTH_TOKEN_URL, params=params, headers=headers)
        login_response = r.json()

        self.set_authorization_header(login_response.get('access_token', None))

    def get(self, url, **kwargs):
        response = self.session.get(url, **kwargs)

        if response.status_code >= 200 and response.status_code < 300:
            return response.json()

        logger.warning('Unable to get: %s, status: %d', url, response.status_code)
        return None

    def post(self, url, data=None, **kwargs):
        return self.session.post(url, data, **kwargs)

    def post_json(self, url, data=None, **kwargs):
        if data is not None:
            data = json.dumps(data)

        response = self.post(url, data, **kwargs)
        return response.json()

    def put(self, url, data=None, **kwargs):
        return self.session.put(url, data, **kwargs)

    def put_json(self, url, data=None, **kwargs):
        if data is not None:
            data = json.dumps(data)

        response = self.put(url, data, **kwargs)
        return response.json()

    def set_authorization_header(self, access_token=None):
        """Update the access token for the current session."""
        headers = {}
        if access_token is not None:
            headers['Authorization'] = 'Bearer %s' % access_token
        else:
            headers['Authorization'] = None

        self.session.headers.update(headers)

    def has_oauth_details(self):
        return (self.oauth_client_name is not None and
                self.oauth_client_secret is not None)


def session(oauth_client_name, oauth_client_secret):
    """Returns a :class:`Session` for api calls."""
    return Session(oauth_client_name, oauth_client_secret)
