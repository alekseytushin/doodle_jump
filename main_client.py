import pygame
from pygame.locals import *
import ast
import os
import requests
import json
import sys


class Connect:
    def __init__(self):
        """
        Класс по подключению игрока к серверу.
        """
        self.url = "http://tushin.ru:4000/jsonrpc"
        self.headers = {'content-type': 'application/json'}

    def add_user(self):
        """
        Функция по добавлению пользователя в игровую сессию
        Возвращает False, если все места заняты.
        Возвращает user_id если на сервере есть место.
        """
        payload = {
            "method": "new_user",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            self.url, data=json.dumps(payload), headers=self.headers).json()
        return response['result']

    def get_unitlist(self):
        """
        Фукция, которая возвращает список игроков с их координатами и направлением
        """
        payload = {
            "method": "number",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            self.url, data=json.dumps(payload), headers=self.headers).json()
        return response['result']

    def set_coord(self, x, y, direction, num_id):
        """
        Функция, для записывания координат игрока на сервер.
        На вход получает координаты(x, y) и направление движения человека.
        Возвращает True, если можно переместиться или False если клетка занята
        """
        payload = {
            "method": "set_coord",
            "params": [x, y, direction, num_id],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            self.url, data=json.dumps(payload), headers=self.headers).json()
        return response['result']

    def disconnect(self, user_id):
        """
        Функция для выхода из игры.
        """
        payload = {
            "method": "disconnect",
            "params": [user_id],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            self.url, data=json.dumps(payload), headers=self.headers).json()
        return


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Unit:
    def __init__(self, x, y, direction, num, obj, img=None):
        image = [['first_user_left.png', 'first_user_right.png']]
        self.x = x
        self.y = y
        self.obj = obj
        if obj == 'player':
            self.imgheight = 400
            self.imgwidth = 500
            self.sprite = pygame.image.load(image[0][direction])
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
        self.imgheight = 400
        self.imgwidth = 500
        self.speed = 10

    def get_collision_list(self, unit):
        if unit.obj == 'player':
            pass
        elif unit.obj == 'ground':
            if self.x + self.imgwidth >= unit.x >= self.x or unit.x + unit.imgwidth >= self.x >= unit.x:
                if self.y + self.imgheight >= unit.y + 20 and self.y + self.imgheight < unit.y + unit.imgheight:
                    self.y = unit.y - 20 - self.imgheight
                    self.onGround = True

    def move(self, forces, keys, connection, UNITLIST):
        result_force = [0, 0]
        for force in forces:
            result_force[0] += force[0]
            result_force[1] += force[1]
        result_force[1] += self.jump_force
        self.x += result_force[0] * self.K_MOVE
        self.y += result_force[1] * self.K_MOVE

        if keys[pygame.K_a]:
            self.x -= self.speed * self.K_MOVE
            self.direction = 0
        if keys[pygame.K_d]:
            self.x += self.speed * self.K_MOVE
            self.direction = 1
        if keys[pygame.K_SPACE]:
            if self.onGround:
                self.onGround = False
                self.jump_force = 500
                self.y -= self.jump_force * self.K_MOVE
                self.jump_force -= self.jump_force / 10

        for i in range(len(UNITLIST)):
            self.get_collision_list(UNITLIST[i])
        connection.set_coord(self.x, self.y, self.direction, self.num_id)


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
        bg = pygame.image.load("bg.png")
        clock = pygame.time.Clock()
        Plats = []
        num = 1
        xPL = 230
        yPL = 800
        while run:
            self.UNITLIST = []
            window.blit(bg, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            players = connection.get_unitlist()
            for i in range(len(players)):
                if len(players[i]) != 0 and (1920 + 512) > players[i][0] > -512 and (1080 + 512) > players[i][1] > -512:
                    self.UNITLIST.append(Unit(players[i][0], players[i][1], players[i][2], i, 'player'))
            for i in range(num):
                Plats.append(Platform(xPL, yPL, pygame.image.load("Platform.jpg")))
                self.UNITLIST.append(Plats[-1])
                xPL += 5
            if pygame.key.get_pressed():
                character.move([(0, 7 * 10)], pygame.key.get_pressed(), connection, self.UNITLIST)
            for unit in self.UNITLIST:
                unit.render(window)
            pygame.display.update()
            clock.tick(240)
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