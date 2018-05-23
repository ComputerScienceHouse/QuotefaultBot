from flask import jsonify
from app import app
import requests

url = app.config['QUOTEFAULT_ADDR'] + '/' + app.config['QUOTEFAULT_KEY']

def help_msg():
	return jsonify(
			text = "Help for CSH Quotefault bot.\n"
			+ "All commands are in the form `/quote command_name [data and arguements]`\n\n"
			+ "`help` - displays this message\n"
			+ "`random` - grabs a random quote and posts it to the current channel",
			response_type="ephemeral"
			)

def random():
	response = requests.get(url + '/random').json()
	return jsonify(
			text = '> ' + response['quote'] + '\n-' + response['speaker'] + '\nSubmitted by: ' + response['submitter'],
			response_type="in_channel"
			)



