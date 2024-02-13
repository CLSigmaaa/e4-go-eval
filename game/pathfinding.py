from collections import deque

class Pathfinding:
    def __init__(self, game) -> None:
        self.map = game.map
        self.path = []
        self.first_path_element = None
    
    def get_neighbors(self, cell):
        x, y = cell
        neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1), (x-1, y-1), (x+1, y+1)]
        res = []
        for neighbor in neighbors:
            if 0 < neighbor[0] < len(self.map[0]) and 0 < neighbor[1] < len(self.map):
                if self.map[neighbor[0]][neighbor[1]] != 'W':
                    res.append(neighbor)
        return res
    
    def bfs(self, start, end):
        queue = deque([(start, [])])
        visited = set()
        while queue:
            pos, path = queue.popleft()
            path.append(pos)
            visited.add(pos)
            adj_neighbors = self.get_neighbors(pos, self.map)
            for neighbor in adj_neighbors:
                if neighbor == end:
                    self.path = path
                    self.first_path_element = path[0]
                    return path
                if neighbor not in visited:
                    queue.append((neighbor, path + [pos]))
        return None