import os
import requests

from dotenv import load_dotenv
from io import BytesIO
from PIL import Image


def get_api_key():
    key = os.environ.get("STATIC_MAPS_KEY")

    if key is None:
        if os.path.exists(".env"):
            load_dotenv(".env")
        elif os.path.exists("template.env"):
            load_dotenv("template.env")
        else:
            raise KeyError("Файл .env не найден")

        key = os.environ.get("STATIC_MAPS_KEY")

        if key is None:
            raise KeyError("API-ключ не найден")

    return key


API_KEY = get_api_key()


def get_map(z, longitude, latitude, theme):
    server = "https://static-maps.yandex.ru/v1"
    params = {
        "apikey": API_KEY,
        "ll": f"{longitude},{latitude}",
        "z": str(z),
        "theme": theme
    }

    response = requests.get(server, params=params)
    status = "200" in str(response)

    if status:
        im = BytesIO(response.content)
        opened_image = Image.open(im)
        opened_image.save("map.png")

    return status
