import queue

class Solution:
    def __init__(self, board):
        self.board = board
        self.start = (0, 0)
        # need to change end coord 
        self.end = (2, 2)

    def find_neighbor(self, board, visited, curr):
        x = curr[0]
        y = curr[1]
        result = []

        potential_neighbor = [(x, y + 1), (x - 1, y), (x, y - 1), (x + 1, y)]

        # need to update bound
        # 0 and g block can be neighbor
        # start position can not be neighbor
        # visited block can not be neighbor
        for (i, j) in potential_neighbor:
            if  (i >= 0 and i < 3) and (j >= 0 and j < 3):
                if board[i][j] == '0' or board[i][j] == "g":
                    if (i, j) not in visited:
                        result.append((i, j))
        return result

    def create_solution(self, backTrack_info):
        print(backTrack_info)
        result = []
        curr = backTrack_info[self.end]

        while curr != (0, 0):
            result.append(curr)
            curr = backTrack_info[curr]
        return result

    def dfs(self):
        # we can use backTrack_info for draw the solution path

        stack = queue.LifoQueue()
        visited = []
        backtrack_info = {}

        stack.put(self.start)
        visited.append(self.start)

        while not stack.empty():
            curr = stack.get()
            neighbor = self.find_neighbor(self.board, visited, curr)
            if curr == self.end:
                print("dfs end")
                print("path")
                print(self.create_solution(backtrack_info))
                break
            
            for child in neighbor:
                backtrack_info[child] = curr
                visited.append(child)
                stack.put(child)
        return backtrack_info

    def bfs(self):
        bfs_queue = queue.Queue()
        visited = []
        backtrack_info = {}

        bfs_queue.put(self.start)
        visited.append(self.start)

        while not bfs_queue.empty():
            curr = bfs_queue.get()
            neighbor = self.find_neighbor(self.board, visited, curr)
            if curr == self.end:
                print("bfs end")
                print("path")
                print(self.create_solution(backtrack_info))
                break
            
            for child in neighbor:
                backtrack_info[child] = curr
                visited.append(child)
                bfs_queue.put(child)        
        return backtrack_info
    


