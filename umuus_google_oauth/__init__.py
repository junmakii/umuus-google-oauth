#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018  Jun Makii <junmakii@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
'''Utilities, tools, and scripts for Python.

umuus-google-oauth
==================

Installation
------------

    $ pip install git+https://github.com/junmakii/umuus-google-oauth.git

    $ pip install addict fire oauth2client google-auth google-api-python-client httplib2 oauthlib requests_oauthlib attrs


Command Line
------------

    $ python -m umuus_google_oauth run \
      --credential_file "config/google/client_secret_XXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com.json" \
      --token_file "config/google/google_youtube_access_token.json" \
      --scope "$(cat config/google/google_youtube_scope.json)"

Code
----

    import umuus_google_oauth

    umuus_google_oauth.run(
        credential_file="config/google/client_secret_XXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com.json",
        token_file="config/google/google_youtube_access_token.json",
        scope="$(cat config/google/google_youtube_scope.json)",
    )

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

'''
# -- BaseImport --
import os
import sys
import re
import datetime
import json
import types
import typing
import threading
import time
import wsgiref.simple_server
import functools
import itertools
import logging
logger = logging.getLogger(__name__)
import fire
import attr
import addict
import oauthlib.oauth2
import apiclient.discovery
import apiclient.http
import oauth2client.client
import httplib2
import urllib.parse
import requests_oauthlib
import flask
import google.oauth2.credentials
# -- End BaseImport --
# -- Metadata --
__version__ = '0.1'
__url__ = 'https://github.com/junmakii/umuus-google-oauth'
__author__ = 'Jun Makii'
__author_email__ = 'junmakii@gmail.com'
__keywords__ = []
__license__ = 'GPLv3'
__scripts__ = []
__install_requires__ = [
    'attrs',
    'addict',
    'requests',
    'addict',
    'fire',
    'oauth2client',
    'google-auth',
    'google-api-python-client',
    'httplib2',
    'oauthlib',
    'requests_oauthlib',
    'attrs',
    'flask',
    # 'umuus-utils@git+https://github.com/junmakii/umuus-utils.git#egg=umuus_utils-0.1',
]
__dependency_links__ = [
    # 'git+https://github.com/junmakii/umuus-utils.git#egg=umuus_utils-1.0',
]
__classifiers__ = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
]
__entry_points__ = {
    'console_scripts': ['umuus_google_oauth = umuus_google_oauth:main'],
    'gui_scripts': [],
}
__project_urls__ = {
    'Bug Tracker': 'https://github.com/junmakii/umuus-google-oauth/issues',
    'Documentation': 'https://github.com/junmakii/umuus-google-oauth/',
    'Source Code': 'https://github.com/junmakii/umuus-google-oauth/',
}
__setup_requires__ = ['pytest-runner']
__test_suite__ = 'umuus_google_oauth'
__tests_require__ = ['pytest']
__extras_require__ = {}
__package_data__ = {'': []}
__python_requires__ = '>=3.0.0'
__include_package_data__ = True
__zip_safe__ = True
__static_files__ = {}
__extra_options__ = {
    'docker_requires': [
        'ca-certificates',
        'python3',
        'python3-dev',
    ],
    'docker_cmd': [],
}
# -- End Metadata --
# -- Extra --
umuus_google_oauth = __import__(__name__)
# -- End Extra --


@attr.s()
class OAuth(object):
    serviceName = attr.ib('youtube')
    version = attr.ib('v3')
    token_file = attr.ib('access_token.json')
    credential_file = attr.ib(
        'client_secret.xxxxxxxx.apps.googleusercontent.com.json')
    credential_file_data = attr.ib({})
    scope = attr.ib([])
    token_uri = attr.ib('https://accounts.google.com/o/oauth2/token')
    auto_refresh_url = attr.ib('https://accounts.google.com/o/oauth2/token')
    code = None
    response = None
    token_file_data = None
    credentials = None
    service = None
    session = None
    server_app = None
    server_thread = None
    server_response = {}
    server_host = attr.ib('0.0.0.0')
    server_port = attr.ib(8022)
    server_route = '/oauth_redirect_uri'
    httpd = None


def close_server(oauth=None):
    oauth.httpd.shutdown()
    return oauth


def run_server(oauth=None):
    oauth.server_app = flask.Flask(__name__)

    def view():
        response = dict(flask.request.args.items())
        oauth.server_response = response
        return flask.Response(
            json.dumps(response),
            content_type='application/json',
        )

    oauth.server_app.route(oauth.server_route)(view)
    oauth.httpd = wsgiref.simple_server.make_server(
        app=oauth.server_app,
        host=oauth.server_host,
        port=oauth.server_port,
    )
    oauth.server_thread = threading.Thread(
        target=lambda: oauth.httpd.serve_forever(poll_interval=0.5))
    oauth.server_thread.start()
    return oauth


def load(oauth=None):
    oauth.credential_file_data = addict.Dict(
        json.load(open(oauth.credential_file)))
    return oauth


def get_session(oauth=None):
    oauth.session = requests_oauthlib.OAuth2Session(
        client_id=oauth.credential_file_data.web.client_id,
        scope=oauth.scope,
        redirect_uri=oauth.credential_file_data.web.redirect_uris[0],
        auto_refresh_url=oauth.auto_refresh_url,
        auto_refresh_kwargs=dict(
            client_id=oauth.credential_file_data.web.client_id,
            client_secret=oauth.credential_file_data.web.client_secret,
        ))
    return oauth


def auth(oauth=None):
    if not os.path.exists(oauth.token_file):
        print(
            oauth.session.authorization_url(
                access_type="offline",
                url=oauth.credential_file_data.web.auth_uri,
                # prompt="select_account",
                approval_prompt="force",
            )[0])
        while True:
            if oauth.server_response:
                oauth.code = oauth.server_response['code']
                break
            time.sleep(1)
        oauth.response = addict.Dict(
            oauth.session.fetch_token(
                oauth.credential_file_data.web.token_uri,
                client_secret=oauth.credential_file_data.web.client_secret,
                code=oauth.code,
                verify=False,
                token_updater=(lambda *args: print('token_updater', args)),
            ))
        open(oauth.token_file, 'w').write(json.dumps(oauth.response))
    else:
        oauth.token_file_data = addict.Dict(json.load(open(oauth.token_file)))
        if datetime.datetime.fromtimestamp(
                oauth.token_file_data.expires_at) < datetime.datetime.utcnow():
            oauth.response = addict.Dict(
                oauth.session.refresh_token(
                    oauth.token_uri, oauth.token_file_data.refresh_token))
            open(oauth.token_file, 'w').write(json.dumps(oauth.response))
        else:
            oauth.response = addict.Dict(oauth.token_file_data)
    return oauth


def get_credentials(oauth=None):
    oauth.credentials = google.oauth2.credentials.Credentials(
        oauth.response.access_token,
        refresh_token=oauth.response.refresh_token,
        token_uri=oauth.token_uri,
        client_id=oauth.credential_file_data.web.client_id,
        client_secret=oauth.credential_file_data.web.client_secret)
    return oauth


def get_service(oauth=None):
    oauth.service = apiclient.discovery.build(
        oauth.serviceName,
        oauth.version,
        credentials=oauth.credentials,
    )
    return oauth


def run(**kwargs):  # type: None
    oauth = OAuth(**kwargs)
    oauth = load(oauth=oauth)
    oauth = run_server(oauth=oauth)
    oauth = get_session(oauth=oauth)
    oauth = auth(oauth=oauth)
    oauth = get_credentials(oauth=oauth)
    oauth = get_service(oauth=oauth)
    oauth = close_server(oauth=oauth)
    return oauth


def test_main():  # type: None
    pass


def main(argv=None):  # type: int
    fire.Fire()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
