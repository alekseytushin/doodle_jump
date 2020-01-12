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
        self.user_id = False

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
        self.user_id = response['result']
        return response['result']

    def update_coord_of_people(self):
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

    def set_coord(self, x, y, direction):
        """
        Функция, для записывания координат игрока на сервер.
        На вход получает координаты(x, y) и направление движения человека.
        Возвращает True, если можно переместиться или False если клетка занята
        """
        payload = {
            "method": "set_coord",
            "params": [x, y, direction, self.user_id],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            self.url, data=json.dumps(payload), headers=self.headers).json()
        return response['result']


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


class Sprite:
    pass


class Unit:
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite

    def render(self, window):
        window.blit(self.sprite, (self.x, self.y))


class Hero(Unit):
    def get_collision_list(self, unitlist):
        pass

    def move(self, keys):
        pass


class Platform(Unit):
    pass


class Weapon(Unit):
    pass


class OtherPlayer(Unit):
    pass

