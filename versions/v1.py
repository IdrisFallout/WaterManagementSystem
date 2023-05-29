import psycopg2
import requests
from flask import Blueprint, request, abort

api_v1 = Blueprint('api_v1', __name__)

conn = psycopg2.connect(
    database="watermanagementsystem",
    user="idrisfallout",
    password="xxVkKFJt0tilbf6cyL7naRjreNlAz1rI",
    host="dpg-chlqusbhp8uej745khj0-a.oregon-postgres.render.com",
    port="5432"
)

# Replace with your actual M-Pesa API credential
consumer_key = "4IewHc4m1sHEvGp92vvszuvFxzhPLxeF"
consumer_secret = "6A8jzT4ls55N27Fo"
shortcode = ""
passkey = ""
initiator_name = "testapi"

# Replace with the appropriate API endpoints
access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
lipa_na_mpesa_online_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"


# Generate access token
def generate_access_token():
    response = requests.get(access_token_url, auth=(consumer_key, consumer_secret))
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return f"Request failed with status code {response.status_code}: {response.reason}"


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


@api_v1.route('/resource', methods=['GET'])
def get_resource():
    return 'Version 1 of the resource. Here is your access token: ' + generate_access_token()


# Make an M-Pesa STK Push request
def lipa_na_mpesa_online(access_token, phone_number, amount):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "BusinessShortCode": shortcode,
        "Password": passkey,
        "Timestamp": "yyyyMMddHHmmss",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": "YOUR_CALLBACK_URL",
        "AccountReference": "YOUR_ACCOUNT_REFERENCE",
        "TransactionDesc": "YOUR_TRANSACTION_DESCRIPTION"
    }
    response = requests.post(lipa_na_mpesa_online_url, json=payload, headers=headers)
    return response.json()
