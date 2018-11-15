#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A package.

umuus-google-oauth
==================

Installation
------------

    $ pip install umuus_google_oauth

Usage
-----

    $ python -m umuus_google_oauth run \
        --credential_file 'client_secret_XXXX.apps.googleusercontent.com.json' \
        --token_file google_access_token.json


Example
-------

    $ umuus_google_oauth

    >>> import umuus_google_oauth

Authors
-------

- Jun Makii <junmakii@gmail.com>

License
-------

GPLv3 <https://www.gnu.org/licenses/>

"""
import os
import sys
import re
import addict
import logging
import addict
import json
import datetime
import oauthlib.oauth2
import apiclient.discovery
import apiclient.http
import oauth2client.client
import httplib2
import urllib.parse
import requests_oauthlib
import google.oauth2.credentials
import fire
__version__ = '0.1'
__url__ = 'https://github.com/junmakii/umuus-google-oauth'
__author__ = 'Jun Makii'
__author_email__ = 'junmakii@gmail.com'
__keywords__ = []
__license__ = 'GPLv3'
__scripts__ = []
__install_requires__ = [
    'addict',
    'fire',
    'oauth2client',
    'google-auth',
    'google-api-python-client',
    'httplib2',
    'oauthlib',
    'requests_oauthlib',
]
__dependency_links__ = [
]
__classifiers__ = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
]
__entry_points__ = {'console_scripts': ['umuus_google_oauth = umuus_google_oauth:main']}

logger = logging.getLogger(__name__)


class OAuth(object):
    serviceName = 'youtube'
    version = 'v3'
    token_file = 'access_token.json'
    credential_file = 'client_secret.xxxxxxxx.apps.googleusercontent.com.json'
    scope = [
        'https://www.googleapis.com/auth/cloud-translation',
        'https://www.googleapis.com/auth/youtube.readonly',
        'https://www.googleapis.com/auth/youtube',
        'https://www.googleapis.com/auth/youtube.force-ssl',
        'https://www.googleapis.com/auth/youtubepartner',
        'https://www.googleapis.com/auth/yt-analytics.readonly',
        'https://www.googleapis.com/auth/yt-analytics-monetary.readonly',
    ]
    token_uri = 'https://accounts.google.com/o/oauth2/token'
    auto_refresh_url = 'https://accounts.google.com/o/oauth2/token'

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def from_file(self):
    self.credential_file_data = addict.Dict(json.load(open(self.credential_file)))
    return self


def get_session(self):
    self.oauth2_session = requests_oauthlib.OAuth2Session(
        client_id=self.credential_file_data.web.client_id,
        scope=self.scope,
        redirect_uri=self.credential_file_data.web.redirect_uris[0],
        auto_refresh_url=self.auto_refresh_url,
        auto_refresh_kwargs=dict(
            client_id=self.credential_file_data.web.client_id,
            client_secret=self.credential_file_data.web.client_secret,
        ))
    return self


def auth(self):
    if not os.path.exists(self.token_file):
        print(self.credential_file_data)
        print(self.oauth2_session.authorization_url(
            access_type="offline",
            url=self.credential_file_data.web.auth_uri,
            # prompt="select_account",
            approval_prompt="force",
        )[0])
        self.code = input('code: ')
        self.response = self.oauth2_session.fetch_token(
            self.credential_file_data.web.token_uri,
            client_secret=self.credential_file_data.web.client_secret,
            code=self.code,
            verify=False,
            token_updater=(lambda *args: print('token_updater', args)),
        )
        open(self.token_file, 'w').write(json.dumps(self.response))
    else:
        self.token_file_data = addict.Dict(json.load(open(self.token_file)))
        if datetime.datetime.fromtimestamp(self.token_file_data.expires_at) < datetime.datetime.utcnow():
            self.response = self.oauth2_session.refresh_token(self.token_uri, self.token_file_data.refresh_token)
            open(self.token_file, 'w').write(json.dumps(self.response))
        else:
            self.response = addict.Dict(self.token_file_data)
    return self


def get_credentials(self):  # type: umuus_google_auth.Auth
    self.credentials = google.oauth2.credentials.Credentials(
        self.response.access_token,
        refresh_token=self.response.refresh_token,
        token_uri=self.token_uri,
        client_id=self.credential_file_data.web.client_id,
        client_secret=self.credential_file_data.web.client_secret)
    return self


def get_service(self):
    self.service = apiclient.discovery.build(
        self.serviceName,
        self.version,
        credentials=self.auth.credentials,
    )
    return self


def run_command(*args, **kwargs):
    data = OAuth(**kwargs)
    data = from_file(data)
    data = get_session(data)
    data = auth(data)


def main(argv=[]):  # type: int
    fire.Fire({
        key[:-len('_command')]: value
        for key, value in globals().items()
        if key.endswith('_command')})
    return 0


if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    sys.exit(main(sys.argv))
