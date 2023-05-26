from flask import Blueprint, request, abort
import psycopg2

api_v1 = Blueprint('api_v1', __name__)

conn = psycopg2.connect(
    database="watermanagementsystem",
    user="idrisfallout",
    password="xxVkKFJt0tilbf6cyL7naRjreNlAz1rI",
    host="dpg-chlqusbhp8uej745khj0-a.oregon-postgres.render.com",
    port="5432"
)


# require API key for all routes in this blueprint
@api_v1.before_request
def before_request():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_key")
    data = cursor.fetchall()
    cursor.close()

    api_key = request.headers.get('X-API-Key')

    # Check if the API key exists in the stored_api_key list
    if api_key not in [key for _, key in data]:
        abort(401)  # Unauthorized

    # return 'API key is valid'


@api_v1.route('/resource', methods=['GET'])
def get_resource():
    return 'Version 1 of the resource'
