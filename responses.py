from flask import jsonify
from app import app
import requests
import traceback

url = app.config['QUOTEFAULT_ADDR'] + '/' + app.config['QUOTEFAULT_KEY']

def help_msg(command: str):
    wrong = '_Unrecognized: ' + command + '_\n\n' if command != '' else ''
        
    return jsonify(
            text = wrong + "Help for CSH Quotefault bot.\n"
            + "All commands are in the form `/quote command_name [data and arguements]`\n\n"
            + "`help` - displays this message\n"
            + "`random` - grabs a random quote and posts it to the current channel.\n"
            + "Arguements:\n"
            + "\t`--submitter [username]` - limit search to a specific submitter by CSH username\n"
            + "\t`--date [date]` - limits search by date. 'MM-DD-YYYY'\n"
            + "`newest` - grabs the newest quote and posts it to the current channel.\n"
            + "Arguements:\n"
            + "\t`--submitter [username]` - limit search to a specific submitter by CSH username\n"
            + "\t`--date [date]` - limits search by date. 'MM-DD-YYYY'",  
            response_type="ephemeral"
            )

def single(request: str):
    command = request.split(' ')
    submitter = command[command.index('--submitter') + 1] if '--submitter' in command else ''
    date = command[command.index('--date') + 1] if '--date' in command else ''
    query = ''
    if date or submitter:
        query += '?'
        if submitter:
            query += 'submitter=' + submitter
            if date:
                query += '&'
        if date:
            query += 'date=' + date
    try:
        print('Request URL: ' + url + '/' + command[0] + query) # Debug
        response = requests.get(url + '/' + command[0] + query)
        app.logger.info(response) # Debug
        if response.text == "none":
            return jsonify(
                    text = 'No quotes found, sorry.',
                    response_type = 'ephemeral'
                    )
        json = response.json()
        app.logger.info(json) # Debug
        return jsonify(
                text = '> ' + json['quote'] + '\n-' + json['speaker'] + '\nSubmitted by: ' + json['submitter'],
                response_type = 'in_channel'
                )
    except:
        app.logger.warning('Query: "' + request + '", requests to API failed.\nError: ' + traceback.format_exc())
        return jsonify(
                text = 'Failed to query quotefault. Please try again. If that fails, message user:mom',
                response_type = 'ephemeral'
                )

