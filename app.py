from flask import Flask, url_for, redirect
from versions import v1, v2

app = Flask(__name__)

# Register the blueprints from version scripts
app.register_blueprint(v1.api_v1, url_prefix='/api/v1')
app.register_blueprint(v2.api_v2, url_prefix='/api/v2')

if __name__ == '__main__':
    app.run()
