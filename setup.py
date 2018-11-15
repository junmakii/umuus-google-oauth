
from setuptools import setup, find_packages

setup(
    name='umuus_google_oauth',
    description='A package.',
    long_description=('A package.\n'
 '\n'
 'umuus-google-oauth\n'
 '==================\n'
 '\n'
 'Installation\n'
 '------------\n'
 '\n'
 '    $ pip install umuus_google_oauth\n'
 '\n'
 'Usage\n'
 '-----\n'
 '\n'
 '    $ python -m umuus_google_oauth run         --credential_file '
 "'client_secret_XXXX.apps.googleusercontent.com.json'         --token_file "
 'google_access_token.json\n'
 '\n'
 '\n'
 'Example\n'
 '-------\n'
 '\n'
 '    $ umuus_google_oauth\n'
 '\n'
 '    >>> import umuus_google_oauth\n'
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
    py_modules=['umuus_google_oauth'],
    version='0.1',
    url='https://github.com/junmakii/umuus-google-oauth',
    author='Jun Makii',
    author_email='junmakii@gmail.com',
    keywords=[],
    license='GPLv3',
    scripts=[],
    install_requires=['addict', 'fire', 'oauth2client', 'google-auth', 'google-api-python-client', 'httplib2', 'oauthlib', 'requests_oauthlib'],
    dependency_links=[],
    classifiers=['Development Status :: 3 - Alpha', 'Intended Audience :: Developers', 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)', 'Natural Language :: English', 'Programming Language :: Python', 'Programming Language :: Python :: 3'],
    entry_points={'console_scripts': ['umuus_google_oauth = umuus_google_oauth:main']}
)

