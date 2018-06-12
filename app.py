#!flask/bin/python
from flask import Flask, request, abort
import os
import responses

app = Flask(__name__)

if os.path.exists(os.path.join(os.getcwd(), "config.py")):
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))
else:
    app.config.from_pyfile(os.path.join(os.getcwd(), "config.env.py"))

singles = ['random', 'newest']

@app.route('/')
def index():
    return "Hello World!"

@app.route('/quote', methods=['POST'])
def get_quote():
    """
    Replies with a auote
    :return: The reply message
    """
    app.logger.info(request.form) # Debug
    if(app.config['VERIFICATION_TOKEN'] == request.form['token']):
        command = request.form['text'].split(' ')[0]
        # TODO use a dictionary to map to functions in responses.py
        if(command == 'help'):
            return responses.help_msg('')
        elif(command in singles):
            return responses.single(request.form['text'])
        else:
            return responses.help_msg(command)
    else:
        abort(401)

if __name__ == '__main__':
    app.run(host = app.config['IP'], port = int(app.config['PORT']), debug = True)
