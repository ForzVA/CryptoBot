import requests
from extensions import val

class APIException(Exception):
    pass

class CryptoConverter:
    """Как я понял, я нашел API без нужды реализации json, так что
    извиняйте за его отсутствие=)"""
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        quote_abbreviation, base_abbreviation = val[quote], val[base]
        if quote == base:
            raise APIException(f'Введена одна и та же валюта два раза - {base}')

        try:
            quote_abbreviation = val[quote]
        except KeyError:
            raise APIException(f'Не удалось найти валюту {quote}')

        try:
            base_abbreviation = val[base]
        except KeyError:
            raise APIException(f'Не удалось найти валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось посчитать кол-во: {amount}')

        url = "https://currency-exchange.p.rapidapi.com/exchange"
        querystring = {"to": f"{base_abbreviation}", "from": f"{quote_abbreviation}", "q": "1.0"}
        headers = {'x-rapidapi-key': "00cff2fb41msh6579d914666efb1p1c2ebejsne0a1ab450979",
                   'x-rapidapi-host': "currency-exchange.p.rapidapi.com"}
        response = requests.get(url, headers=headers, params=querystring)
        total_base = round(float(amount) *float(response.text), 3)

        return total_base