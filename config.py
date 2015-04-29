from flask import Flask
import os

basedir = os.environ['OPENSHIFT_DATA_DIR']

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['DATABASE_PATH'] = os.path.join(basedir,'app_databese.db')
