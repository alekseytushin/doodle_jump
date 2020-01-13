import pygame
from pygame.locals import *
import ast
import os
import socket
import sys
import time


class Connect:
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect(("212.33.255.45", 4000))

    def add_user(self):
        """
        Функция по добавлению пользователя в игровую сессию
        Возвращает False, если все места заняты.
        Возвращает user_id если на сервере есть место.
        """

        self.sock.send(b'new_user')
        answer = self.sock.recv(512).decode("utf-8")
        if answer.isdigit():
            answer = int(answer)
        return answer

    def get_unitlist(self):
        """
        Фукция, которая возвращает список игроков с их координатами и направлением
        """
        self.sock.send(b'number')
        answer = eval(self.sock.recv(512).decode("utf-8"))
        return answer

    def set_coord(self, x, y, direction, num_id, sprite_num):
        """
        Функция, для записывания координат игрока на сервер.
        На вход получает координаты(x, y) и направление движения человека.
        Возвращает True, если можно переместиться или False если клетка занята
        """
        string = ' '.join([str(x), str(y), str(direction), str(num_id), str(sprite_num)])
        self.sock.send(b'set_coord')
        self.sock.send(str(len(string)).encode("utf-8"))
        self.sock.send(string.encode("utf-8"))

    def disconnect(self, user_id):
        """
        Функция для выхода из игры.
        """
        self.sock.send(b'disconnect')
        self.sock.send(str(user_id).encode("utf-8"))
        self.sock.close()


class Unit:
    def __init__(self, x, y, direction, num, obj, img=None, sprite_num=None):
        self.x = x
        self.y = y
        self.obj = obj
        walkRight = [pygame.image.load('game_files/pygame_right_1.png'),
                     pygame.image.load('game_files/pygame_right_2.png'),
                     pygame.image.load('game_files/pygame_right_3.png'),
                     pygame.image.load('game_files/pygame_right_4.png'),
                     pygame.image.load('game_files/pygame_right_5.png'),
                     pygame.image.load('game_files/pygame_right_6.png')]

        walkLeft = [pygame.image.load('game_files/pygame_left_1.png'),
                    pygame.image.load('game_files/pygame_left_2.png'),
                    pygame.image.load('game_files/pygame_left_3.png'),
                    pygame.image.load('game_files/pygame_left_4.png'),
                    pygame.image.load('game_files/pygame_left_5.png'),
                    pygame.image.load('game_files/pygame_left_6.png')]

        stand = pygame.image.load('game_files/pygame_idle.png')
        if obj == 'player':
            self.imgheight = 400
            self.imgwidth = 500
            if direction == 0:
                self.sprite = walkLeft[sprite_num]
            elif direction == 1:
                self.sprite = walkRight[sprite_num]
            elif direction == 2:
                self.sprite = stand
        else:
            self.sprite = img
            self.imgwidth = img.get_width()
            self.imgheight = img.get_height()

    def render(self, window):
        window.blit(self.sprite, (self.x, self.y))


class Hero:
    def __init__(self, x, y, direction, num_id):
        self.G = 10
        self.K_MOVE = 0.8
        self.jump_force = 0
        self.onGround = False
        self.x = x
        self.y = y
        self.num_id = num_id
        self.direction = direction
        self.imgheight = 71
        self.imgwidth = 60
        self.speed = 10
        self.sprite_num = 0

    def get_collision_list(self, unit):
        if unit.obj == 'player':
            pass
        elif unit.obj == 'ground':
            if self.x + self.imgwidth >= unit.x >= self.x or unit.x + unit.imgwidth >= self.x >= unit.x:
                if unit.y + 10 <= self.y + self.imgheight < unit.y + unit.imgheight:
                    self.y = unit.y - self.imgheight
                    self.onGround = True

    def move(self, forces, keys, connection, UNITLIST):
        result_force = [0, 0]
        for force in forces:
            result_force[0] += force[0]
            result_force[1] += force[1]
        result_force[1] += self.jump_force
        self.x += result_force[0] * self.K_MOVE / 5
        self.y += result_force[1] * self.K_MOVE / 5

        if keys[pygame.K_a]:
            self.x -= self.speed * self.K_MOVE
            if self.direction == 1:
                self.sprite_num = 0
            self.direction = 0
            self.sprite_num += 1
        elif keys[pygame.K_d]:
            self.x += self.speed * self.K_MOVE
            if self.direction == 0:
                self.sprite_num = 0
            self.direction = 1
            self.sprite_num += 1
        else:
            self.direction = 2
            self.sprite_num = 0
        if self.sprite_num > 5:
            self.sprite_num = 0

        if keys[pygame.K_SPACE]:
            if self.onGround:
                self.onGround = False
                self.jump_force = 250

        # for jump
        if self.jump_force > 20:
            self.y -= self.jump_force / 2
            self.jump_force -= self.jump_force / 10

        for i in range(len(UNITLIST)):
            self.get_collision_list(UNITLIST[i])
        connection.set_coord(self.x, self.y, self.direction, self.num_id, self.sprite_num)


class Platform(Unit):
    def __init__(self, x, y, image):
        Unit.__init__(self, x, y, 0, 0, 'ground', img=image)


class Weapon(Unit):
    pass


class OtherPlayer(Unit):
    pass


class Client:
    def __init__(self, connection, character_id):
        pygame.init()
        pygame.display.set_caption("Stick Fight The Game")
        window = pygame.display.set_mode((1920, 1080), flags=pygame.FULLSCREEN)
        players = connection.get_unitlist()
        character = Hero(players[character_id][0], players[character_id][1], players[character_id][2], character_id)
        run = True
        bg = pygame.image.load("game_files/bg.png")
        clock = pygame.time.Clock()
        Plats = []
        num = 1
        xPL = 230
        yPL = 800
        while run:
            clock.tick(120)
            self.UNITLIST = []
            window.blit(bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            players = connection.get_unitlist()
            for i in range(len(players)):
                if len(players[i]) != 0 and (1920 + 512) > players[i][0] > -512 and (1080 + 512) > players[i][1] > -512:
                    self.UNITLIST.append(Unit(players[i][0], players[i][1],
                                              players[i][2], i, 'player', sprite_num=players[i][3]))
            Plats.append(Platform(xPL, yPL, pygame.image.load("game_files/Platform.jpg")))
            self.UNITLIST.append(Plats[-1])
            if pygame.key.get_pressed():
                character.move([(0, 9 * 10)], pygame.key.get_pressed(), connection, self.UNITLIST)
            for unit in self.UNITLIST:
                unit.render(window)
            pygame.display.update()
        pygame.quit()


def main():
    try:
        connection = Connect()
        char_id = connection.add_user()
        if char_id != 0 and char_id == False:
            print("Connection failed!")
            exit()
        client = Client(connection, char_id)
        connection.disconnect(char_id)
    except Exception as e:
        print(str(e))
        connection.disconnect(char_id)


if __name__ == "__main__":
    main()