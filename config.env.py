import os

# Flask Config
DEBUG = True
IP = os.environ.get('API_IP', '127.0.0.1')
PORT = os.environ.get('API_PORT', 5000)
SERVER_NAME = os.environ.get('API_SERVER_NAME', '')

# Quotefault API config
QUOTEFAULT_ADDR = os.environ.get('QUOTEFAULT_API_ADDR', 'quotefault-api.csh.rit.edu')
QUOTEFAULT_KEY = os.environ.get('QUOTEFAULT_API_KEY', '')

# Slack creds
CLIENT_ID = os.environ.get('SLACK_CLIENT_ID', '');
CLIENT_SECRET = os.environ.get('SLACK_CLIENT_SECRET', '')
VERIFICATION_TOKEN = os.environ.get('SLACK_VERIFICATION_TOKEN', '')

# CSH LDAP creds
LDAP_BIND_DN = os.environ.get('LDAP_BIND_DN', '')
LDAP_BIND_PASS = os.environ.get('LDAP_BIND_PASS', '')
