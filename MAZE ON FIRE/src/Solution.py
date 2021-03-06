## @Sangkyun Kim @Tenzin Norden
## PROJECT 1 440 

## imports
import queue
import math

class Solution:
    ## Solution class constructor 
    ## @param board the maze array
    ## @param start is the tuple pos at which the agent is starting
    ## @param mode selects if stategy 3 should be used
    ## @param fireStartLoc is the tuple pos at the fire is starting from 
    def __init__(self, board, start, mode, fireStartLoc):
        self.board = board
        self.start = start
        self.end = (len(board) - 1, len(board) - 1)
        self.mode = mode
        self.fireLoc = fireStartLoc

    ## finds the neighbors of the current pos and collects it depending on the algorithm picked
    ## @param board the maze array
    ## @param visited it holds the pos of all the visited blocks
    ## @param curr is the current pos of the agent 
    ## @param algo selects if dfs should be used
    ## @return result list of portential neighbors
    def find_neighbor(self, board, visited, curr, algo):
        x = curr[0]
        y = curr[1]
        result = []

        potential_neighbor = [(x, y - 1), (x - 1, y), (x, y + 1), (x + 1, y)]

        for (i, j) in potential_neighbor:
            if  (i >= 0 and i < len(board)) and (j >= 0 and j < len(board)):
                if algo == "dfs":
                    if board[i][j] == '0' or board[i][j] == "g":
                        if (i, j) not in visited:
                            result.append((i, j))
                else:
                    if board[i][j] == '0' or board[i][j] == "g" or board[i][j] == "2":
                        if (i, j) not in visited:
                            result.append((i, j))
        return result

    ## Creates a solution from backtrack_info and start_pos 
    ## @param backTrack_info its a dictionary object which holds all the blocks as parent and child
    ## @param start_pos its the start pos of the agent
    ## @return result list of pos that mark the final path
    def create_solution(self, backTrack_info, start_pos):
        result = []        
        try:
            curr = backTrack_info[self.end] #(99,99)
        except IndexError:
            return []
            print("Out of range")
        while curr != start_pos:
            result.append(curr)
            curr = backTrack_info[curr]
        return result

    ## DFS algorithm 
    ## @return backtrack_info if available and list of visited blocks 
    def dfs(self):
        stack = queue.LifoQueue()
        visited = []
        backtrack_info = {}
        result = []

        stack.put(self.start)
        visited.append(self.start)

        while not stack.empty():
            curr = stack.get()
            neighbor = self.find_neighbor(self.board, visited, curr, "dfs")
            for child in neighbor:
                backtrack_info[child] = curr
                visited.append(child)
                stack.put(child)
            if curr == self.end:
                return (backtrack_info, visited)
        return ({}, visited)

    ## BFS algorithm 
    ## @return backtrack_info if available and list of visited blocks 
    def bfs(self):
        bfs_queue = queue.Queue()
        visited = []
        backtrack_info = {}
        result = []

        bfs_queue.put(self.start)
        visited.append(self.start)

        while not bfs_queue.empty():
            curr = bfs_queue.get()
            neighbor = self.find_neighbor(self.board, visited, curr, "bfs")
            for child in neighbor:
                backtrack_info[child] = curr
                visited.append(child)
                bfs_queue.put(child)      
            if curr == self.end:
                return (backtrack_info, visited)
        return ({}, visited) 
    
    ## A* algorithm 
    ## @return backtrack_info if available and list of visited blocks 
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
            neighbor = self.find_neighbor(self.board, visited, curr, "a_star")
            for child in neighbor:
                backtrack_info[child] = curr
                visited.append(child)
                cost_start_curr[child] = cost_start_curr[curr] + 1
                p_queue.put((cost_start_curr[child] + self.heuristic(child, self.fireLoc, self.mode) ,child))
            if curr == self.end:
                return (backtrack_info, visited)
        return ({}, visited)
    
    ## Heurisitc it calculates the distance from player position to the end point and the initial fire position
    ## @param child the possible neigbors of the current position
    ## @param fireLoc is the initial fire location
    ## @param mode selects if stategy 3 should be used
    ## @return distance values which gets used by A*
    def heuristic(self, child, fireLoc, mode):
        curr_x = child[0]
        curr_y = child[1]
        end_x = self.end[0]
        end_y = self.end[1]
        fire_x = fireLoc[0]
        fire_y = fireLoc[1]
        if mode == "strat3":
            return math.sqrt((end_x - curr_x)**2 + (end_y - curr_y)**2) - math.sqrt((fire_x - curr_x)**2 + (fire_y - curr_y)**2)
        return math.sqrt((end_x - curr_x)**2 + (end_y - curr_y)**2)
