# Приложение Yandex Maps API
_Для запуска проекта потребуется установить Python_

## Активация виртуального окружения
Для создания виртуального окружения и его активации выполните:
```bash
python3 -m venv venv
source venv/bin/activate
```

## Установка зависимостей
Для установки зависимостей выполните:
```bash
pip3 install -r requirements.txt
```

## Настройка переменных окружения
Скопируйте файл `template.env` в `.env`:
```bash
cp template.env .env
```
Если посчитаете нужным, замените общедоступные API-ключи на свои:
+ Подробнее о том, как получить ключ для `Yandex Maps Static API`, можно прочитать
[тут](https://yandex.ru/maps-api/docs/static-api/quickstart.html)
+ Подробнее о том, как получить ключ для `Yandex Maps JavaScript API и HTTP Геокодер`, можно прочитать
[тут](https://yandex.ru/maps-api/docs/geocoder-api/quickstart.html)

## Настройка параметров приложения
Если посчитаете нужным, измените параметры в методе `__init__` класса `Map` в файле `main.py` 

## Запуск
Для запуска проекта выполните:
```bash
python3 main.py
```
