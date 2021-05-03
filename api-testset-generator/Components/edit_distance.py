import random

class EditDistance():
    def __init__(self):
        self.letters = list("abcdefghijklmnopqrstuvwxyz")
        self.ratio_ed2 = 0.2

    def ed1(self, token):
        return token.replace(token[random.randint(0, len(token)-1)], random.choice(self.letters))

    def generate(self, token):
        if random.uniform(0, 1) > 0.2:
            return self.ed1(token)
        else:
            return self.ed1(self.ed1(token))
