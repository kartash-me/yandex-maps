import requests

from io import BytesIO
from PIL import Image


def get_map(z, longitude, latitude, theme):
    server = "https://static-maps.yandex.ru/v1"
    params = {
        "apikey": "8031deff-226c-47c1-a820-90a4d2fd217c",
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
