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
cp config.env .env
```
Если посчитаете нужным, замените общедоступный API-ключ на свой.
Подробнее о том, как это сделать, можно прочитать [тут](https://yandex.ru/maps-api/docs/static-api/quickstart.html).

## Запуск
Для запуска проекта выполните:
```bash
python3 main.py
```
