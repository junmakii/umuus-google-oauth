
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def run_tests(self):
        import sys
        import shlex
        import pytest
        errno = pytest.main(['--doctest-modules'])
        if errno != 0:
            raise Exception('An error occured during installution.')
        install.run(self)


setup(
    packages=setuptools.find_packages('.'),
    version='0.1',
    url='https://github.com/junmakii/umuus-google-oauth',
    author='Jun Makii',
    author_email='junmakii@gmail.com',
    keywords=[],
    license='GPLv3',
    scripts=[],
    install_requires=['attrs',
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
 'flask'],
    dependency_links=[],
    classifiers=['Development Status :: 3 - Alpha',
 'Intended Audience :: Developers',
 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
 'Natural Language :: English',
 'Programming Language :: Python',
 'Programming Language :: Python :: 3'],
    entry_points={'console_scripts': ['umuus_google_oauth = umuus_google_oauth:main'],
 'gui_scripts': []},
    project_urls={'Bug Tracker': 'https://github.com/junmakii/umuus-google-oauth/issues',
 'Documentation': 'https://github.com/junmakii/umuus-google-oauth/',
 'Source Code': 'https://github.com/junmakii/umuus-google-oauth/'},
    setup_requires=['pytest-runner'],
    test_suite='umuus_google_oauth',
    tests_require=['pytest'],
    extras_require={},
    package_data={'': []},
    python_requires='>=3.0.0',
    include_package_data=True,
    zip_safe=True,
    name='umuus-google-oauth',
    description='Utilities, tools, and scripts for Python.',
    long_description=('Utilities, tools, and scripts for Python.\n'
 '\n'
 'umuus-google-oauth\n'
 '==================\n'
 '\n'
 'Installation\n'
 '------------\n'
 '\n'
 '    $ pip install git+https://github.com/junmakii/umuus-google-oauth.git\n'
 '\n'
 '    $ pip install addict fire oauth2client google-auth '
 'google-api-python-client httplib2 oauthlib requests_oauthlib attrs\n'
 '\n'
 '\n'
 'Command Line\n'
 '------------\n'
 '\n'
 '    $ python -m umuus_google_oauth run       --credential_file '
 '"config/google/client_secret_XXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com.json"       '
 '--token_file "config/google/google_youtube_access_token.json"       --scope '
 '"$(cat config/google/google_youtube_scope.json)"\n'
 '\n'
 'Code\n'
 '----\n'
 '\n'
 '    import umuus_google_oauth\n'
 '\n'
 '    umuus_google_oauth.run(\n'
 '        '
 'credential_file="config/google/client_secret_XXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com.json",\n'
 '        token_file="config/google/google_youtube_access_token.json",\n'
 '        scope="$(cat config/google/google_youtube_scope.json)",\n'
 '    )\n'
 '\n'
 'Example\n'
 '-------\n'
 '\n'
 '    $ umuus_google_oauth\n'
 '\n'
 '    >>> import umuus_google_oauth\n'
 '\n'
 '\n'
 'Authors\n'
 '-------\n'
 '\n'
 '- Jun Makii <junmakii@gmail.com>\n'
 '\n'
 'License\n'
 '-------\n'
 '\n'
 'GPLv3 <https://www.gnu.org/licenses/>'),
    cmdclass={"pytest": PyTest},
)
