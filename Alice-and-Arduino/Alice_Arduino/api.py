# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals


import json
import logging


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



sessionStorage = {}



@app.route("/", methods=['POST'])
def main():
    
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



def handle_dialog(req, res):
    global global_flag_open

    user_id = req['session']['user_id']

    if req['session']['new']:
        

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
        'режим один',
        'включить режим один',
        'включи режим один',

    ]:
        # Пользователь согласился, прощаемся.
        # здесь отправляем сигнал на Arduino(up)
        res['response']['text'] = 'Режим 1 включен.'
        global_flag_open = 1


    # Если нет, то убеждаем его купить слона!
    elif req['request']['original_utterance'].lower() in [
        'режим 2',
        'включить режим 2',
        'режим два',
        'включить режим два',
        'включи режим два',


    ]:
        res['response']['text'] = 'Режим 2 включен'
        global_flag_open = 2

    elif req['request']['original_utterance'].lower() in [
        'режим 3',
        'включить режим 3',
        'режим три',
        'включить режим три',
        'включи режим три',


    ]:

        res['response']['text'] = 'Режим 3 включен.'
        global_flag_open = 3

    elif req['request']['original_utterance'].lower() in [
        'режим 4',
        'включить режим 4',
        'режим четыре',
        'включить режим четыре',
        'включи режим четыре',


    ]:

        res['response']['text'] = 'Режим 4 включен.'
        global_flag_open = 4

    elif req['request']['original_utterance'].lower() in [
        'режим 5',
        'включить режим 5',
        'режим пять',
        'включить режим пять',
        'включи режим пять',


    ]:

        res['response']['text'] = 'Режим 5 включен.'
        global_flag_open = 5

    elif req['request']['original_utterance'].lower() in [
        'режим 0',
        'включить режим 0',
        'режим ноль',
        'включить режим ноль',
        'включи режим ноль',


    ]:

        res['response']['text'] = 'Режим 0 включен.'
        global_flag_open = 0

    else:
        res['response']['text'] = 'Я тебя не поняла'

    
    res['response']['buttons'] = get_suggests(user_id)



def get_suggests(user_id):
    session = sessionStorage[user_id]

    
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    
    return suggests


if __name__ == "__main__":
    app.run(ssl_context='adhoc', host='0.0.0.0', port='443')
