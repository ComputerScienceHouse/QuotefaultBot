from csh_quotefault_bot import app

if __name__ == '__main__':
    app.run(host = app.config['IP'], port = int(app.config['PORT']), debug = True)

application = app
