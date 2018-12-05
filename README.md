
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

    $ python -m umuus_google_oauth run       --credential_file "config/google/client_secret_XXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com.json"       --token_file "config/google/google_youtube_access_token.json"       --scope "$(cat config/google/google_youtube_scope.json)"

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