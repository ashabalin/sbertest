import os
from datetime import datetime, date
from logging.config import dictConfig

from flask import Flask
from flask import request, redirect, url_for, render_template

from blueprint_api import blueprint_api


PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))


test_config = {
    'SECRET_KEY': 'dev',
    'UPLOAD_PATH': os.path.join(PROJECT_PATH, 'upload'),
}


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(blueprint_api)

    return app


app = create_app(test_config)


@app.template_filter('date')
def format_date(value):
    if isinstance(value, (date, datetime)):
        return value.strftime('%d.%m.%Y')


@app.template_filter('datetime')
def format_datetime(value):
    if isinstance(value, datetime):
        return value.strftime('%d.%m.%Y %H:%M:%S')


@app.route('/')
def home():
    return render_template('home.html')


'''
logging configuration
'''
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file':
        {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'log/error.log',
        },
        'debug':
        {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': 'log/debug.log',
        }
    },
    'loggers': {
        'root': {
            'handlers': ['console', 'file']
        },
        'custom': {
            'handlers': ['debug'],
            'level': 'DEBUG'
        }
    }
})


# Start development web server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
