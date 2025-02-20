from io import BytesIO
import requests
from PIL import Image


def get_map(z):
    server = "https://static-maps.yandex.ru/v1"
    params = {
        "apikey": "8031deff-226c-47c1-a820-90a4d2fd217c",
        "ll": "37.620070,55.753630",
        "z": str(z)
    }

    response = requests.get(server, params=params)

    if "200" in str(response):
        im = BytesIO(response.content)
        opened_image = Image.open(im)
        opened_image.save("map.png")

    return "200" in str(response)


if __name__ == "__main__":
    print(get_map(20))
