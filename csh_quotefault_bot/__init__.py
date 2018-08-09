import os
import json
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
others = ['submit']

_url = app.config['QUOTEFAULT_ADDR'] + '/' + app.config['QUOTEFAULT_KEY']

responses.init(_url, multiples, app.config['OAUTH_TOKEN'])

@app.route('/')
def index():
    return "Hello World!"

@app.route('/quote', methods=['POST'])
def get_quote(): # pylint: disable=inconsistent-return-statements
    """
    Replies with a auote
    :return: The reply message
    """
    app.logger.info('Request recieved:')
    app.logger.info(request.form) # Debug
    if app.config['VERIFICATION_TOKEN'] == request.form['token']:
        command = request.form['text'].split(' ')[0]
        if command == 'help':
            return responses.help_msg('')
        if command in singles + multiples:
            return responses.respond(request.form['text'])
        if command == 'submit':
            return responses.submission(request.form['text'], request.form['user_id'])
        return responses.help_msg(command)
    abort(401)

@app.route('/interactive', methods=['POST'])
def do_interact():
    """
    Handles interactive components.
    """
    data = json.loads(request.form['payload'])

    app.logger.info('Interaction recieved:')
    app.logger.info(data)

    if data['type'] == 'message_action':
        action(data)

    return 200

def action(data: dict):# TODO move to responses
    response_url = data['response_url']
    submitter = data['user']['id']
    speaker = data['message']['user']
    quote = data['message']['text']

    msg = f'"#{quote}" -#{speaker}, submitted by #{submitter}'
    requests.put(response_url, json={'text':msg, 'response_type':'ephemeral'}) # pylint: disable=undefined-variable
