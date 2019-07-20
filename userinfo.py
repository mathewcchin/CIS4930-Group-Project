import pickle
import os


class User:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.filename = self.name + ".dat"

    def save(self):
        # finds the 'users' directory and looks to open the associated file name
        current_dir = os.getcwd() + "/users"
        file_to_open = os.path.join(current_dir, self.filename)
        user_file = open(file_to_open, "wb")
        pickle.dump(self, user_file)
        user_file.close()

    def load(self, tag):
        tag = tag + ".dat"
        return pickle.load(open(tag, "rb"))

    def show_score(self):
        return self.score

    def add_score(self, num):
        self.score += num

