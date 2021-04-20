import json

from flask import Flask, request
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)

player_class = {
    'w_knight': {
        'name': 'Рыцарь',
        'img': '1521359/3157da3180aa703e088b'
    },
    'b_knight': {
        'name': 'Рыцарь',
        'img': '965417/fa9468b3f67b8ace8e17'
    }
}

enemy_class = {
    'bandit': {
        'name': 'Бандит',
        'img': '1030494/b4f5e0cdce81031f659c'
    },
    'fat_robber': {
        'name': 'Толстяк',
        'img': '1652229/cb3d50939c01643cc705'
    },
    'angry_wizard': {
        'name': 'Злой Маг',
        'img': '1652229/674668c85fb558ed011b'
    }
}


friends_class = {
    'b_priest': {
        'name': 'Священник',
        'img': '1521359/7ec168b22eeb821aa28c'
    },
    'w_priest': {
        'name': 'Священник',
        'img': '1521359/f9a2a14661eae47597d9'
    },
    'good_wizard': {
        'name': 'Злой Маг',
        'img': '965417/036a076c5d1157cc6a9e'
    },
    'redneck': {
        'name': 'Деревенщина',
        'img': '965417/e86a9455c5837840e33a'
    },
    'mother': {
        'name': 'Мать',
        'img': '1652229/e01096683abb63095bb7'
    }
}


def change_class(user_id, req, res):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            if name := entity['value'].get('first_name'):
                name = name.capitalize()
                session_state[user_id]['first_name'] = name
                res['response']['text'] = f"Я рад что ты вернулся, {name}, выбери своё новое обличие"
                res['response']['card'] = {
                    'type': 'ItemsList',
                    'header': {
                        'text': f"Я рад что ты вернулся, {name}, выбери своё новое обличие"
                    },
                    'items': [
                        {
                            'image_id': player_class['w_knight']['img'],
                            'title': player_class['w_knight']['name'],
                            'description': "Я хочу быть им",
                            'button': {
                                'text': 'Выбрать героя',
                                'payload': {
                                    'class': 'w_knight'
                                }
                                    }
                        },
                        {
                            'image_id': player_class['b_knight']['img'],
                            'title': player_class['b_knight']['name'],
                            'description': "Я хочу быть им",
                            'button': {
                                'text': 'Выбрать героя',
                                'payload': {
                                    'class': 'b_knight'
                                }
                            }
                        }
                    ],
                    'footer': {
                        'text': 'Выбор только один...'
                    }
                }
                session_state[user_id] = {
                    'state': 2
                }
                return
        else:
            res['response']['text'] = 'Не блефуй! Назови настоящее имя, воин!'

def go_adventure(user_id, req, res):
    try:
        selected_class = req['request']['payload']['class']
    except KeyError:
        res['response']['text'] = 'Пока не выберешь своё обличие, не сможешь вернуться в наш мир'
        return
    session_state[user_id].update({
        'class': selected_class,
        'state': 3
    })
    res['response'] = {
        'text': f"{selected_class.capitalize} - Ха, что за слабака ты выбрал?! Ладно, сойдёт...",
        'card': {
            'type': 'BigImage',
            'image_id': player_class[selected_class]['img'],
            'title': f"{selected_class.capitalize} - Ха, что за слабака ты выбрал?! Ладно, сойдёт..."
        },
        'buttons':[
            {
                "title": "Не надо никаких разговоров. Пошли воевать!!!",
                "payload": {'fight': True},
                "hide": True
            },
            {
                "title": "Что со мной произошло?",
                "hide": True
            },
            {
                "title": "Кто ты такой?",
                "hide": True
            }
        ]
    }
    if req['request']['original_utterance'] == "Что со мной произошло?":
        res['response'] = {
            'text': f"Ты был великим и могучим рыцарем нашего государства. Именно тебя называли героем Орррска"
                    f"Именно ты поймал Злого Орка и усадил его в темницу",
                    f"Мир был на нашей земле окола 1000 лет, пока из тени не вышел он..."
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['b_priest']['img'],
                'title': friends_class['b_priest']['name']
                    },
            'buttons':[
                {
                    "title": "А кто он?",
                    "hide": True
                },
                {
                    "title": "И как я возродился?",
                    "hide": True
                }
            ]
        }
        if req['request']['original_utterance'] == "А кто он?":
            res['response'] = {
                'text': f"Тёмный Маг... Он был правой рукой Злого Орка,"
                        f"а теперь решил возглавить всю его паршивую армию"
                        f"и вернуть своего лидера. И я должен сказать, что это у него почти получилось..."
                        f"В общем-то, поэтому ты и сдесь."
                        f"Я Священник... Один из немногих, кто до сих пор сопротивляется..."
                        f"У нас есть свой лидер - Добрый Маг! Именно благодаря нему ты сдесь.",
                'card': {
                    'type': 'BigImage',
                    'image_id': friends_class['b_priest']['img'],
                    'title': friends_class['b_priest']['name']
                },
            'buttons':[
                {
                    "title": "Кажется, я начинаю припоминать свою прошлую жизнь. Отведи меня к нему!",
                    "hide": True
                    }
                ]
            }
        elif req['request']['original_utterance'] == "И как я возродился?":
            res['response'] = {
                'text': f"Тебя возродил Добрый Маг. Это наш предводитель. Предводитель полследнего лагеря "
                        f"сопротивления, который воюет против Тёмного Мага",
                'card': {
                    'type': 'BigImage',
                    'image_id': friends_class['b_priest']['img'],
                    'title': friends_class['b_priest']['name']
                },
                'buttons': [
                    {
                        "title": "Кажется, я начинаю припоминать свою прошлую жизнь. Отведи меня к нему!",
                        "hide": True
                    }
                ]
            }
    elif req['request']['original_utterance'] == "Кто ты такой?":
        res['response'] = {
            'text': f"Я Священник... Один из немногих, кто до сих пор сопротивляется..."
                    f"Мы последний лагерь, который ещё не поработил Тёмный Маг..."
                    f"Я думаю, тебе стоит сходить к Доброму Магу, он всё расскажет",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['b_priest']['img'],
                'title': friends_class['b_priest']['name']
                    },
            'buttons': [
                {
                    "title": "Так отведи меня к нему!",
                    "hide": True
                }
            ]
        }


def fight(user_id, req, res):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        res['response']['text'] = 'Не стой на месте. Пора идти в бой!'
        return

    if answer:
        enemy1 = enemy_class['bandit']
        enemy2 = enemy_class['fat_robber']
        enemy3 = enemy_class['angry_wizard']


def end_game(user_id, req, res):
    pass


@app.route('\post', methods=['POST'])
def get_alice_request():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Приветствую тебя, душа странника! Назови своё имя'
        session_state[user_id] = {
            'state': 1,

        }
        return
    states[session_state[user_id]['state']](user_id, req, res)


states = {
    1: change_class,
    2: go_adventure,
    3: fight,
    4: end_game
}
session_state = {

}

if __name__ == '__main__':
    app.run()