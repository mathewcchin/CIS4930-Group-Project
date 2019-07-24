
import os

class User:
    def __init__(self):
        self.name = ""
        self.user_list = list()
        self.highscore = 0
        self.score = 0

    def show_score(self):
        self.high_score()
        return self.score

    def show_highscore(self):
        return self.highscore

    def add_score(self, num):
        self.score += num

    def high_score(self):
        if self.highscore >= self.score:
            self.highscore = self.highscore
        else:
            self.highscore = self.score

    def check_user(self, username) -> bool:  # this will be a bool function: 1 - username already used, 0 - not used
        username += ".dat"
        current_dir = os.getcwd() + "/users"
        for file in os.listdir(current_dir):
            if file == username:
                return 1

        return 0

    def show_users(self):
        current_dir = os.getcwd() + "/users"
        for file in os.listdir(current_dir):
            file = file[:-4]
            self.user_list.append(file)

        return self.user_list
