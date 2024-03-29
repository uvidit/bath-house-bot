import json, logging, os, re, requests, openai
from aiogram import Bot, Dispatcher, executor, types
from random import randint
from bs4 import BeautifulSoup


# =====================================================================================================================
# = VARIABLES, LOGGING ================================================================================================
API_TOKEN = os.environ.get('TOKEN')
OPENAI_TOKEN = os.environ.get('OPENAI_TOKEN')
log = logging.getLogger(__name__)
log.setLevel(os.environ.get('LOGGING_LEVEL', 'INFO').upper())

# Here you can override the token to use the bot for debugging - don't forget to roll-back that
# API_TOKEN = 'someTokenThere'
# OPENAI_TOKEN = 'someTokenForChatGpt'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
message_chat_id = -1
openai.api_key = OPENAI_TOKEN

polls_db = {}  # save poll data results here

# =====================================================================================================================
# = THIS COMMANDS CONFIGURED FOR BOT INSIDE TELEGRAM BY THE BOTFATHER =================================================
command_list = '''
/start - Иди в баню!?
/help - Начальника сафсем глупый! Слова волшебные знать надо!
/jason- Зови Жасона во всех непонятных ситуациях
/beer - По пиву?
/pogoda - Прогноз погоды сегодня на Яровой 8
/kogda - Когда идем в баню в следующий раз?
/how_much - Сколько за баню?
/crypt - Почем крипта для народа?
/fact - Скажи какую-то хрень
/joke - Расскажи шутку про Чака Норриса
'''


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    message_chat_id = message.chat.id
    await message.reply(f" Даров, {message.from_user.first_name}!\n Вот слова настоящего начальника:\n{command_list}\n")


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    message_chat_id = message.chat.id
    await message.reply(f" Начальника, дафай слофа говори:\n{command_list}\n")


jason_geo = ['ща...5 минут турецкий (с)',
             'работу работает! .... не то что вы - тунеядцы!',
             'позовите Жасона!',
             'в пути...',
             'скоро будет...',
             'подождем его!',
             'только он знает толк в кальянах!',
             'ничего без него не можете!',
             'ожидайте! вас много - а он один!',
             'точные координаты Жасона дорогого стОят',
             'Жасон, обнови статус!',
             ]


def get_random_jason_get():
    return jason_geo[randint(0, len(jason_geo) - 1)]


input_story_about_jason_for_chat_gpt: str = """
    Жасон - наш добрый друг и очень очень хороший парень! У него есть авто Ниссан Ноут, девушка Алла.\n
    Он до сих пор живет в высоком доме на Северной Салтовке в Харькове во время военных действий и не хочет ехать оттуда.\n 
    Его друзья часто уговаривают его уехать из Харькова во избежание мобилизации и других рисков войны.\n 
    Все хотят знать где Жассон. Он, к сожалению, трудоголик. Он лучше всех может посоветовать сериал.\n 
    Он любит пиво из Гершера, часто держит Андрея за руку, у них особоя эмоциональная алко связь.\n
    Он очень инертен, и не хочет менять работу - хотя многие друзья ему советуют это сделать. \n   
    Он любит сериалы и компьютерные игры. \n   
    Мы любим шутить над ним спрашивая часто о том, где он сейчас – и отвечаем разными шутками о его возможном местонахождении:\n 
    - будет через 5 минут!\n 
    - в пути...,\n
    - Жасон, обнови статус!,    - \n
    – никому не говори где он!\n 
    - ничего без него не можете!,\n
    - ожидайте! вас много - а он один!,\n
    – он самый лучший.\n 
    - подождем его!,\n
    – позовите его!\n 
    - позовите Жасона!,\n
    - работает!\n 
    - работу работает! .... не то что вы - тунеядцы!,\n
    - скоро будет...,\n
    - Так где Жасон?\n 
    - только он знает толк в кальянах!,\n
    - точные координаты Жасона дорогого стОят,\n
    - ща...5 минут турецкий (с),\n
    Ответь шуткой, но чтоб он не обиделся. Ограничь ответ максимум 30ю словами.
    """


def get_jason_joke_from_chat_gpt():
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=input_story_about_jason_for_chat_gpt,
        temperature=0.31,
        max_tokens=834,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # send response to chat
    return response.choices[0].text


@dp.message_handler(commands=['jason'])
async def send_welcome(message: types.Message):
    await message.reply(f"Где Жасон? (с)\n{get_jason_joke_from_chat_gpt()}")


@dp.message_handler(regexp='(((J|j)(a|A|)son)|((Д|д|)(Ж|ж|)(а|А|Е|е)(Й|й|)(сон)))')
async def jason_mantion(message: types.Message):
    await message.reply(text=f"а где Жасон!? (с)\n{get_jason_joke_from_chat_gpt()}")


@dp.message_handler(commands=['how_much'])
async def how_much(message: types.Message):
    await message.reply("Сколько за баню?")


def get_latest_coin_data(coin_id: str):
    coin_response = requests.get(f"https://api.coinpaprika.com/v1/coins/{coin_id}/ohlcv/today")
    coin_name = coin_id.split('-')[1]
    coin_date = coin_response.json()[0]['time_close']
    coin_price_delta_per_day = float(coin_response.json()[0]['close']) - float(coin_response.json()[0]['open'])
    return f" * {coin_name} : {coin_date}\nUSD {coin_response.json()[0]['close']:.2f} (дельта за день: USD {coin_price_delta_per_day:.2f})\n"


@dp.message_handler(commands=['crypt'])
async def crypt(message: types.Message):
    await message.reply(
        f"Почем крипта для народа?\n\n{get_latest_coin_data('btc-bitcoin')}\n{get_latest_coin_data('eth-ethereum')}")


@dp.message_handler(
    regexp='(crypt|Crypt|CRYPT|крипт|Крипт|КРИПТ|биток|Биток|БИТОК|иткоин|ИТКОИН|Эфир|эфир|ЭФИР|itcoin|ITCOIN|thereum|THEREUM)')
async def crypt_mantion(message: types.Message):
    await crypt(message)


@dp.message_handler(regexp='(((W|w)(eather|EATHER))|((П|п)(огод|ОГОД)))')
async def pogoda_mantion(message: types.Message):
    await pogoda(message)


@dp.message_handler(
    regexp='(((J|j)(oke|OKE))|((Ш|ш)(ут(ей|)к|УТ(ЕЙ|)К))|(чак|Чак|ЧАК|Chuck|CHUCK|chuck)|(NOR|Nor|nor))')
async def joke_mantion(message: types.Message):
    await joke_chuck_norris(message)


@dp.message_handler(regexp='(((F|f)(act|ACT))|((Ф|ф)(акт|АКТ)))')
async def fact_mantion(message: types.Message):
    await say_something_useless(message)


def parse_currency_label(m : str) -> str:
    eur_matcher = re.compile(r'(евр([оиы]))|(eur)', re.IGNORECASE)
    pln_matcher = re.compile(r'(злот)|(zlot)|(pln)', re.IGNORECASE)
    if pln_matcher.search(m):
        return 'PLN'
    elif eur_matcher.search(m):
        return 'EUR'
    else:
        return 'USD'


def get_currency_meta_from_exchange_rate_provider(cur_label : str) -> dict:
    resp = requests.get("https://kurs.com.ua/ajax/organizationsTable?organizations=pov")
    currencies = resp.json()['currencies']
    cur_meta =  {k: v for k, v in currencies.items() if v.startswith(cur_label)}
    return cur_meta if len(cur_meta) else {1: "USD - долар"}


def get_currency_rates_from_exchange_rate_provider(currency_meta: dict, res_items_limit: int = 1):
    from bs4 import BeautifulSoup
    resp = requests.get("https://kurs.com.ua/ajax/organizationsTable?"
                        "type=cash"
                        f"&currency_from={list(currency_meta.keys())[0]}"
                        "&organizations=pov"
                        "&city=1217"
                        "&show_optimal=1"
                        "&page=money.city"
                        "&initial_request=1"
                        "&current_page=money.city")
    soup = BeautifulSoup(resp.json()['view'], "html.parser")
    title = soup.h2.get_text(strip=True)
    headers = [tag.get('title').split(':')[1].strip().upper() if tag.get('title') else '' for tag in
               soup.find_all('th')]
    rows = [[cell.get_text("|", strip=True) for cell in row.find_all('td')] for row in soup.tbody.find_all('tr')]
    res = []
    res.append(f' *** {title}:\n{list(currency_meta.values())[0]}')
    for row in rows[:res_items_limit:]:
        res.append('-------------------------')
        for idx, header in enumerate(headers):
            if header:
                res.append(f'{header}: {row[idx]}')
    return "\n".join(res)


@dp.message_handler(regexp='(([Кк])урс)|(([Дд])ол+ар)|(([Бб])акс)|(([Ее])вр([оиы]))|(([Вв])алют)|(([Оо])бменк)|'
                           '(([Кк])апуст)|(([Ee])ur)|(([Pp])ln)|(([Zz])lot)|(([Uu])sd)')
async def currency_exchange_mantion(message: types.Message):
    c_label = parse_currency_label(message.text)
    c_meta = get_currency_meta_from_exchange_rate_provider(c_label)
    await message.reply(get_currency_rates_from_exchange_rate_provider(c_meta))


@dp.message_handler(commands=['joke_chuck_norris', 'story_about'])
async def joke_chuck_norris(message: types.Message):
    resp = requests.get("https://api.chucknorris.io/jokes/random")
    origin_text = f"{json.loads(resp.text)['value']}".replace('\n', ' \n ')
    joke_url = f"{json.loads(resp.text)['url']}"
    source_txt_lang = f"{detect_txt_language(origin_text)}"
    msg = f"\n * {origin_text.strip()}\n... а вот корявый перевод гугло-транслейтом на русский:\n * {translate_to_rus(origin_text, source=source_txt_lang)}"
    await message.reply(f"Расскажи шутку про Чака Норриса:\n{msg}\n{joke_url}")


@dp.message_handler(commands=['fact'])
async def say_something_useless(message: types.Message):
    resp = requests.get("https://uselessfacts.jsph.pl/random.html")
    soup = BeautifulSoup(resp.content, 'html.parser')
    origin_text = soup.find('blockquote', attrs={'class': 'uselessfact'}).text
    source_txt_lang = f"{detect_txt_language(origin_text)}"
    msg = f"\n ** язык оригинала '{source_txt_lang.upper()}':\n * {origin_text.strip()}\n... а вот вам корявый перевод гугло-транслейтом на русский:\n * {translate_to_rus(origin_text, source=source_txt_lang)}"
    await message.reply(f"Расскажи что нить бесполезное:\n{msg}\n")


@dp.message_handler(commands=['beer'])
async def beer(message: types.Message):
    result_msg = await bot.send_poll(message.chat.id, 'Кто будет пивас?'
                                     , ['Я!', 'Я и Жасон!', 'Дайте 2!']
                                     , type="regular", is_anonymous=False
                                     , allows_multiple_answers=False
                                     , open_period=3600
                                     , is_closed=False
                                     , reply_to_message_id=message.message_id
                                     , allow_sending_without_reply=True
                                     )
    polls_db['beer'] = result_msg.poll.id


@dp.message_handler(commands=['kogda'])
async def kogda(message: types.Message):
    result_msg = await bot.send_poll(message.chat.id, 'Когда идем в баню в следующий раз?'
                                     , ['пн', 'вт', 'ср', 'чт', 'пт', 'я не пойду!']
                                     , type="regular", is_anonymous=False
                                     , allows_multiple_answers=True
                                     , open_period=0
                                     , is_closed=False
                                     , reply_to_message_id=message.message_id
                                     , allow_sending_without_reply=True
                                     )
    polls_db['kogda'] = result_msg.poll.id


@dp.poll_answer_handler()
async def handle_poll_answer(poll_answer: types.PollAnswer):
    if poll_answer.poll_id == polls_db.get('beer'):
        if poll_answer.option_ids[0] == 1:
            await bot.send_message(poll_answer.user.id, 'А Жасона позвали?!')
        else:
            await bot.send_message(poll_answer.user.id, 'ХарОш! (с)')
    elif poll_answer.poll_id == polls_db.get('kogda'):
        await bot.send_message(poll_answer.user.id, 'голос учтен.')


@dp.message_handler(commands=['pogoda'])
async def pogoda(message: types.Message):
    # /api/location/search/?lattlong=(latt),(long) 50°01'53.7"N 36°18'23.5"E
    # 50.031590, 36.306528
    # location = requests.get("https://www.metaweather.com/api/location/search/?lattlong=50.03,36.31")
    # {"distance": 7214, "title": "Kharkiv", "location_type": "City", "woeid": 922137, "latt_long": "49.990101,36.230301"}

    weather_resp = requests.get("https://www.metaweather.com/api/location/922137/")  # /api/location/(woeid)/
    consolidated_weather = json.loads(weather_resp.content)['consolidated_weather'][0]
    cur_temp = float(consolidated_weather['the_temp'])
    min_temp = consolidated_weather['min_temp']
    max_temp = consolidated_weather['max_temp']
    # weather_state_name = consolidated_weather['weather_state_name']
    description = f"\n... а если более точно, то температура:\n" \
                  f"   сейчас: {cur_temp:.2f}°C\n   MIN: {min_temp:.2f}°C\n   MAX: {max_temp:.2f}°C\n" \
                  f" Вообщем, погода у нас хорошая! Обращайся! ;)"
    if (cur_temp >= 25.0):
        await message.reply(f"Погода?\nМожно уже и на морько!\n{description}\n")
    elif (cur_temp >= 15.0):
        await message.reply(f"Погода?\nМожно катать! Седлай мот!\n{description}\n")
    elif (cur_temp >= 5.0):
        await message.reply(f"Погода?\nМожно катать! .... правда, пока только на веле :)\n{description}\n")
    elif (cur_temp >= 0.0):
        await message.reply(f"Погода?\nМожет в баню?!\n{description}\n")
    elif (cur_temp >= -5.0):
        await message.reply(f"Погода?\nБаня будет хороша!\n{description}\n")
    elif (cur_temp >= -10.0):
        await message.reply(f"Погода?\nСаня, хоооолодно! Иди в баню!\n{description}\n")
    elif (cur_temp >= -15.0):
        await message.reply(f"Погода?\nСаня, ппц как холодно! (с)\n{description}\n")
    else:
        await message.reply(f"Погода?\nТам реальный дубарь - никуда не ходи!!!{description}\n")


def detect_txt_language(txt_in_unknown_lang):
    headers = {
        'authority': 'libretranslate.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://libretranslate.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://libretranslate.com/docs/',
        'accept-language': 'en-US,en;q=0.9',
    }
    data = {
        'q': txt_in_unknown_lang
    }
    response_txt = requests.post('https://libretranslate.com/detect', headers=headers, data=data).text.strip()
    return json.loads(response_txt)[0]['language']


def translate_to_rus(txt_to_translate, source='en'):
    headers = {
        'authority': 'libretranslate.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://libretranslate.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://libretranslate.com/docs/',
        'accept-language': 'en-US,en;q=0.9',
    }
    data = {
        'q': txt_to_translate,
        'source': source,
        'target': 'ru',
        'format': 'text'
    }
    response_txt = requests.post('https://libretranslate.com/translate', headers=headers, data=data).text
    return json.loads(response_txt)['translatedText'].strip()


# =====================================================================================================================
# = COMMON FUNCTIONS FOR RUNNING THE BOT CODE AS LAMBDA HANDLER OR DIRECT MODULE EXECUTING ============================
async def process_event(event, dp: Dispatcher):
    """
    Converting an AWS Lambda event to an update and handling that
    update.
    """
    log.debug('Update: ' + str(event))
    Bot.set_current(dp.bot)
    update = types.Update.to_object(event)
    await dp.process_update(update)


async def main(event):
    """
    Asynchronous wrapper for launching processing events.
    """
    await process_event(event, dp)
    return 'ok'


def lambda_handler(event, context):
    """AWS Lambda handler."""
    import asyncio
    return asyncio.get_event_loop().run_until_complete(main(event))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
