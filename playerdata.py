import pickle


class PlayerData:
    def __init__(self, player_id, color_str, x, y, joined=False):
        self.player_id = player_id
        self.color_str=color_str
        self.posX=x
        self.posY=y
        self.joined=joined

    def __repr__(self):
        return str(self.player_id) + ", " + self.color_str + ", " + str(self.posX) + ", " + str(self.posY)

    def opponent_id(self):
        return 3 - self.player_id

    def update(self, updated_self):
        self.posX = updated_self.posX
        self.posY = updated_self.posY

    def pickle(self):
        return pickle.dumps(self)
