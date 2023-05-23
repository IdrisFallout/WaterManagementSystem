from flask import Blueprint, request, abort

api_v1 = Blueprint('api_v1', __name__)


# require API key for all routes in this blueprint
@api_v1.before_request
def before_request():
    # get the API key from the query string
    api_key = request.headers.get('X-API-Key')

    # if the API key is missing or invalid, return an error
    if not api_key or api_key != 'eiWee8ep9due4deeshoa8Peichai8Eih':
        abort(401)


@api_v1.route('/resource', methods=['GET'])
def get_resource():
    return 'Version 1 of the resource'
