class Game:
    def __init__(self, id):

        self.ready = False
        self.id = id


    def getReady(self):
        return self.ready
    
    def getID(self):
        return self.id