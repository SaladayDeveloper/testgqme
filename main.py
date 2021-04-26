# импортируем библиотеки
import json

from flask import Flask, request

# создаём приложение
# мы передаём __name__, в нем содержится информация,
# в каком модуле мы находимся.
app = Flask(__name__)

# Загружаем два скина для выбора персонажа
player_class = {
    'w_knight': {
        'name': 'Рыцарь',
        'img': '213044/ab0e0e49f00e3eb4032e'
    },
    'b_knight': {
        'name': 'Рыцарь',
        'img': '965417/53c098b89cd26844c3e7'
    }
}

# Загружаем всех врагов
enemy_class = [
    {'name': 'Бандит', 'img': '937455/952cbc400eaa77b7783e'},
    {'name': 'Толстяк', 'img': '213044/bdb2098793bd50e33f24'},
    {'name': 'Злой Маг', 'img': '1521359/ee5330cff89118c8320f'},
    {'name': 'Шпана', 'img': '965417/796f3c199189ca463524'},
    {'name': 'Лучник', 'img': '937455/f7a7d47badea5eece43f'},
    {'name': 'Панк', 'img': '1030494/03133c23fea23c08fdea'},
    {'name': 'Воин', 'img': '1521359/07497b2575374b779bd5'}
]

# Загружаем всех друзей
friends_class = {
    'b_priest': {
        'name': 'Священник',
        'img': '1030494/fa6a0c54e1e4971e6c0d'
    },
    'good_wizard': {
        'name': 'Добрый Маг',
        'img': '213044/d75eea8401b3bd570d71'
    },
    'redneck': {
        'name': 'Деревенщина',
        'img': '997614/82ef7494a778a7ff45fb'
    },
    'сommander': {
        'name': 'Командир',
        'img': '997614/a53fb38d45b9e7285de2'
    },
    'mother': {
        'name': 'Мать',
        'img': '1521359/cb878a879cbdc877dee1'
    }
}


# Функция с выбором персонажа
def change_person(user_id, req, res):
    if session_state[user_id]['first_name'] == None:
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
                            'title': 'Верхний',
                            "payload": {'class': 'w_knight'},
                            'hide': True
                        },
                        {
                            'title': 'Нижний',
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
            res['response']['buttons'] = [
                {
                    'title': 'Верхний',
                    "payload": {'class': 'w_knight'},
                    'hide': True
                },
                {
                    'title': 'Нижний',
                    "payload": {'class': 'b_knight'},
                    'hide': True
                }
            ]
            return


# Функция, в которой описано всё основное приключение
def go_adventure(user_id, req, res):
    if 'original_utterance' not in req['request'] or \
            req['request']['original_utterance'] == "Начать сначала":
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
            'text': f"Обратив внимание на лицо девушки, в ваших глазах вдруг потемнело. "
                    f"Она напомнила вам вашу мать",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['mother']['img'],
                'title': f"Обратив внимание на лицо девушки, в ваших глазах вдруг потемнело. "
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
    elif req['request']['original_utterance'] == "Что именно нужно сделать?":
        res['response'] = {
            'text': f'"У меня есть план..." - Тут вдруг неожиданно в палатку забегает ещё один рыцарь. '
                    f"По его погонам ты понимаешь, что это командир",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['сommander']['img'],
                'title': f'"У меня есть план..." - Тут вдруг неожиданно в палатку забегает ещё один рыцарь. '
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
            'text': f"Они здесь! ТЁМНЫЙ МАГ ЗДЕСЬ!!!",
            'card': {
                'type': 'BigImage',
                'image_id': friends_class['сommander']['img'],
                'title': f"Они здесь! ТЁМНЫЙ МАГ ЗДЕСЬ!!!"
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
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Начать бой" or \
            req['request']['original_utterance'] == "Начать бой сначала":
        res['response'] = {
            'text': f"Ваш противник - {enemy_class[3]['name']}",
            'card': {
                'type': "BigImage",
                'image_id': enemy_class[3]['img'],
                'title': f"Ваш противник - {enemy_class[3]['name']}"
            },
            'buttons': [
                {
                    "title": "Ударить",
                    "hide": True
                },
                {
                    "title": "Увернуться",
                    "hide": True
                },
                {
                    "title": "Испугаться и убежать",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Ударить":
        res['response'] = {
            'text': f"{enemy_class[3]['name']} повержена",
            'card': {
                'type': "BigImage",
                'image_id': enemy_class[3]['img'],
                'title': f"{enemy_class[3]['name']} повержена"
            },
            'buttons': [
                {
                    "title": "Следующий враг",
                    "hide": True
                },
                {
                    "title": "Испугаться и убежать",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Увернуться":
        res['response'] = {
            'text': f"Вы увернулись и уклонились от удара",
            'card': {
                'type': "BigImage",
                'image_id': enemy_class[3]['img'],
                'title': f"Вы увернулись и уклонились от удара"
            },
            'buttons': [
                {
                    "title": "Ударить",
                    "hide": True
                },
                {
                    "title": "Испугаться и убежать",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Следующий враг":
        res['response'] = {
            'text': f"Ваш противник - {enemy_class[5]['name']}",
            'card': {
                'type': "BigImage",
                'image_id': enemy_class[5]['img'],
                'title': f"Ваш противник - {enemy_class[5]['name']}"
            },
            'buttons': [
                {
                    "title": "Ударить панка",
                    "hide": True
                },
                {
                    "title": "Сделать комплимент о его причёске",
                    "hide": True
                },
                {
                    "title": "Испугаться и убежать",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Ударить панка":
        end_game(user_id, req, res)
    elif req['request']['original_utterance'] == "Сделать комплимент о его причёске":
        res['response'] = {
            'text': f"{enemy_class[5]['name']} растрогался и встал на вашу сторону!",
            'card': {
                'type': "BigImage",
                'image_id': enemy_class[5]['img'],
                'title': f"{enemy_class[5]['name']} растрогался и встал на вашу сторону!"
            },
            'buttons': [
                {
                    "title": "Напасть на лучника",
                    "hide": True
                },
                {
                    "title": "Испугаться и убежать",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Напасть на лучника":
        res['response'] = {
            'text': f"Ты хотел напасть на {enemy_class[4]['name']}а, "
                    f"но он напал на тебя...",
            'card': {
                'type': "BigImage",
                'image_id': enemy_class[4]['img'],
                'title': f"Ты хотел напасть на {enemy_class[4]['name']}а, "
                    f"но он напал на тебя..."
            },
            'buttons': [
                {
                    "title": "Ловить все его стрелы и кидать в него",
                    "hide": True
                },
                {
                    "title": "Уворачиваться",
                    "hide": True
                },
                {
                    "title": "Испугаться и убежать",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Ловить все его стрелы и кидать в него":
        end_game(user_id, req, res)
    elif req['request']['original_utterance'] == "Уворачиваться":
        res['response'] = {
            'text': f"Вы увернулись от стрел лучника, они у него кончились "
                    f"и он сбежал с поля боя, напугавшись вас",
            'card': {
                'type': "BigImage",
                'image_id': enemy_class[4]['img'],
                'title': f"Вы увернулись от стрел лучника, они у него кончились "
                         f"и он сбежал с поля боя, напугавшись вас"
            },
            'buttons': [
                {
                    "title": "Что?? Бандит с АК-47?",
                    "hide": True
                },
                {
                    "title": "Испугаться и убежать",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Что?? Бандит с АК-47?":
        res['response'] = {
            'text': f"И вправду... Вообще, его не должно было быть в игре, "
                    f"но он выглядил слишком брутально!",
            'card': {
                'type': "BigImage",
                'image_id': enemy_class[0]['img'],
                'title': f"И вправду... Вообще, его не должно было быть в игре, "
                        f"Но этот выглядил слишком брутально!"
            },
            'buttons': [
                {
                    "title": "Эй, разработчик? И что мне с ним делать?",
                    "hide": True
                },
                {
                    "title": "Побежать на него с мечом",
                    "hide": True
                },
                {
                    "title": "Испугаться и убежать",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Эй, разработчик? И что мне с ним делать?":
        res['response'] = {
            'text': f"Ладно-ладно, я уберу его. Твой новый противник - {enemy_class[6]['name']}",
            'card': {
                'type': "BigImage",
                'image_id': enemy_class[6]['img'],
                'title': f"Ладно-ладно, я уберу его. Твой новый противник - {enemy_class[6]['name']}"
            },
            'buttons': [
                {
                    "title": "Сразиться в бою на мечах",
                    "hide": True
                },
                {
                    "title": "Испугаться и убежать",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Побежать на него с мечом":
        end_game(user_id, req, res)
    if req['request']['original_utterance'] == "Сразиться в бою на мечах":
        res['response'] = {
            'text': f"В бою на мечах тебе нет равных! {enemy_class[6]['name']} повержен",
            'card': {
                'type': "BigImage",
                'image_id': enemy_class[6]['img'],
                'title': f"В бою на мечах тебе нет равных! {enemy_class[6]['name']} повержен"
            },
            'buttons': [
                {
                    "title": "Вау, вот это толстяк там впереди!",
                    "hide": True
                },
                {
                    "title": "Испугаться и убежать",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Вау, вот это толстяк там впереди!":
        res['response'] = {
            'text': f'"Сам ты толстяк" - крикнул тебе {enemy_class[1]["name"]}',
            'card': {
                'type': "BigImage",
                'image_id': enemy_class[1]['img'],
                'title': f'"Сам ты толстяк" - крикнул тебе {enemy_class[1]["name"]}'
            },
            'buttons': [
                {
                    "title": "Предложить попить чай с конфетами",
                    "hide": True
                },
                {
                    "title": "Проткнуть иголкой",
                    "hide": True
                },
                {
                    "title": "Испугаться и убежать",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Предложить попить чай с конфетами":
        end_game(user_id, req, res)
    elif req['request']['original_utterance'] == "Проткнуть иголкой":
        res['response'] = {
            'text': f"{enemy_class[1]['name']} сдулся и улетел, как шарик",
            'buttons': [
                {
                    "title": "Поймать Тёмного Мага",
                    "hide": True
                },
                {
                    "title": "Испугаться и убежать",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Поймать Тёмного Мага":
        res['response'] = {
            'text': f"Тёмный Маг пойман! Ты ждал эпичной битвы? :)",
            'card': {
                'type': "BigImage",
                'image_id': enemy_class[2]['img'],
                'title': f"Тёмный Маг пойман! Ты ждал эпичной битвы? :)"
            },
            'buttons': [
                {
                    "title": "Да!",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Да!":
        res['response'] = {
            'text': f"А Маг вот не ждал! Когда ты подошёл к нему, он сразу же наколдовал себе наручники "
                    f"и приковал себя к ним",
            'card': {
                'type': "BigImage",
                'image_id': enemy_class[2]['img'],
                'title': f"А Маг вот не ждал! Когда ты подошёл к нему, он сразу же наколдовал себе наручники "
                    f"и приковал себя к ним"
            },
            'buttons': [
                {
                    "title": "Я молодец!",
                    "hide": True
                }
            ]
        }
    if req['request']['original_utterance'] == "Я молодец!":
        end_game(user_id, req, res)
    if req['request']['original_utterance'] == "Испугаться и убежать":
        end_game(user_id, req, res)
    # Если игрок захочет покинуть сессию, то мы попрощаемся и завершим её
    elif req['request']['original_utterance'] == "Выйти":
        res['response'] = {
            'text': f"Пока-пока!"
        }
        res['response']['end_session'] = True
    elif req['request']['original_utterance'] == "Начать сначала":
        go_adventure(user_id, req, res)


# Функция, организовывающая выход из игры при выборе игроком разных ситуаций
def end_game(user_id, req, res):
    if req['request']['original_utterance'] == "Испугаться и убежать":
        res['response'] = {
            'text': f"Из-за вашего отказа маг убил вас, посчитав предателем. Поздравляю, вы дурак!",
            'buttons': [
                {
                    "title": "Начать бой сначала",
                    "hide": True
                },
                {
                    "title": "Выйти",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Ударить панка":
        res['response'] = {
            'text': f"{enemy_class[5]['name']} не любит, когда его бьют. "
                    f"Он ударил тебя в ответ. Ты проиграл. "
                    f"Панки, хой!",
            'buttons': [
                {
                    "title": "Начать бой сначала",
                    "hide": True
                },
                {
                    "title": "Выйти",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Ловить все его стрелы и кидать в него":
        res['response'] = {
            'text': f"Такой глупости я ещё не видел..."
                    f"Премия Дарвина у тебя в кармане!",
            'buttons': [
                {
                    "title": "Начать бой сначала",
                    "hide": True
                },
                {
                    "title": "Выйти",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Побежать на него с мечом":
        res['response'] = {
            'text': f"{enemy_class[0]['name']} начал стрелять по тебе и ты умер"
                    f"Глупо!",
            'buttons': [
                {
                    "title": "Начать бой сначала",
                    "hide": True
                },
                {
                    "title": "Выйти",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Предложить попить чай с конфетами":
        res['response'] = {
            'text': f"{enemy_class[1]['name']} не отказался. Вы ушли с поля боя пить чай"
                    f"Ищи плюсы! Зато ты жив!",
            'buttons': [
                {
                    "title": "Начать бой сначала",
                    "hide": True
                },
                {
                    "title": "Выйти",
                    "hide": True
                }
            ]
        }
    elif req['request']['original_utterance'] == "Я молодец!":
        res['response'] = {
            'text': f"Молодец! Ты перебил всех. Добрый Маг сделал тебя новым правителем, " 
                    f"а сам стал служить тебе, как и все оставшиеся выжившие из лагеря сопротивления. "
                    f"Все ликуют! "
                    f"Мир снова воцарил в Орррске!",
            'buttons': [
                {
                    "title": "Выйти",
                    "hide": True
                }
            ]
        }
    # Если игрок захочет начать бой сначала, то мы вернём его в бой
    elif req['request']['original_utterance'] == "Начать бой сначала":
        go_adventure(user_id, req, res)


# Обработчик
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
    # Если игрок не отвечает на кнопки, а пишет какую-то ерунду, то мы отыгрываем концовку
    if 'text' not in response['response']:
        response['response'] = {
            'text': f"Ты начал нести какую-то ахинею, тебя посчитали психом и умертвили. "
                    f"Подсказка: выбирай варианты ответов, а не придумывай свои!",
            'buttons': [
                {
                    "title": "Начать сначала",
                    "hide": True
                },
                {
                    "title": "Выйти",
                    "hide": True
                }
            ]
        }
    return json.dumps(response)


# Функция, с которой начнётся игра. Мы поприветствуем игрока и попросим представиться, если он новый.
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


# Словарь с двумя основными функциями, для перехода между ними
states = {
    1: change_person,
    2: go_adventure
}
# Тут хранятся состояния сессии
session_state = {}

# Завершаем программу
if __name__ == '__main__':
    app.run()
