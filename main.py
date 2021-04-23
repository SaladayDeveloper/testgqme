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

enemy_class = [
    {'name': 'Бандит', 'img': '1030494/b4f5e0cdce81031f659c'},
    {'name': 'Толстяк', 'img': '1652229/cb3d50939c01643cc705'},
    {'name': 'Злой Маг', 'img': '1652229/674668c85fb558ed011b'},
    {'name': 'Шпана', 'img': '965417/5cb25033fc74a80240e7'},
    {'name': 'Лучник', 'img': '1521359/c5088cff3ee05a17d3a6'},
    {'name': 'Панк', 'img': '1030494/8aa9af21e99fbf43f51b'},
    {'name': 'Воин', 'img': '1030494/dd8ac1abb56b7e5a3fb1'}
]

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
        'name': 'Добрый Маг',
        'img': '965417/036a076c5d1157cc6a9e'
    },
    'redneck': {
        'name': 'Деревенщина',
        'img': '965417/e86a9455c5837840e33a'
    },
    'сommander': {
        'name': 'Командир',
        'img': '965417/e3f0c8562cd8e2e53a3d'
    },
    'mother': {
        'name': 'Мать',
        'img': '1652229/e01096683abb63095bb7'
    }
}


def change_class(user_id, req, res):
    if session_state[user_id]['first_name'] == None:
        names = 'кирилл'
        for entity in req['request']['nlu']['entities']:
            if entity['type'] == 'YANDEX.FIO':
                if names == 'кирилл':
                    name = names.capitalize()
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
                                'description': "Я буду им"
                            },
                            {
                                'image_id': player_class['b_knight']['img'],
                                'title': player_class['b_knight']['name'],
                                'description': "Я хочу быть им",
                            }
                        ],
                        'footer': {
                            'text': 'Выбор только один...'
                        }
                    }
                    res['response']['buttons'] = [
                        {
                            'title': 'Да',
                            "payload": {'class': 'w_knight'},
                            'hide': True
                        },
                        {
                            'title': 'Нет',
                            "payload": {'class': 'b_knight'},
                            'hide': True
                        }
                    ]
                return
        else:
            res['response']['text'] = 'Не блефуй! Назови настоящее имя, воин!'
    else:
        try:
            selected_class = req['request']['payload']['class']
            session_state[user_id]['class'] = selected_class
            session_state[user_id]['state'] = 2
            go_adventure(user_id, req, res)
        except KeyError:
            res['response']['text'] = 'Пока не выберешь своё обличие, не сможешь вернуться в наш мир'
            return


def go_adventure(user_id, req, res):
    if 'original_utterance' not in req['request']:
        res['response'] = {
            'text': f"Ха, что за слабака ты выбрал?! Ладно, сойдёт...",
            'card': {
                'type': 'BigImage',
                'image_id': player_class[session_state[user_id]['class']]['img'],
                'title': f"Ха, что за слабака ты выбрал?! Ладно, сойдёт..."
            },
            'buttons': [
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
        return
    if req['request']['original_utterance'] == "Что со мной произошло?":
        res['response'] = {
            'text': f"Ты был героем Орррска. "
                    f"Именно ты поймал Злого Орка и усадил его в темницу. "
                    f"Всё было хорошо, пока не вышел он...",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['b_priest']['img'],
                'title': f"Ты был героем Орррска. "
                    f"Именно ты поймал Злого Орка и усадил его в темницу. "
                    f"Всё было хорошо, пока не вышел он..."
            },
            'buttons': [
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
    elif req['request']['original_utterance'] == "Кто ты такой?":
        res['response'] = {
            'text': f"Я Священник... Один из немногих, кто до сих пор сопротивляется... "
                    f"Мы - последний лагерь, который ещё не поработил Тёмный Маг...",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['b_priest']['img'],
                'title': f"Я Священник... Один из немногих, кто до сих пор сопротивляется... "
                    f"Мы - последний лагерь, который ещё не поработил Тёмный Маг..."
            },
            'buttons': [
                {
                    "title": "И как я тут оказался?",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "И как я тут оказался?":
        res['response'] = {
            'text': f"Тебя возродил Добрый Маг. Грядёт очень важная битва, мы не справимся без тебя. "
                    f"Тебе стоит узнать всё у него самого",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['b_priest']['img'],
                'title': f"Тебя возродил Добрый Маг. Грядёт очень важная битва, мы не справимся без тебя. "
                        f"Тебе стоит узнать всё у него самого"
            },
            'buttons': [
                {
                    "title": "Но подожди... Кто я?",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Но подожди... Кто я?":
        res['response'] = {
            'text': f"Ты тот, кто убил лидера Тёмного Мага "
                    f"Ты тот, кто должен убить Тёмного Мага...",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['b_priest']['img'],
                'title': f"Ты тот, кто убил лидера Тёмного Мага... "
                    f"Ты тот, кто должен убить Тёмного Мага..."
            },
            'buttons': [
                {
                    "title": "Кажется, я вспоминаю свою прошлую жизнь. Отведи меня к нему!",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "А кто он?":
        res['response'] = {
            'text': f"Тёмный Маг... Он был правой рукой Злого Орка, "
                    f"а теперь решил возглавить всю его паршивую армию "
                    f"и вернуть своего лидера!",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['b_priest']['img'],
                'title': f"Тёмный Маг... Он был правой рукой Злого Орка, "
                        f"а теперь решил возглавить всю его паршивую армию "
                        f"и вернуть своего лидера!"
            },
            'buttons': [
                {
                    "title": "А что ты от меня-то хочешь?",
                    "hide": True
                },
                {
                    "title": "Чего мы ждём? Что мне делать?",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "И как я возродился?":
        res['response'] = {
            'text': f"Тебя возродил Добрый Маг. Грядёт очень важная битва, мы не справимся без тебя. "
                    f"Тебе стоит узнать всё у него самого",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['b_priest']['img'],
                'title': f"Тебя возродил Добрый Маг. Грядёт очень важная битва, мы не справимся без тебя. "
                        f"Тебе стоит узнать всё у него самого"
            },
            'buttons': [
                {
                    "title": "Кажется, я вспоминаю свою прошлую жизнь. Отведи меня к нему!",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "А что ты от меня-то хочешь?":
        res['response'] = {
            'text': f"Как что?! Нам нужна твоя помощь, иначе последний лагерь сопротивления падёт!",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['b_priest']['img'],
                'title': f"Как что?! Нам нужна твоя помощь, иначе последний лагерь сопротивления падёт!"
            },
            'buttons': [
                {
                    "title": f"Ну да, глупый вопрос:) Ладно, я помогу вам, что делать?",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Чего мы ждём? Что мне делать?" or \
            req['request']['original_utterance'] == "Ну да, глупый вопрос:) Ладно, я помогу вам, что делать?":
        res['response'] = {
            'text': f"Тебе надо сходить к Доброму Магу, он всё расскажет...",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['b_priest']['img'],
                'title': f"Тебе надо сходить к Доброму Магу, он всё расскажет..."
            },
            'buttons': [
                {
                    "title": f"Так отведи меня к нему!",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Так отведи меня к нему!" or \
            req['request']['original_utterance'] == "Кажется, я вспоминаю свою прошлую жизнь. Отведи меня к нему!":
        res['response'] = {
            'text': f"Священник указал тебе палату, в которой сидел Добрый Маг. Ты пошёл "
                    f"и по пути встретил Деревенщину",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['redneck']['img'],
                'title': f"Священник указал тебе палату, в которой сидел Добрый Маг. Ты пошёл "
                        f"и по пути встретил Деревенщину"
            },
            'buttons': [
                {
                    "title": "Подойти и поприветствовать",
                    "hide": True
                },
                {
                    "title": "Пройти мимо",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Подойти и поприветствовать":
        res['response'] = {
            'text': f"Э-гэ-гэй, привет странник. Чего требуется от меня?",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['redneck']['img'],
                'title': f"Э-гэ-гэй, привет странник. Чего требуется от меня?"
            },
            'buttons': [
                {
                    "title": "Какой я тебе странник!!! Я великий и могучий рыцарь Орррска!",
                    "hide": True
                },
                {
                    "title": "А как ты-то сюда попал?",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Пройти мимо":
        res['response'] = {
            'text': f"Проходя Деревенщину, ты случайно спотыкаешься об камень и падаешь. "
                    f"Тебя поднимает мимо идущая женщина.",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['mother']['img'],
                'title': f"Проходя Деревенщину, ты случайно спотыкаешься об камень и падаешь. "
                        f"Тебя поднимает мимо идущая женщина."
            },
            'buttons': [
                {
                    "title": "Кто вы такая?",
                    "hide": True
                },
                {
                    "title": "Эй, уйди от меня!",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Кто вы такая?":
        res['response'] = {
            'text': f"Обратив внимание на лицо девушки, в ваших глазах вдруг потемнело "
                    f"Она напомнила вам вашу мать",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['mother']['img'],
                'title': f"Обратив внимание на лицо девушки, в ваших глазах вдруг потемнело "
                    f"Она напомнила вам вашу мать"
            },
            'buttons': [
                {
                    "title": "Мама?",
                    "hide": True
                },
                {
                    "title": "Папа?",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Эй, уйди от меня!":
        res['response'] = {
            'text': f"Пройдя ещё немного вперёд, вы пришли к палатке Доброго Мага",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['mother']['img'],
                'title': f"Пройдя ещё немного вперёд, вы пришли к палатке Доброго Мага"
            },
            'buttons': [
                {
                    "title": "Войти",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Мама?":
        res['response'] = {
            'text': f"Она посмотрела на тебя и бархатным голоском произнесла: "
                    f"Я верю в тебя, сынок!",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['mother']['img'],
                'title': f"Она посмотрела на тебя и бархатным голоском произнесла: "
                    f"Я верю в тебя, сынок!"
            },
            'buttons': [
                {
                    "title": "Мама стой!",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Папа?":
        res['response'] = {
            'text': f'"Ты что, дурак?" - произнесла девушка и шлёпнула вас по щеке',
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['mother']['img'],
                'title': f'"Ты что, дурак?" - произнесла девушка и шлёпнула вас по щеке'
            },
            'buttons': [
                {
                    "title": "Извините, я что-то попутал",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Мама стой!":
        res['response'] = {
            'text': f"После этих слов она словно испарилась. "
                    f"Ты прошёл ещё немного и оказался у палатки Доброго Мага",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['mother']['img'],
                'title': f"После этих слов она словно испарилась. "
                         f"Ты прошёл ещё немного и оказался у палатки Доброго Мага"
            },
            'buttons': [
                {
                    "title": "Войти",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Извините, я что-то попутал":
        res['response'] = {
            'text': f"Девушка ушла. Пройдя ещё немного, ты оказался у палатки Доброго Мага",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['mother']['img'],
                'title': f"Девушка ушла. Пройдя ещё немного, ты оказался у палатки Доброго Мага"
            },
            'buttons': [
                {
                    "title": "Войти",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "А как ты-то сюда попал?":
        res['response'] = {
            'text': f"Понимаешь, дружище... Не могу я жить там, где меня за раба принимают "
                    f"У меня ведь семья, дети. Не хочу я рабом быть!",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['redneck']['img'],
                'title': f"Понимаешь, дружище... Не могу я жить там, где меня за раба принимают "
                    f"У меня ведь семья, дети. Не хочу я рабом быть!",
            },
            'buttons': [
                {
                    "title": "...",
                    "hide": True
                },
            ]
        }
    elif req['request']['original_utterance'] == "Какой я тебе странник!!!" \
                                                 " Я великий и могучий рыцарь Орррска!":
        res['response'] = {
            'text': f"Ой-ой!!! Извините меня, господин...",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['redneck']['img'],
                'title': f"Ой-ой!!! Извините меня, господин..."
            },
            'buttons': [
                {
                    "title": "Уйти, бормоча себе что-то под нос",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "...":
        res['response'] = {
            'text': f"Ненавижу я Тёмного Мага, нет в нём ничего святого. Я лучше умру в битве с ним, "
                    f"чем служить ему буду. А ты кто сам, странник?",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['redneck']['img'],
                'title': f"Ненавижу я Тёмного Мага, нет в нём ничего святого. Я лучше умру в битве с ним, "
                        f"чем служить ему буду. А ты кто сам, странник?"
            },
            'buttons': [
                {
                    "title": "Какой я тебе странник!!! Я великий и могучий рыцарь Орррска!",
                    "hide": True
                },
                {
                    "title": "Не твоё собачье дело!",
                    "hide": True
                },
            ]
        }
    if req['request']['original_utterance'] == "Какой я тебе странник!!! Я великий и могучий рыцарь Орррска!":
        res['response'] = {
            'text': f"Ой, простите меня господин... Получается, вы пришли сюда чтобы покончить "
                    f"с Тёмным Магом. Слава рыцарю, господи!!! Слава!",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['redneck']['img'],
                'title': f"Ой, простите меня господин... Получается, вы пришли сюда чтобы покончить "
                    f"с Тёмным Магом. Слава рыцарю, господи!!! Слава!"
            },
            'buttons': [
                {
                    "title": 'Уйти со словами: "Я помогу тебе, мужик! Не волнуйся!"',
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Не твоё собачье дело!":
        res['response'] = {
            'text': f"Извините...",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['redneck']['img'],
                'title': f"Извините..."
            },
            'buttons': [
                {
                    "title": "Уйти, бормоча себе что-то под нос",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Уйти, бормоча себе что-то под нос" or \
            req['request']['original_utterance'] == 'Уйти со словами: "Я помогу тебе, мужик! Не волнуйся!"':
        res['response'] = {
            'text': f"Ты идёшь прямо и вдруг встречаешь на своём пути женщину."
                    f"Она очень похожа на твою маму",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['mother']['img'],
                'title': f"Ты идёшь прямо и вдруг встречаешь на своём пути женщину."
                        f"Она очень похожа на твою маму"
            },
            'buttons': [
                {
                    "title": "Женщина, кто вы такая?",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Женщина, кто вы такая?":
        res['response'] = {
            'text': f"Она, улыбаясь, машет вам",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['mother']['img'],
                'title': f"Она, улыбаясь, машет вам"
            },
            'buttons': [
                {
                    "title": "Мама, это ты?",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Мама, это ты?":
        res['response'] = {
            'text': f"Вдруг она исчезла. Что это было, ты не понял. Пройдя ещё немного "
                    f"ты оказался у палатки Доброго Мага",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['mother']['img'],
                'title': f"Вдруг она исчезла. Что это было, ты не понял. Пройдя ещё немного "
                    f"ты оказался у палатки Доброго Мага"
            },
            'buttons': [
                {
                    "title": "Войти",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Войти":
        res['response'] = {
            'text': f"Я ждал тебя...",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['good_wizard']['img'],
                'title': f"Я ждал тебя..."
            },
            'buttons': [
                {
                    "title": "А я наслышан о тебе...",
                    "hide": True
                },
                {
                    "title": "Спасибо за то, что оживили меня. Давно я не чувствовал себя "
                             "таким свободным и живым...",
                    "hide": True
                },
                {
                    "title": "Зачем ты вернул меня к жизни, приспешник?",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "А я наслышан о тебе...":
        res['response'] = {
            'text': f"Мои друзья тебе уже всё рассказали... Так ты поможешь?",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['good_wizard']['img'],
                'title': f"Мои друзья тебе уже всё рассказали... Так ты поможешь?"
            },
            'buttons': [
                {
                    "title": "Думаю, да",
                    "hide": True
                },
                {
                    "title": "Что именно нужно сделать?",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Спасибо за то, что оживили меня. Давно я не чувствовал себя " \
            "таким свободным и живым...":
        res['response'] = {
            'text': f"Я оживил тебя, чтобы ты помог мне в битве с Тёмным Магом...",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['good_wizard']['img'],
                'title': f"Я оживил тебя, чтобы ты помог мне в битве с Тёмным Магом..."
            },
            'buttons': [
                {
                    "title": "Я уничтожу его!",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Зачем ты вернул меня к жизни, приспешник?":
        res['response'] = {
            'text': f"Извини, я не справлюсь один. Я пытался, но он сильнее",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['good_wizard']['img'],
                'title': f"Извини, я не справлюсь один. Я пытался, но он сильнее"
            },
            'buttons': [
                {
                    "title": "Как тебе не стыдно. У нас был уговор!!!",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Думаю, да":
        res['response'] = {
            'text': f"Тут вдруг неожиданно в палатку забегает ещё один рыцарь "
                    f"По его погонам ты понимаешь, что это командир",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['сommander']['img'],
                'title': f"Тут вдруг неожиданно в палатку забегает ещё один рыцарь "
                    f"По его погонам ты понимаешь, что это командир"
            },
            'buttons': [
                {
                    "title": "Вытаращить глаза",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Что именно нужно сделать?":
        res['response'] = {
            'text': f'"У меня есть план..." - Тут вдруг неожиданно в палатку забегает ещё один рыцарь '
                    f"По его погонам ты понимаешь, что это командир",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['сommander']['img'],
                'title': f'"У меня есть план..." - Тут вдруг неожиданно в палатку забегает ещё один рыцарь '
                    f"По его погонам ты понимаешь, что это командир"
            },
            'buttons': [
                {
                    "title": "Вытаращить глаза",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Я уничтожу его!":
        res['response'] = {
            'text': f"Тут вдруг неожиданно в палатку забегает ещё один рыцарь "
                    f"По его погонам ты понимаешь, что это командир",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['сommander']['img'],
                'title': f"Тут вдруг неожиданно в палатку забегает ещё один рыцарь "
                    f"По его погонам ты понимаешь, что это командир"
            },
            'buttons': [
                {
                    "title": "Вытаращить глаза",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Как тебе не стыдно. У нас был уговор!!!":
        res['response'] = {
            'text': f"Я помню... Простите меня, господин",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['good_wizard']['img'],
                'title': f"Я помню... Простите меня, господин"
            },
            'buttons': [
                {
                    "title": "Говори где он, я от него пустого места не оставлю!",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Говори где он, я от него пустого места не оставлю!":
        res['response'] = {
            'text': f"Тут вдруг неожиданно в палатку забегает ещё один рыцарь. "
                    f"По его погонам ты понимаешь, что это командир",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['сommander']['img'],
                'title': f"Тут вдруг неожиданно в палатку забегает ещё один рыцарь. "
                    f"По его погонам ты понимаешь, что это командир"
            },
            'buttons': [
                {
                    "title": "Вытаращить глаза",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Вытаращить глаза":
        res['response'] = {
            'text': f"Они сдесь! ТЁМНЫЙ МАГ СДЕСЬ!!!",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['сommander']['img'],
                'title': f"Они сдесь! ТЁМНЫЙ МАГ СДЕСЬ!!!"
            },
            'buttons': [
                {
                    "title": "Что...",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Что...":
        res['response'] = {
            'text': f'Вы переглянулись с Добрым Магом. "Мы должны!" - сказал он. '
                    f'"Мы должны!" - сказал ты.',
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['good_wizard']['img'],
                'title': f'Вы переглянулись с Добрым Магом. "Мы должны!" - сказал он. '
                    f'"Мы должны!" - сказал ты.'
            },
            'buttons': [
                {
                    "title": "Выйти на улицу",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Выйти на улицу":
        res['response'] = {
            'text': f"Выйдя на улицу, ты увидел его... Весь лагерь горел, а перед тобой "
                    f"появилась толпа противников. Время пришло...",
            'card': {
                'type': 'BigImage',
                'image_id': enemy_class[2]['img'],
                'title': f"Выйдя на улицу, ты увидел его... Весь лагерь горел, а перед тобой "
                    f"появилась толпа противников. Время пришло...",
            },
            'buttons': [
                {
                    "title": "Начать бой",
                    "payload": {'fight': True},
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Начать бой":
        session_state[user_id]['state'] = 3


def fight(user_id, req, res):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        res['response']['text'] = 'Не стой на месте. Пора идти в бой!'
        return
    if answer:
        enemy = enemy_class[0]['name']['img']
        session_state[user_id]['state'] = 4
        res['response'] = {
            'text': f"Ваш противник - {enemy[0]['name']}",
            'card': {
                'type': "BigImage",
                'image_id': enemy['img'],
                'title': f"Ваш противник - {enemy[0]['name']}"
            },
            'buttons': [
                {
                    "title": "Ударить",
                    "payload": {'fight': True},
                    "hide": True
                },
                {
                    "title": "Увернуться",
                    "payload": {'fight': True},
                    "hide": True
                },
                {
                    "title": "Испугаться и убежать",
                    "payload": {'fight': False},
                    "hide": True
                },
            ]
        }
    else:
        end_game(user_id, req, res)


def end_game(user_id, req, res):
    try:
        answer = req['request']['payload']['fight']
    except KeyError:
        res['response']['text'] = f"Ты не можешь просто так уйти..."
        return
    if not answer:
        res['response']['text'] = f"Из-за вашего отказа маг убил вас, посчитав предателем. Поздравляю, вы дурак!"
    else:
        res['response']['text'] = f"Молодец! Ты перебил всех. Маг сделал тебя новым правителем," \
                                  f"А сам стал служить тебе, как и все оставшиеся выжившие из лагеря сопротивления." \
                                  f"Все ликуют!" \
                                  f"Мир снова воцарил в Орррске!"
    res['response']['end_session'] = True


@app.route('/post', methods=['POST'])
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
            'first_name': None
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
