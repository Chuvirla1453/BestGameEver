from heapq import heappush, heappop

from Classes.Cells import *
from Classes.Characters import *


def calculate_turn(enemy, gamefield):
    path = a_star(gamefield.my_map, enemy.get_cell(), gamefield.hero.get_cell())
    print(path)
    if len(path) > 10:
        return
    if len(path) == 2:
        enemy.hit(gamefield.hero)
        return
    if type(gamefield[path[1][0]][path[1][1]].character) == Stone:
        gamefield[path[1][0]][path[1][1]].add_character(None)
        return
    if type(gamefield[path[1][0]][path[1][1]].character) == BaseEnemy:
        return
    gamefield[path[0][0]][path[0][1]].add_character(None)
    gamefield[path[1][0]][path[1][1]].add_character(enemy)
    enemy.move(path[1][1] - path[0][1], path[1][0] - path[0][0])


def a_star(field, start, goal):
    my_field = field.copy()
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j].type in ('wall', 'none'):
                my_field[i][j] = 999
            elif field[i][j].type in ('ladder', 'floor'):
                my_field[i][j] = 1
                if type(field[i][j].character) == BaseEnemy:
                    my_field[i][j] += 998
                elif type(field[i][j].character) == Stone:
                    my_field[i][j] += 1

    rows = len(my_field)
    cols = len(my_field[0])

    graph = {}
    for y, row in enumerate(my_field):
        for x, col in enumerate(row):
            graph[(x, y)] = graph.get((x, y), []) + get_next_nodes(x, y, cols, rows, my_field)

    queue = []
    heappush(queue, (0, start))
    cost_visited = {start: 0}
    visited = {start: None}
    path = []

    while True:
        if queue:
            cur_cost, cur_node = heappop(queue)
            if cur_node == goal:
                queue = []
                continue

            next_nodes = graph[cur_node]
            for next_node in next_nodes:
                neigh_cost, neigh_node = next_node
                new_cost = cost_visited[cur_node] + neigh_cost

                if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                    priority = new_cost + heuristic(neigh_node, goal)
                    heappush(queue, (priority, neigh_node))
                    cost_visited[neigh_node] = new_cost
                    visited[neigh_node] = cur_node

        path_head = cur_node
        path.append(path_head)
        if path_head == goal:
            return path


def heuristic(a, b):
   return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_next_nodes(x, y, cols, rows, my_field):
    check_next_node = lambda x, y: True if 0 <= x < cols and 0 <= y < rows else False
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(my_field[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]
