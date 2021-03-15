
# Whether or not it is a mine or safe.
# if safe, the number of mines surroinding it indicated by clue.
# the number of safe squares indentified arround it.
# the number of mines indentified arround it.
# the number of hidden squares around it. 

class Cell():
    # takes in a String to determine the state of the cell currently.
    # "s" if safe "m" if it has a mine and "?" if uncovered.
    def __init__(self, state):
        self.state = state
        self.safeCount = 0
        self.mineCount = 0
        self.hiddenCount = 0

    def setState(self, state):
        self.state = state
    def setSafeCount(self, safeCount):
        self.safeCount = safeCount
    def setMineCount(self, mineCount):
        self.mineCount = mineCount
    def setHiddenCount(self, hiddenCount):
        self.hiddenCount = hiddenCount

    

