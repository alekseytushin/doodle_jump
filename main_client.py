import pygame
from pygame.locals import *
import ast
import os
import requests
import json


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