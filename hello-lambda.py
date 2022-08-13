import os, logging
from aiogram import Bot, Dispatcher, executor, types

TOKEN=os.environ.get('TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def lambda_handler(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


# URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)
# def send_message(text, chat_id):
#     final_text = "You said: " + text
#     url = URL + "sendMessage?text={}&chat_id={}".format(final_text, chat_id)
#     requests.get(url)
# def lambda_handler(event, context):
#     message = json.loads(event['body'])
#     chat_id = message['message']['chat']['id']
#     reply = message['message']['text']
#     send_message(reply, chat_id)
#     return {
#         'statusCode': 200
#     }