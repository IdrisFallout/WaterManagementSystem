import base64
from datetime import datetime

import psycopg2
import requests
from Crypto.PublicKey import RSA
from flask import Blueprint, request, abort

import random

api_v1 = Blueprint('api_v1', __name__)

conn = psycopg2.connect(
    database="watermanagementsystem",
    user="idrisfallout",
    password="xxVkKFJt0tilbf6cyL7naRjreNlAz1rI",
    host="dpg-chlqusbhp8uej745khj0-a.oregon-postgres.render.com",
    port="5432"
)

base_url = "https://e3d9-197-232-131-204.ngrok-free.app/api/v1"

# Replace with your actual M-Pesa API credential
consumer_key = "4IewHc4m1sHEvGp92vvszuvFxzhPLxeF"
consumer_secret = "6A8jzT4ls55N27Fo"
shortcode = "174379"  # 174379 / 8362942 / 6265952 / 247247
passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
initiator_name = "testapi"

# Replace with the appropriate API endpoints
access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
lipa_na_mpesa_online_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"


# @api_v1.before_request
def before_request():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_key")
    data = cursor.fetchall()
    cursor.close()

    api_key = request.headers.get('X-API-Key')

    # Check if the API key exists in the stored_api_key list
    if api_key not in [key for _, key in data]:
        abort(401)  # Unauthorized


# AUTHORIZATION API
def generate_access_token():
    response = requests.get(access_token_url, auth=(consumer_key, consumer_secret))
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        return f"Request failed with status code {response.status_code}: {response.reason}"


@api_v1.route('/resource', methods=['GET'])
def get_resource():
    # public_key_path = 'venv/Lib/site-packages/certifi/cacert.pem'
    # with open(public_key_path, "rb") as key_file:
    #     public_key = RSA.import_key(key_file.read())
    return "public_key"


# Make an M-Pesa STK Push request
def lipa_na_mpesa_online(access_token, phone_number, amount):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    payload = {
        "BusinessShortCode": shortcode,
        "Password": base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode(),
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://e3d9-197-232-131-204.ngrok-free.app/api/v1/confirmation",
        "AccountReference": "254765566365",  # CompanyXLTD
        "TransactionDesc": f"Payment of KSH {amount} to {shortcode} by {phone_number}"
    }
    response = requests.post(lipa_na_mpesa_online_url, json=payload, headers=headers, verify=False)
    return response.json()


@api_v1.route('/lipa', methods=['POST'])
def lipa():
    access_token = generate_access_token()
    phone_number = request.json['PhoneNumber']
    amount = request.json['Amount']
    response = lipa_na_mpesa_online(access_token, phone_number, amount)
    return response


@api_v1.route('/register_urls', methods=['POST'])
def register_urls():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": f"Bearer {generate_access_token()}"}
    payload = {
        "ShortCode": shortcode,
        "ResponseType": "Completed",
        "ConfirmationURL": f"{base_url}/confirmation",
        "ValidationURL": f"{base_url}/validation"
    }
    response = requests.post(mpesa_endpoint, json=payload, headers=headers)
    return response.json()


# ACCOUNT BALANCE API
@api_v1.route('/account_balance', methods=['GET'])
def account_balance():
    mpesa_endpoint = "https://sandbox.safaricom.co.ke/mpesa/accountbalance/v1/query"
    headers = {"Authorization": f"Bearer {generate_access_token()}"}
    payload = {
        "Initiator": initiator_name,
        "SecurityCredential": "jL/C5aM4wjaLPnKC/HCWiOesJEZ3Lxv2S0z+3ynPWdljlGU3LWH5Sn4D47pskOqdNjbhsPhta48we1JCgp7hclcnUMrKWytC6xnATW0wV36LJz6XOKiCYW64iNVRsLkxrag2zBToLbFBmJP6P/InvFjJAfBB2Mo2U0pZVleVyr/JndnOmJofTvBYkz8G2OmdngjU0TKdrUlQRdHNEq0inTANFBr5kkKQBDE/z6NA6qUVaJnsUw+55pn1XiITelqf/J4UFqkrXY3u1vf07qrUTXfZINHbU+C/j5ak4XPAs2VtXlEsQ3cEgwFyLnhNlFwg5lOlj9Q6mq1tlE3a3HfxRA==",
        "CommandID": "AccountBalance",
        "PartyA": shortcode,
        "IdentifierType": "4",
        "Remarks": "done!",
        "QueueTimeOutURL": f"{base_url}/AccountBalance/queue",
        "ResultURL": f"{base_url}/AccountBalance/result"
    }
    response = requests.post(mpesa_endpoint, json=payload, headers=headers)
    return response.json()


@api_v1.route('/confirmation', methods=['POST'])
def confirmation():
    print(request.json)
    return request.json


@api_v1.route('/validation', methods=['POST'])
def validation():
    print(request.json)
    return request.json


@api_v1.route('/AccountBalance/queue', methods=['POST'])
def queue():
    print(request.json)
    return request.json


@api_v1.route('/AccountBalance/result', methods=['POST'])
def result():
    print(request.json)
    return request.json


# generate token function takes in phone number and amount as parameters and outputs a 20 numerical digits number
def generate_token(meter_number, amount, phone_number, timestamp):
    token = f"{meter_number}-{amount}-{phone_number}-{timestamp}"
    count = len(token)
    return token + "-" + str(count - 3)


@api_v1.route('/generate_token_number', methods=['POST'])
def generate_token_number():
    phone_number = request.json['PhoneNumber']
    amount = request.json['Amount']
    meter_number = request.json['MeterNumber']
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    # secret_key = it is unique for every meter number, retrieve from the database
    return generate_token(meter_number, amount, phone_number, timestamp)
