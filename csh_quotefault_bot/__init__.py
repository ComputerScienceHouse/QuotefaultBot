import os
from flask import Flask, request, abort
import requests
import csh_ldap
from csh_quotefault_bot import responses, ldap_utils

app = Flask(__name__)

if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

#LDAP
_ldap = csh_ldap.CSHLDAP(app.config['LDAP_BIND_DN'], app.config['LDAP_BIND_PASS'])
ldap_utils.init(_ldap)

singles = ['random', 'newest', 'id']
multiples = ['between', 'all']
others = ['submit', 'markoc']

_url = app.config['QUOTEFAULT_ADDR'] + '/' + app.config['QUOTEFAULT_KEY']

responses.init(_url, multiples)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/quote', methods=['POST'])
def get_quote(): # pylint: disable=inconsistent-return-statements,too-many-return-statements
    """
    Replies with a quote
    :return: The reply message
    """
    app.logger.info('Request received:')
    app.logger.info(request.form) # Debug
    if app.config['VERIFICATION_TOKEN'] == request.form['token']:
        command = request.form['text'].split(' ')[0]

        # Authenticate.
        addr = 'https://slack.com/api/users.profile.get?'
        addr += 'token=' + app.config['OAUTH_TOKEN'] + '&user=' + request.form['user_id']
        res = requests.get(addr)
        print(res.json())
        email = res.json()['profile']['email']
        if '@csh.rit.edu' in email:
            uid = email.split('@')[0]
        else:
            return '''Could not find your CSH username.
Please set your email to your CSH email at https://cshrit.slack.com/account/settings#email'''
        if ldap_utils.resolve_name(uid) == uid:
            return '''Your email on Slack seems to be an alias.
Please use your base email so I can verify your identity.
You can set that at https://cshrit.slack.com/account/settings#email'''

        if command == 'help':
            return responses.help_msg('')
        if command in singles + multiples:
            return responses.respond(request.form['text'])
        if command == 'submit':
            return responses.submission(request.form['text'], uid)
        if command == 'markov':
            return responses.markov(request.form['text'])
        return responses.help_msg(command)
    abort(401)
