from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from jsonrpc import JSONRPCResponseManager, dispatcher
import sqlite3


@dispatcher.add_method
def add_user():
    global players
    if len(players) == 0:
        players.append(0, 0, 'right')  # изменить
    elif len(players) == 1:
        players.append(0, 0, 'right')  # изменить
    elif len(players) == 2:
        players.append(0, 0, 'left')  # изменить
    elif len(players) == 3:
        players.append(0, 0, 'left')  # изменить
    elif len(players) == 4:
        return False
    return len(players) - 1


@dispatcher.add_method
def number():
    global players
    return players


@dispatcher.add_method
def set_coord(x, y, direction, user_id):
    con = sqlite3.connect('C:\\Users\\Admin\\Desktop\\server\\new.db')
    cur = con.cursor()
    result = cur.execute("""SELECT kW,Daytime,Night,Special,Extrainformation,debt FROM counter
                            WHERE id == """ + str(user_id)).fetchone()
    con.close()
    return result


@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    players = []
    run_simple('192.168.10.5', 4000, application)