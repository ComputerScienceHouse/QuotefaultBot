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
            + "\tBETA: `--speaker [name]` - limits search by speaker. Speaker can be any string, not just a username.\n"
            + "`newest` - grabs the newest quote and posts it to the current channel.\n"
            + "Arguements:\n"
            + "\t`--submitter [username]` - limit search to a specific submitter by CSH username\n"
            + "\t`--date [date]` - limits search by date. 'MM-DD-YYYY'"
            + "\tBETA: `--speaker [name]` - limits search by speaker. Speaker can be any string, not just a username.\n",
            response_type = 'ephemeral'
            )

def single(request: str):
    command = request.split(' ')
    submitter = command[command.index('--submitter') + 1] if '--submitter' in command else ''
    date = command[command.index('--date') + 1] if '--date' in command else ''
    speaker = command[command.index('--speaker') + 1] if '--speaker' in command else ''
    query = ''
    if date or submitter or speaker:
        query += '?'
        if submitter:
            query += 'submitter=' + submitter
            if date or speaker:
                query += '&'
        if date:
            query += 'date=' + date
            if speaker:
                query += '&'
        if speaker:
            query += 'speaker=' + speaker
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

def multiple(request: str):
    command = request.split(' ')
    submitter = command[command.index('--submitter') + 1] if '--submitter' in command else ''
    date = command[command.index('--date') + 1] if '--date' in command else ''
    speaker = command[command.index('--speaker') + 1] if '--speaker' in command else ''
    if command[0] == 'between':
        date = ''
    query = ''
    if date or submitter or speaker:
        query += '?'
        if submitter:
            query += 'submitter=' + submitter
            if date or speaker:
                query += '&'
        if date:
            query += 'date=' + date
            if speaker:
                query += '&'
        if speaker:
            query += 'speaker=' + speaker
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
        big_text = ''
        for i in json:
            big_text += '> ' + i['quote'] + '\n-' + i['speaker'] + '\nSubmitted by: ' + i['submitter'] + '\n'
        return jsonify(
                text = big_text,
                #response_type = 'in_channel'
                response_type = 'ephemeral'
                )
    except:
        app.logger.warning('Query: "' + request + '", requests to API failed.\nError: ' + traceback.format_exc())
        return jsonify(
                text = 'Failed to query quotefault. Please try again. If that fails, message user:mom',
                response_type = 'ephemeral'
                )
