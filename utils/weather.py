import aiohttp

from data import config


async def get_city_coords(city: str) -> str:
    params = {
        'geocode': city,
        'apikey': config.GEO_TOKEN,
        'format': 'json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url='https://geocode-maps.yandex.ru/1.x', params=params) as resp:
            resp = await resp.json()
    return resp['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']


async def get_weather(city: str) -> str:
    coords = await get_city_coords(city=city)
    coords = coords.split()
    params = {'lat': coords[1], 'lon': coords[0], 'lang': 'ru_RU'}
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url='https://api.weather.yandex.ru/v2/forecast',
                params=params,
                headers={'X-Yandex-API-Key': config.WEATHER_TOKEN}) as resp:
            resp = await resp.json()
    fact = resp['fact']
    forecast_day = resp['forecasts'][0]['parts']['day']
    text = f'<b>Погода в городе {city}</b>\n\n' \
           f'<u>Температура:</u> {fact["temp"]} °C, ощущается как: {fact["feels_like"]} °C\n' \
           f'<u>Ветер:</u> {fact["wind_speed"]} м/с. <u>Давление:</u> {fact["pressure_mm"]} мм\n' \
           f'<u>Днем:</u> {forecast_day["temp_avg"]} °C.\n' \
           f'<u>Ветер:</u> {forecast_day["wind_speed"]} м/c. ' \
           f'<u>Давление:</u> {forecast_day["pressure_mm"]} мм.'
    return text