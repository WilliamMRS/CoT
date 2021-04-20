GET STARTED:

inside flask_server folder in cmd:
Create venv on mac & linux: 'python3 -m venv venv'
windows: 'py -3 -m venv venv'


in the directory flask_server activate environemnt for development using command: '. venv/bin/activate'

For å kjøre serveren, først i flask_server mappen skriv:
'export FLASK_APP=server.py'
så 'flask run'
source: https://flask.palletsprojects.com/en/1.1.x/quickstart/

Enable autoreload (så man ikke trenger å eksportere hver gang):
    To enable all development features (including debug mode) you can export the FLASK_ENV environment variable and set it to development before running the server:
    $ export FLASK_ENV=development
    $ flask run

This does the following things:

it activates the debugger
it activates the automatic reloader
it enables the debug mode on the Flask application.