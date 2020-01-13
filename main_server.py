import socket


def new_user():
    """
    Функция, которая отвечает за обработку запросов и формирования ответа.
    Возвращает False если мест на сервере нет, либо возвращает user_id
    """
    global players
    for i in range(len(players)):
        if len(players[i]) == 0:
            players[i] = [240 + i * 480, 0, 2, 0]
            return i
    return False


def disconnect(user_id):
    """
    Функция, которая удаляет персонажа с поля
    """
    global players
    players[user_id] = []


def set_coord(x, y, direction, user_id, sprite_num):
    """
    Функция, которая обновляет координаты и направление игрока.
    """
    global players
    players[user_id] = (x, y, direction, sprite_num)


if __name__ == '__main__':
    sock = socket.socket()
    sock.bind(('192.168.10.5', 4000))
    sock.listen(4)
    players = [[], [], [], []]
    cou = 0
    try:
        conn, addr = sock.accept()
        while True:
            data = conn.recv(512).decode("utf-8")
            if data == 'new_user':
                a = new_user()
                conn.send(str(a).encode("utf-8"))
            elif data == 'number':
                conn.send(str(players).encode("utf-8"))
            elif data == 'disconnect':
                disconnect(int(conn.recv(512).decode("utf-8")))
            elif data == 'set_coord':
                i = conn.recv(2).decode("utf-8")
                text = conn.recv(int(i)).decode("utf-8").split()
                set_coord(float(text[0]), float(text[1]), int(text[2]), int(text[3]), int(text[4]))
    finally:
        sock.close()
