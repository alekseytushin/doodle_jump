from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher


@dispatcher.add_method
def new_user():
    """
    Функция, которая отвечает за обработку запросов и формирования ответа.
    Возвращает False если мест на сервере нет, либо возвращает user_id
    """
    global players
    for i in range(len(players)):
        if len(players[i]) == 0:
            players[i] = [240 + i * 480, 0, i % 2]
            return i
    return False


@dispatcher.add_method
def number():
    """
    Функция, которая возвращает всю информацию о игроках.
    """
    global players
    return players


@dispatcher.add_method
def disconnect(user_id):
    """
    Функция, которая удаляет персонажа с поля
    """
    global players
    players[user_id] = []
    return


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
    players = [[], [], [], []]
    run_simple('192.168.10.5', 4000, application)