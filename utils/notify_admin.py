import logging
from datetime import datetime

from loader import dp
from data.config import ADMIN
from .weather import get_weather
from .exchange_rates import get_rates


async def on_startup_notify():
    try:
        await dp.bot.send_message(chat_id=ADMIN, text='Bot started')
    except Exception as e:
        logging.exception(e)


async def everyday_broadcast():
    try:
        weather_text = await get_weather('Актау')
        rates = await get_rates()
        text = f'Дайджест на <b>{datetime.now().strftime("%d.%m.%Y")}</b>\n\n' \
               f'{weather_text}\n\n' \
               f'{rates}'
        await dp.bot.send_message(chat_id=ADMIN, text=text)
    except Exception as e:
        logging.exception(e)
