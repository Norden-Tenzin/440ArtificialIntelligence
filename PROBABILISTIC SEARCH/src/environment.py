from board import *

class Environment():
    def __init__(self):
        self.game = Board()
        self.board = self.game.board
        self.target = self.game.target
        
    def search(self, curr):
        p = random.uniform(0, 1)
        currNegRate = self.getNegRate(curr)
        if p > currNegRate:
            if curr == self.target:
                return (True, self.getNegRate(curr))
            else:
                return (False, self.getNegRate(curr))
        else:
            return (False, self.getNegRate(curr))
    
    def newBoard(self):
        self.game.newBoard()
        self.board = self.game.board
        self.target = self.game.target
    
    def getNegRate(self, pos):
        row = pos[0]
        col = pos[1]
        if self.board[row][col] == 1:
            return 0.1
        elif self.board[row][col] == 2:
            return 0.3
        elif self.board[row][col] == 3:
            return 0.7
        elif self.board[row][col] == 4:
            return 0.9

def main():
    env = Environment()
    print(env.getNegRate((0,0)))

if __name__ == '__main__':
    main()
        