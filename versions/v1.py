from flask import Blueprint, request, abort
import secrets

api_v1 = Blueprint('api_v1', __name__)


def generate_api_key():
    api_key = secrets.token_hex(16)  # Generate a random 32-character hexadecimal string
    return api_key


valid_api_keys = [f'{generate_api_key()}', f'{generate_api_key()}']
print(valid_api_keys)


@api_v1.before_request
def validate_api_key():
    #     get API Key from the header
    api_key = request.headers.get('API_KEY')
    print(api_key)
    # if request.headers.get('api_key') not in valid_api_keys:
    #     abort(401)


@api_v1.route('/resource', methods=['GET'])
def get_resource():
    return 'Version 1 of the resource'
