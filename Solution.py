import queue
import math

class Solution:
    def __init__(self, board):
        self.board = board
        self.start = (0, 0)
        # need to change end coord 
        self.end = (99, 99)

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
            if  (i >= 0 and i < 100) and (j >= 0 and j < 100):
                if board[i][j] == '0' or board[i][j] == "g":
                    if (i, j) not in visited:
                        result.append((i, j))
        return result

    def create_solution(self, backTrack_info):
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
        result = []

        stack.put(self.start)
        visited.append(self.start)

        while not stack.empty():
            curr = stack.get()
            neighbor = self.find_neighbor(self.board, visited, curr)
            if curr == self.end:
                print("dfs end")
                print("visited len")
                print(len(visited))
                print("path len")
                result = self.create_solution(backtrack_info)
                print(len(result))
                print("\n")
                break
            
            for child in neighbor:
                backtrack_info[child] = curr
                visited.append(child)
                stack.put(child)
        return result

    def bfs(self):
        bfs_queue = queue.Queue()
        visited = []
        backtrack_info = {}
        result = []

        bfs_queue.put(self.start)
        visited.append(self.start)

        while not bfs_queue.empty():
            curr = bfs_queue.get()
            neighbor = self.find_neighbor(self.board, visited, curr)
            if curr == self.end:
                print("bfs end")
                print("visited len")
                print(len(visited))
                print("path len")
                result = self.create_solution(backtrack_info)
                print(len(result))
                print("\n")
                break
            
            for child in neighbor:
                backtrack_info[child] = curr
                visited.append(child)
                bfs_queue.put(child)        
        return result
    
    def a_star(self):
        p_queue = queue.PriorityQueue()
        visited = []
        backtrack_info = {}
        result = []
        cost_start_curr = {}

        p_queue.put((0, self.start))
        cost_start_curr[self.start] = 0
        visited.append(self.start)

        while not p_queue.empty():
            curr = p_queue.get()
            curr = curr[1]
            neighbor = self.find_neighbor(self.board, visited, curr)

            if curr == self.end:
                print("A* end")
                print("visited len")
                print(len(visited))
                print("path len")
                result = self.create_solution(backtrack_info)
                print(len(result))

            for child in neighbor:
                backtrack_info[child] = curr
                visited.append(child)
                cost_start_curr[child] = cost_start_curr[curr] + 1
                p_queue.put((cost_start_curr[child] + self.heuristic(child) ,child))

        return result
        
    def heuristic(self, child):
        curr_x = child[0]
        curr_y = child[1]
        end_x = self.end[0]
        end_y = self.end[1]

        return math.sqrt((end_x - curr_x)**2 + (end_y - curr_y)**2)
