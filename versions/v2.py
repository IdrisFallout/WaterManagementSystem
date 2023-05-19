from flask import Blueprint

api_v2 = Blueprint('api_v2', __name__)


@api_v2.route('/resource', methods=['GET'])
def get_resource():
    return 'Version 2 of the resource'
