from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import sqlite3


@dispatcher.add_method
def add_user():
    """
    Функция, которая отвечает за обработку запросов и формирования ответа.
    Возвращает False если мест на сервере нет, либо возвращает user_id
    """
    global players
    if len(players) == 0:
        players.append([0, 0, 'right'])  # изменить
    elif len(players) == 1:
        players.append([0, 0, 'right'])  # изменить
    elif len(players) == 2:
        players.append([0, 0, 'left'])  # изменить
    elif len(players) == 3:
        players.append([0, 0, 'left'])  # изменить
    elif len(players) == 4:
        return False
    return len(players) - 1


@dispatcher.add_method
def number():
    """
    Функция, которая возвращает всю информацию о игроках.
    """
    global players
    return players


@dispatcher.add_method
def set_coord(x, y, direction, user_id):
    """
    Функция, которая обновляет координаты и направление игрока.
    """
    global players
    players[user_id] = (x, y, direction)
    return True


@Request.application
def application(request):
    """
    Обработка всех входящих запросов
    """
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    players = []
    run_simple('192.168.10.5', 4000, application)