from io import BytesIO
import requests
from PIL import Image

server = "https://static-maps.yandex.ru/v1"
params = {
    "apikey": "8031deff-226c-47c1-a820-90a4d2fd217c",
    "ll": "37.620070,55.753630"
}

response = requests.get(server, params=params)
print(response)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()
