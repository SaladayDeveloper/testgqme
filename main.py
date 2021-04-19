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
    pass


def go_adventure(user_id, req, res):
    pass


def fight(user_id, req, res):
    pass


def end_game(user_id, req, res):
    pass

@app.route('\post', methods=['POST'])
def get_alice_request():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response':{
            'end_session': False
        }
    }

    handle_dialog(request.json, response)
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Приветствую тебя, душа странника! Назови своё имя'
        session_state['user_id'] = {
            'state': 1
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