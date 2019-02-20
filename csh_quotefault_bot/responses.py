import traceback
from flask import jsonify
import requests

url = ''
multiples = []
_LDAP = None

def init(addr: str, multi: list, ldap):
    global url
    global multiples
    global _LDAP
    url = addr
    multiples = multi
    _LDAP = ldap

def help_msg(command: str):
    wrong = '_Unrecognized: ' + command + '_\n\n' if command != '' else ''

    return jsonify(
            text=wrong + '''Help for CSH Quotefault bot.
All commands are in the form `/quote command_name [data and arguments]`

`help` - displays this message
`random` - grabs a random quote and posts it to the current channel.
`newest` - grabs the newest quote and posts it to the current channel.
`between <start> <end>` - returns all quotes between `start` and `end`. 'MM-DD-YYYY'.
`all` - responds with _*Every Single Quote*_. This cuts off at some point, so use arguments.
`id <quote_id>` - responds with the specified quote, ignores arguments.
`markov <count>` - responds with a generated quote. Takes speaker and submitter arguements. Count is optional.
`submit "<quote>" - <speaker>` - quote is the quote to submit, speaker is the CSH username of the speaker of the quote. Does not accept arguments.

Arguments:
    `--submitter [username]` - limit search to a specific submitter by CSH username
    `--speaker [name]` - limits search by speaker. Speaker can be any string, not just a username.
    `--date [date]` - limits search by date. 'MM-DD-YYYY' Not useable for `between`.''',
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
                + 'If that fails, message @mom',
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

def submission(text: str, user_name: str):
    text = text.replace('“', '"').replace('”', '"')
    if 'quote="' in text and 'speaker="' in text:
        quote = substring(text, 'quote="', '"')
        speaker = substring(text, 'speaker="', '"')
    else: # "<quote>" -<speaker> format
        start = text.index('"')
        end = text.index('"', start + 1)
        dash = text.index('-', end)
        quote = text[start+1:end].strip()
        speaker = text[dash+1:].strip()


    status = _LDAP.validate_uid(speaker)[0]
    if status == 'failure':
        return f'Could not validate {speaker} as a CSH username.'

    res = requests.put(url + '/create', json={'quote':quote, 'submitter':user_name, 'speaker':speaker})
    #return jsonify(quote=quote, submitter=uid, speaker=speaker) # DEBUG
    return "You're getting the raw API response, at least until I make it fancy\n\n" + res.text

def markov(text: str):
    words = text.split()

    speaker = parse_arg(words, 'speaker')
    submitter = parse_arg(words, 'submitter')

    query_args = ''
    if speaker:
        query_args += 'speaker=' + speaker
    if submitter:
        if query_args != '':
            query_args += '&'
        query_args += 'submitter=' + submitter
    if query_args != '':
        query_args = '?' + query_args

    print('DEBUG: Markov query args :', query_args)

    url_arg = ''
    return_type = 'in_channel'
    if len(words) > 1:
        if '-' not in words[1]:
            if int(words[1]) > 5:
                return_type = 'ephemeral'
            url_arg = '/' + words[1].strip()

    quotes = requests.get(url + '/markov' + url_arg + query_args).json()
    if isinstance(quotes, str):
        quotes = [quotes]
    return jsonify(
            text="\n".join(quotes),
            response_type=return_type
            )


def make_slack_msg(quotes, multiple: bool):
    msg = ''
    if multiple:
        for i in quotes:
            speaker = i['speaker']
            status, result = _LDAP.validate_uid(speaker)
            if status == 'ok':
                speaker = result['name']

            submitter = i['submitter']
            status, result = _LDAP.validate_uid(submitter)
            if status == 'ok':
                submitter = result['name']

            msg += f'''Quote #{i['id']}
> {i['quote']}
-{speaker}
Submitted by: {submitter}
'''
    else:
        speaker = quotes['speaker']
        status, result = _LDAP.validate_uid(speaker)
        if status == 'ok':
            speaker = result['name']

        submitter = quotes['submitter']
        status, result = _LDAP.validate_uid(submitter)
        if status == 'ok':
            submitter = result['name']
        print(quotes)
        msg = f'''Quote #{quotes['id']}
> {quotes['quote']}
-{speaker}
Submitted by: {submitter}'''
    return jsonify(
            text=msg,
            response_type='ephemeral' if multiple else 'in_channel'
            # If responding with multiple quotes, we don't want to clog channels.
           )

def parse_arg(message: list, arg: str):
    return message[message.index('--' + arg) + 1] if '--' + arg in message else ''

def substring(text: str, start: str, end: str):
    start_i = text.index(start) + len(start)
    end_i = text.index(end, start_i)
    return text[start_i:end_i]
