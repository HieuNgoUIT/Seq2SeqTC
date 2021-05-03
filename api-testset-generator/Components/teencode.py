class Teencode():
    def __init__(self):
        self.teen={"ch":"ck","ph":"f","th":"tk","nh":"nk","Ch":"Ck","Ph":"F","Th":"Tk","Nh":"Nk"}

    def generate(self, token):
        for i in self.teen.keys():
            if i in token:
                return token.replace(i, self.teen[i])
        return False