#!flask/bin/python
from flask import Flask, request, abort
import os

app = Flask(__name__)

if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

@app.route('/')
def index():
	return "Hello World!"

@app.route('/quote', methods=['POST'])
def get_quote():
	"""
	Replies with a random quote.
	:return: The reply message
	"""
	# TODO Parse the message from slack.
	app.logger.info(request.form)
	if(app.config['VERIFICATION_TOKEN'] == request.form['token']):
		return "Hello, <@" + request.form['user_id'] +">. Message recieved."
	else:
		abort(401)


if __name__ == '__main__':
	app.run(host = app.config['IP'], port = int(app.config['PORT']), debug = True)
