import pickle
import os


class User:
    def __init__(self):
        self.name = ""
        self.score = 0
        self.filename = self.name + ".dat"
        self.user_list = list()

    def save(self):
        # finds the 'users' directory and looks to open the associated file name
        current_dir = os.getcwd() + "/users"
        file_to_open = os.path.join(current_dir, self.filename)
        user_file = open(file_to_open, "wb")
        pickle.dump(self, user_file)
        user_file.close()

    def load(self, tag):
        file = os.path.join((os.getcwd() + "/users"), tag + ".dat")
        return pickle.load(open(file, "rb"))

    def show_score(self):
        return self.score

    def add_score(self, num):
        self.score += num

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
