import random

class Region():
    def __init__(self):
        self.region={"ể":"ễ","ễ":"ể","ẳ":"ẵ","ẵ":"ẳ","ẩ":"ẫ","ẫ":"ẩ","ử":"ữ","ữ":"ử","ổ":"ỗ","ỗ":"ổ","ở":"ỡ","ỡ":"ở","ẻ":"ẽ","ẽ":"ẻ","ũ":"ủ","ủ":"ũ","ã":"ả","ả":"ã","ỏ":"õ","õ":"ỏ","i":"j","s":"x","l":"n","n":"l","x":"s","d":"gi","S":"X","L":"N","N":"L","X":"S","Gi":"D","D":"Gi"}

    def generate(self, token):
        possible_error = [i for i in token if i in self.region.keys()]
        if len(possible_error) > 0:
            token_error = random.choice(possible_error)
            return token.replace(token_error, self.region[token_error])
        else:
            return False