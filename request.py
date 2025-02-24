import os
import requests

from dotenv import load_dotenv
from io import BytesIO
from PIL import Image


def get_api_key(key_name):
    key = os.environ.get(key_name)

    if key is None:
        if os.path.exists(".env"):
            load_dotenv(".env")
        elif os.path.exists("template.env"):
            load_dotenv("template.env")
        else:
            raise KeyError("Файл .env не найден")

        key = os.environ.get(key_name)

        if key is None:
            raise KeyError("API-ключ не найден")

    return key


STATIC_MAPS_KEY = get_api_key("STATIC_MAPS_KEY")
GEOCODE_API_KEY = get_api_key("GEOCODE_API_KEY")


def get_map(z, longitude, latitude, theme, pt):
    server = "https://static-maps.yandex.ru/v1"
    params = {
        "apikey": STATIC_MAPS_KEY,
        "ll": f"{longitude},{latitude}",
        "z": str(z),
        "theme": theme
    }

    if pt:
        params["pt"] = f"{pt[0]},{pt[1]},pm2rdm"

    response = requests.get(server, params=params)

    if response.ok:
        im = BytesIO(response.content)
        Image.open(im).save("map.png")

    return response.ok


def geocode(query):
    geocoder_server = "https://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": GEOCODE_API_KEY,
        "geocode": query,
        "format": "json",
        "lang": "ru_RU"
    }

    try:
        response = requests.get(geocoder_server, params=params)
        response.raise_for_status()

        data = response.json()
        features = data["response"]["GeoObjectCollection"]["featureMember"]

        if not features:
            return None, None, None

        top_result = features[0]["GeoObject"]
        pos = top_result["Point"]["pos"]
        longitude, latitude = map(float, pos.split())

        address = top_result["metaDataProperty"]["GeocoderMetaData"]["text"]

        return longitude, latitude, address

    except Exception as e:
        print(f"Ошибка геокодирования: {e}")
        return None, None, None
