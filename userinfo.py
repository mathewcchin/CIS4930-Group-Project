import pickle
import os
from player import Player
from setting import Settings
class User:
    def __init__(self):
        self.name = ""
        self.user_list = list()
        self.highscore = 0
        self.score = 0
        self.accuracy = 0.0

    def get_username(self):
        return self.name

    def show_score(self):
        return self.score

    def add_score(self, num):
        self.score += num

    def high_score(self):
        if self.highscore >= self.score:
            self.highscore = self.highscore
        else:
            self.highscore = self.score
        return self.highscore

    def check_user(self, username) -> bool:  # this will be a bool function: 1 - username already used, 0 - not used
        username += ".dat"
        current_dir = os.getcwd() + "/users"
        for file in os.listdir(current_dir):
            if file == username:
                return True
        return False

    def show_users(self):
        current_dir = os.getcwd() + "/users"
        for file in os.listdir(current_dir):
            file = file[:-4]
            self.user_list.append(file)

        return self.user_list


