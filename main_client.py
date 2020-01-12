import pygame
from pygame.locals import *
import ast
import os
import requests
import json
import sys


class Connect:
    def __init__(self):
        self.url = "http://tushin.ru:4000/jsonrpc"
        self.headers = {'content-type': 'application/json'}
        self.user_id = False

    def add_user(self):
        payload = {
            "method": "new_user",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            self.url, data=json.dumps(payload), headers=self.headers).json()
        self.user_id = response['result']
        return response

    def update_coord_of_people(self):
        payload = {
            "method": "number",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            self.url, data=json.dumps(payload), headers=self.headers).json()
        return response

    def set_coord(self, x, y, direction):
        payload = {
            "method": "set_coord",
            "params": [x, y, direction, self.user_id],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            self.url, data=json.dumps(payload), headers=self.headers).json()
        return response


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

