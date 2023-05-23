import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from versions import v1, v2
import secrets

app = Flask(__name__)
# Register the blueprints from version scripts
app.register_blueprint(v1.api_v1, url_prefix='/api/v1')
app.register_blueprint(v2.api_v2, url_prefix='/api/v2')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.app_context().push()


class APIKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(32), unique=True)


# generate an API key
@app.route('/generate-api-key', methods=['GET'])
def generate_api_key():
    api_key = secrets.token_hex(16)
    new_api_key = APIKey(key=api_key)
    db.session.add(new_api_key)
    db.session.commit()
    return 'API Key generated and stored in the database.'


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
