import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from versions import v1, v2

app = Flask(__name__)
# Register the blueprints from version scripts
app.register_blueprint(v1.api_v1, url_prefix='/api/v1')
app.register_blueprint(v2.api_v2, url_prefix='/api/v2')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
