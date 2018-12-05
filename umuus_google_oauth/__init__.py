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

config.json::

    {
        "credential_file": "config/google/client_secret_XXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com.json",
        "token_file": "config/google/google_youtube_access_token.json",
        "scope": [
            "https://www.googleapis.com/auth/cloud-translation",
            "https://www.googleapis.com/auth/youtube.readonly",
            "https://www.googleapis.com/auth/youtube",
            "https://www.googleapis.com/auth/youtube.force-ssl",
            "https://www.googleapis.com/auth/youtubepartner",
            "https://www.googleapis.com/auth/yt-analytics.readonly",
            "https://www.googleapis.com/auth/yt-analytics-monetary.readonly"
        ]
    }

----

    $ python -m umuus_google_oauth run --file config.json

----

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
import datetime
import json
import threading
import time
import wsgiref.simple_server
import logging
logger = logging.getLogger(__name__)
import fire
import attr
import addict
import apiclient.discovery
import apiclient.http
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
    code = attr.ib(None)
    response = attr.ib(None)
    token_file_data = attr.ib(None)
    credentials = attr.ib(None)
    service = attr.ib(None)
    session = attr.ib(None)
    server_app = attr.ib(None)
    server_thread = attr.ib(None)
    server_response = attr.ib({})
    server_host = attr.ib('0.0.0.0')
    server_port = attr.ib(8022)
    server_route = attr.ib('/oauth_redirect_uri')
    httpd = None

    def close_server(self):
        self.httpd.shutdown()
        return self

    def run_server(self):
        self.server_app = flask.Flask(__name__)

        def view():
            response = dict(flask.request.args.items())
            self.server_response = response
            return flask.Response(
                json.dumps(response),
                content_type='application/json',
            )

        self.server_app.route(self.server_route)(view)
        self.httpd = wsgiref.simple_server.make_server(
            app=self.server_app,
            host=self.server_host,
            port=self.server_port,
        )
        self.server_thread = threading.Thread(
            target=lambda: self.httpd.serve_forever(poll_interval=0.5))
        self.server_thread.start()
        return self

    def load(self):
        self.credential_file_data = (self.credential_file_data or addict.Dict(
            json.load(open(self.credential_file))))
        return self

    def get_session(self):
        self.session = requests_oauthlib.OAuth2Session(
            client_id=self.credential_file_data.web.client_id,
            scope=self.scope,
            redirect_uri=self.credential_file_data.web.redirect_uris[0],
            auto_refresh_url=self.auto_refresh_url,
            auto_refresh_kwargs=dict(
                client_id=self.credential_file_data.web.client_id,
                client_secret=self.credential_file_data.web.client_secret,
            ))
        return self

    def write(self):
        open(self.token_file, 'w').write(json.dumps(self.response))
        return self

    def auth(self):
        if not os.path.exists(self.token_file):
            print(
                self.session.authorization_url(
                    access_type="offline",
                    url=self.credential_file_data.web.auth_uri,
                    # prompt="select_account",
                    approval_prompt="force",
                )[0])
            while True:
                if self.server_response:
                    self.code = self.server_response['code']
                    break
                time.sleep(1)
            self.response = addict.Dict(
                self.session.fetch_token(
                    self.credential_file_data.web.token_uri,
                    client_secret=self.credential_file_data.web.client_secret,
                    code=self.code,
                    verify=False,
                    token_updater=(lambda *args: print('token_updater', args)),
                ))
            # open(self.token_file, 'w').write(json.dumps(self.response))
        else:
            self.token_file_data = (self.token_file_data or addict.Dict(
                json.load(open(self.token_file))))
            if datetime.datetime.fromtimestamp(self.token_file_data.expires_at
                                               ) < datetime.datetime.utcnow():
                self.response = addict.Dict(
                    self.session.refresh_token(
                        self.token_uri, self.token_file_data.refresh_token))
                # open(self.token_file, 'w').write(json.dumps(self.response))
            else:
                self.response = addict.Dict(self.token_file_data)
        return self

    def get_credentials(self):
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
            credentials=self.credentials,
        )
        return self


def run(file=None, options={}):
    return OAuth(
        **dict((file and json.load(open(file))or {}), **options))\
        .load()\
        .run_server()\
        .get_session()\
        .auth()\
        .write()\
        .get_credentials()\
        .get_service()\
        .close_server()


def test_main():  # type: None
    pass


def main(argv=None):  # type: int
    fire.Fire()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
