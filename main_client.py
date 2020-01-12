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

    def number_of_people(self):
        payload = {
            "method": "number",
            "params": [],
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            self.url, data=json.dumps(payload), headers=self.headers).json()
        return response

    def update_coord_of_people(self):
        payload = {
            "method": "get_info",
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
            "params": [x, y, direction],
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
    def __init__(self):
        self.G = 10
        self.K_MOVE = 0.8
        self.jump_force = 0
        self.speed = 10

    def get_collision_list(self, unitlist):
        pass

    def move(self, forces, keys):
        result_force = (0, 0)
        if keys[pygame.K_a]:
            result_force[0] -= self.speed
        if keys[pygame.K_d]:
            result_force[0] += self.speed
        for force in forces:
            result_force[0] += force[0]
            result_force[1] += force[1]
        result_force[1] += jump_force
        movement_by_force = (0, 0)
        movement_by_force[0] = result_force[0] * self.K_MOVE
        movement_by_force[1] = result_force[1] * self.K_MOVE


class Platform(Unit):
    pass


class Weapon(Unit):
    pass


class OtherPlayer(Unit):
    pass


class Client:
    def __init__(self, connection):
        pass


def main():
    connection = Connect()
    if not connection.add_user():
        print("Connection failed!")
        input()
        exit()
    client = Client(connection)
