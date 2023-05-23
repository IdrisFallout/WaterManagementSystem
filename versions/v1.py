from flask import Blueprint

api_v1 = Blueprint('api_v1', __name__)


@api_v1.route('/resource', methods=['GET'])
def get_resource():
    return 'Version 1 of the resource'
