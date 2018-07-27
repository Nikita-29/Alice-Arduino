# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

app = Flask(__name__)

# sudo python3 api.py
# nano api.py


global_flag_open = 0

logging.basicConfig(level=logging.DEBUG)


@app.route('/get_status')
def get_status():
    global global_flag_open
    if global_flag_open==0:
        res='0'
    if global_flag_open==1:
        res='1'
    if global_flag_open==2:
        res='2'
    if global_flag_open==3:
        res='3'
    if global_flag_open==4:
        res='4'
    if global_flag_open==5:
        res='5'
    
    return res


# Хранилище данных о сессиях.
sessionStorage = {}


# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    global global_flag_open

    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Включить режим 1",
                "Включить режим 2",
                "Включить режим 3",
                "Включить режим 4",
                "Включить режим 5",

            ]
        }

        res['response']['text'] = 'Привет!Чем я могу тебе помочь?'
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Обрабатываем ответ пользователя.
    if req['request']['original_utterance'].lower() in [
        'режим 1',
        'включить режим 1',

    ]:
        # Пользователь согласился, прощаемся.
        # здесь отправляем сигнал на Arduino(up)
        res['response']['text'] = 'Режим 1 включен.'
        global_flag_open = 1


    # Если нет, то убеждаем его купить слона!
    elif req['request']['original_utterance'].lower() in [
        'режим 2',
        'включить режим 2',

    ]:
        res['response']['text'] = 'Режим 2 включен'
        global_flag_open = 2

    elif req['request']['original_utterance'].lower() in [
        'режим 3',
        'включить режим 3',

    ]:

        res['response']['text'] = 'Режим 3 включен.'
        global_flag_open = 3

    elif req['request']['original_utterance'].lower() in [
        'режим 4',
        'включить режим 4',

    ]:

        res['response']['text'] = 'Режим 4 включен.'
        global_flag_open = 4

    elif req['request']['original_utterance'].lower() in [
        'режим 5',
        'включить режим 5',

    ]:

        res['response']['text'] = 'Режим 5 включен.'
        global_flag_open = 5

    elif req['request']['original_utterance'].lower() in [
        'режим 0',
        'включить режим 0',

    ]:

        res['response']['text'] = 'Режим 0 включен.'
        global_flag_open = 0

    else:
        res['response']['text'] = 'Я тебя не поняла'

    # res['response']['text'] = 'Все говорят "%s", а ты купи слона!' % (
    # req['request']['original_utterance']
    # )
    res['response']['buttons'] = get_suggests(user_id)


# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    #   suggests.append({
    #       "title": "Ладно",
    #      "url": "https://market.yandex.ru/search?text=слон",
    #     "hide": True
    # })

    return suggests


if __name__ == "__main__":
    app.run(ssl_context='adhoc', host='0.0.0.0', port='443')