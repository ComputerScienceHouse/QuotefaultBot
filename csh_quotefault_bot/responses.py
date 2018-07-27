import traceback
from flask import jsonify
import requests
#import multiples
#import app
from csh_quotefault_bot.ldap_utils import resolve_name

url = ''
multiples = []

def init(addr: str, multi: list):
    global url
    url = addr
    global multiples
    multiples = multi

def help_msg(command: str):
    wrong = '_Unrecognized: ' + command + '_\n\n' if command != '' else ''

    return jsonify(
            text=wrong + '''Help for CSH Quotefault bot.
All commands are in the form `/quote command_name [data and arguements]`

`help` - displays this message
`random` - grabs a random quote and posts it to the current channel.
`newest` - grabs the newest quote and posts it to the current channel.
`between <start> <end>` - returns all quotes between `start` and `end`. 'MM-DD-YYYY'.
`all` - responds with _*Every Single Quote*_. This cuts off at some point, so use arguements.
`id <qoute_id>` - responds with the specified quote, ignores arguements.

Arguements:
    `--submitter [username]` - limit search to a specific submitter by CSH username
    `--speaker [name]` - limits search by speaker. Speaker can be any string, not just a username.
    `--date [date]` - limits search by date. 'MM-DD-YYYY' Not useable for `between`''',
            response_type='ephemeral'
            )

def respond(slack_request: str):
    message = slack_request.split(' ')
    command = message[0]

    params = {}
    if command == 'between':
        # TODO add validation and error check
        params['start'] = message[1]
        params['end'] = message[2]
    if command == 'id':
        params['id'] = message[1]

    args = {}
    args['submitter'] = parse_arg(message, 'submitter')
    args['date'] = parse_arg(message, 'date')
    args['speaker'] = parse_arg(message, 'speaker')

    response = request(command, params, args)
    if response == 'err':
        # No response error message
        return jsonify(
                text='Failed to query quotefault. Please try again.'
                + 'If that fails, message user:mom',
                response_type='ephemeral'
                )
    if response.text == 'none':
        # No quotes found error message
        return jsonify(
                text='No quotes found, sorry.',
                response_type='ephemeral'
                )
    return make_slack_msg(response.json(), command in multiples)


def request(command: str, params: dict, args: dict):
    query = ''
    if command == 'between':
        args['date'] = ''
        command += '/' + params['start'] + '/' + params['end']
    if command == 'id':
        command = params['id']
    if args['date'] or args['submitter'] or args['speaker']:
        query += '?'
        if args['submitter']:
            query += 'submitter=' + args['submitter']
            if args['date'] or args['speaker']:
                query += '&'
        if args['date']:
            query += 'date=' + args['date']
            if args['speaker']:
                query += '&'
        if args['speaker']:
            query += 'speaker=' + args['speaker']
    try:
        print('Request URL: ' + url + '/' + command + query) # Debug
        response = requests.get(url + '/' + command + query)
        #print('Response:\n' + response)
        # app.logger.info(response)
        return response
    except: # pylint: disable=bare-except
        #app.logger.warning('Error:\n' + traceback.format_exc() + '\n\n')
        print('Error:\n' + traceback.format_exc() + '\n\n')
        return 'err'

def make_slack_msg(quotes, multiple: bool):
    msg = ''
    if multiple:
        for i in quotes:
            msg += f'''Quote #{i['id']}
> {i['quote']}
-{resolve_name(i['speaker'])}
Submitted by: {resolve_name(i['submitter'])}
'''
    else:
        print(quotes)
        msg = f'''Quote #{quotes['id']}
> {quotes['quote']}
-{resolve_name(quotes['speaker'])}
Submitted by: {resolve_name(quotes['submitter'])}'''
    return jsonify(
            text=msg,
            response_type='ephemeral' if multiple else 'in_channel'
            # If responding with multiple quotes, we don't want to clog channels.
           )

def parse_arg(message: list, arg: str):
    return message[message.index('--' + arg) + 1] if '--' + arg in message else ''
