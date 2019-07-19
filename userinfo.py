import pickle
from os import path


class User:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.filename = self.name + ".dat"

    def save(self):
        pickle.dump(self,open(self.filename, "wb"))

    def load(self, tag):
        tag=tag+".dat"
        return pickle.load(open(tag, "rb"))

