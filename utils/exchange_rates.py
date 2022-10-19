import aiohttp

from data import config


async def get_rates() -> str:
    url = f'https://v6.exchangerate-api.com/v6/{config.EXCHANGERATE_TOKEN}/latest/RUB'
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as resp:
            resp = await resp.json()
    rates = resp['conversion_rates']
    return f'KZT: {rates["KZT"]:.2f} | USD: {1 / rates["USD"]:.2f} | EUR: {1 / rates["EUR"]:.2f}'
