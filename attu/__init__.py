from flask import Flask
import os

app = Flask(__name__)
app.config['DB_PATH'] = os.path.join(os.path.dirname(__file__),
                                     'lds_scriptures.db')
app.config['BASE_ADDRESS'] = 'localhost:8001'
if os.environ.get('ATTU_SETTINGS'):
    app.config.from_envvar('ATTU_SETTINGS')

import attu.views
