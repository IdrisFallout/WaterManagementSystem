import secrets

from flask import Flask, url_for, redirect, request, abort
from versions import v1, v2

app = Flask(__name__)
# Register the blueprints from version scripts
app.register_blueprint(v1.api_v1, url_prefix='/api/v1')
app.register_blueprint(v2.api_v2, url_prefix='/api/v2')

app.secret_key = secrets.token_hex(16)  # Generate a random 32-character hexadecimal string


def generate_api_key():
    api_key = secrets.token_hex(16)  # Generate a random 32-character hexadecimal string
    return api_key


print(generate_api_key())

if __name__ == '__main__':
    app.run()
