from flask import jsonify
import app
import requests
import traceback
from ldap_utils import resolve_name

url = app.app.config['QUOTEFAULT_ADDR'] + '/' + app.app.config['QUOTEFAULT_KEY']

def help_msg(command: str):
    wrong = '_Unrecognized: ' + command + '_\n\n' if command != '' else ''
        
    return jsonify(
            text = wrong + "Help for CSH Quotefault bot.\n"
            + "All commands are in the form `/quote command_name [data and arguements]`\n\n"
            + "`help` - displays this message\n"
            + "`random` - grabs a random quote and posts it to the current channel.\n"
            + "`newest` - grabs the newest quote and posts it to the current channel.\n"
            + "`between <start> <end>` - returns all quotes between `start` and `end`. 'MM-DD-YYYY'.\n"
            + "`all` - responds with _*Every Single Quote*_. This cuts off at some point, so use arguements.\n"
            + "`id <qoute_id>` - responds with the specified quote, ignores arguements.\n\n"
            + "Arguements:\n"
            + "\t`--submitter [username]` - limit search to a specific submitter by CSH username\n"
            + "\t`--speaker [name]` - limits search by speaker. Speaker can be any string, not just a username.\n"
            + "\t`--date [date]` - limits search by date. 'MM-DD-YYYY' Not useable for `between`\n",
            response_type = 'ephemeral'
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
                text = 'Failed to query quotefault. Please try again.'
                + 'If that fails, message user:mom',
                response_type = 'ephemeral'
                )
    elif response.text == 'none':
        # No quotes found error message
        return jsonify(
                text = 'No quotes found, sorry.',
                response_type = 'ephemeral'
                )
    else:
        return make_slack_msg(response.json(), command in app.multiples)


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
        print('Response:\n')
        app.app.logger.info(response)
        return response
    except:
        app.app.logger.warning('Error:\n' + traceback.format_exc() + '\n\n')
        return 'err'

def make_slack_msg(quotes, multiple: bool):    
    msg = ''
    if multiple:
        for i in quotes:
            msg += 'Quote #' + str(i['id']) + '\n> ' + i['quote'] + '\n-' + resolve_name(i['speaker']) + '\nSubmitted by: ' + resolve_name(i['submitter']) + '\n'
    else:
        msg = 'Quote #' + str(quotes['id']) + '\n> ' + quotes['quote'] + '\n-' + resolve_name(quotes['speaker']) + '\nSubmitted by: ' + resolve_name(quotes['submitter'])
    return jsonify(
            text = msg,
            response_type = 'ephemeral' if multiple else 'in_channel'
            # If responding with multiple quotes, we don't want to clog channels.
           )
 
def parse_arg(message: list, arg: str):
    return message[message.index('--' + arg) + 1] if '--' + arg in message else ''

