import os
from flask import Flask, request, abort
import requests
from csh_quotefault_bot import responses, ldap_utils

app = Flask(__name__)

if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

#LDAP
_LDAP = ldap_utils.LDAPUtils(app.config['LDAP_BIND_DN'], app.config['LDAP_BIND_PASS'])

singles = ['random', 'newest', 'id']
multiples = ['between', 'all']
others = ['submit', 'markov']

_url = app.config['QUOTEFAULT_ADDR'] + '/' + app.config['QUOTEFAULT_KEY']

responses.init(_url, multiples, _LDAP)

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

        # Authenticate
        slack_id = request.form['user_id']
        status, result = _LDAP.verify_slack_uid(slack_id)
        if status == 'failure':
            return "Could not autenticate you. Please visit https://eac.csh.rit.edu/slack"

        if command == 'help':
            return responses.help_msg('')
        if command in singles + multiples:
            return responses.respond(request.form['text'])
        if command == 'submit':
            return responses.submission(request.form['text'], result['uid'])
        if command == 'markov':
            return responses.markov(request.form['text'])
        return responses.help_msg(command)
    abort(401)
