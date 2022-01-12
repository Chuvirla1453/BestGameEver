from heapq import heappush, heappop

from Classes.Cells import *
from Classes.Characters import *
from Classes.Consts import *


def calculate_turn(enemy, game_field):
    if heuristic((enemy.get_cell()[0] + 17, enemy.get_cell()[1] + 14),
                  (game_field.hero.get_cell()[0] + 17, game_field.hero.get_cell()[1] + 14)) > 10:
        return
    path = a_star(game_field.my_map, (enemy.get_cell()[0] + 17, enemy.get_cell()[1] + 14),
                  (game_field.hero.get_cell()[0] + 17, game_field.hero.get_cell()[1] + 14))
    print(*path)

    if len(path) == 2:
        enemy.hit(game_field.hero)
        GETTING_HIT_SND.play()
        return
    if len(path) < 2:
        return
    if type(game_field.my_map[path[1][0]][path[1][1]].character) == Stone:
        game_field.my_map[path[1][0]][path[1][1]].add_character(None)
        return
    if type(game_field.my_map[path[1][0]][path[1][1]].character) == BaseEnemy:
        return
    return (path[1][0] - path[0][0], path[1][1] - path[0][1])


def a_star(field, start, goal):
    print("Goal", goal[0], goal[1])
    print("Start", start[0], start[1])
    my_field = [[0] * len(field[0]) for _ in range(len(field))]
    for i in range(len(field)):
        for j in range(len(field[i])):
            if field[i][j].type in ('wall', 'none'):
                my_field[i][j] = 999
            elif field[i][j].type in ('ladder', 'floor'):
                if type(field[i][j].character) == BaseEnemy:
                    my_field[i][j] = 999
                elif type(field[i][j].character) == Stone:
                    my_field[i][j] = 2
                elif type(field[i][j].character) == MainCharacter:
                    continue
                else:
                    my_field[i][j] = 1
    for i in my_field:
        print(*i)

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

    while queue:
        cur_cost, cur_node = heappop(queue)
        if cur_node == goal:
            break

        neighbours = graph[cur_node]
        for neighbour in neighbours:
            neigh_cost, neigh_node = neighbour
            new_cost = cost_visited[cur_node] + neigh_cost

            if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                priority = new_cost + heuristic(neigh_node, goal)
                heappush(queue, (priority, neigh_node))
                cost_visited[neigh_node] = new_cost
                visited[neigh_node] = cur_node

    path_segment = goal
    while path_segment and path_segment in visited:
        path.append(path_segment)
        path_segment = visited[path_segment]
    path.reverse()
    return path


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_next_nodes(x, y, cols, rows, my_field):
    ways = [-1, 0], [0, -1], [1, 0], [0, 1]
    return [(my_field[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy, cols, rows, my_field)]


def check_next_node(x, y, cols, rows, my_field):
    if 0 <= x < cols and 0 <= y < rows:
        if my_field[y][x] != 999:
            return True
    return False
