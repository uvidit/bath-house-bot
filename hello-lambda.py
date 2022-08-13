import json, os
from botocore.vendored import requests
TELE_TOKEN=os.environ.get('TOKEN')
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)
def send_message(text, chat_id):
    final_text = "You said: " + text
    url = URL + "sendMessage?text={}&chat_id={}".format(final_text, chat_id)
    requests.get(url)
def lambda_handler(event, context):
    message = json.loads(event['body'])
    chat_id = message['message']['chat']['id']
    reply = message['message']['text']
    send_message(reply, chat_id)
    return {
        'statusCode': 200
    }