import random


def proc_gen(level):
    return Map(level)


class Map:
    def __init__(self, level):
        self.enemy_count = 5 * level + random.randint(-1, 3 * level)
        self.room_count = 3 * level + random.randint(-1, 2 * level)
        self.room_count = 1
        self.width = int(self.room_count ** 0.5 * 15)
        self.height = int(self.room_count ** 0.5 * 15)
        self.my_map = []
        self.rooms = []
        for _ in range(self.height):
            self.my_map.append(['.'] * self.width)

        while self.room_count:
            self.room_count -= 1
            self.create_room()

    def create_room(self):
        blocks_count = random.randint(30, 50)
        y0 = random.randint(0, self.height - 1)
        x0 = random.randint(0, self.width - 1)
        queue = [(y0, x0)]
        room_blocks = []
        self.test_my_map = [['.'] * self.width for _ in range(self.height)]

        while blocks_count > 0:
            try:
                p = random.randint(0, len(queue) - 1)
            except:
                break
            t = queue[p]
            del queue[p]
            blocks_count -= 1
            queue += self.neighbours(t[0], t[1])
            self.test_my_map[t[0]][t[1]] = '#'
            room_blocks.append((t[0], t[1]))

        self.clear_room(room_blocks)

    def neighbours(self, y, x, all=False, check=[]):
        t = []
        if not all:
            sym = '#'
        else:
            sym = 'AAAAA'
        if y > 0:
            if self.test_my_map[y - 1][x] != sym and (y - 1, x) not in check:
                t.append((y - 1, x))
        if y < self.height - 1:
            if self.test_my_map[y + 1][x] != sym and (y + 1, x) not in check:
                t.append((y + 1, x))
        if x > 0:
            if self.test_my_map[y][x - 1] != sym and (y, x - 1) not in check:
                t.append((y, x - 1))
        if x < self.width - 1:
            if self.test_my_map[y][x + 1] != sym and (y, x + 1) not in check:
                t.append((y, x + 1))
        return t

    def clear_room(self, room):
        walls = []
        empties = []
        dels = room[:]
        for i in room:
            t = self.neighbours(i[0], i[1], True)
            b = 0
            for j in t:
                if self.test_my_map[j[0]][j[1]] == '.':
                    b += 1
            if b == 0:
                empties.append(i)
            else:
                walls.append(i)
        for i in empties:
            self.test_my_map[i[0]][i[1]] = '_'

        for i in dels:
            t = self.neighbours(i[0], i[1], True)
            for j in t:
                if j in empties:
                    walls.append(i)
                    break
            else:
                self.test_my_map[i[0]][i[1]] = '.'

        room = (walls, empties)

        if not empties or not walls:
            self.del_room(room)
            self.room_count += 1
        elif not self.check_room(room):
            self.del_room(room)
            self.room_count += 1
        else:
            if not self.merge_maps:
                self.del_room(room)
                self.room_count += 1
            else:
                self.rooms.append(room)
                self.merge_maps()

    def check_room(self, room):
        q = self.neighbours(room[1][0][0], room[1][0][1])
        checked = []
        while q:
            q += self.neighbours(q[0][0], q[0][1], False, checked)
            checked.append(q[0])
            del q[0]
            try:
                while q[0] in checked:
                    del q[0]
            except:
                continue
        if len(checked) != len(room[1]):
            return False
        return True

    def del_room(self, room):
        for i in room[0]:
            self.test_my_map[i[0]][i[1]] = '.'
        for i in room[1]:
            self.test_my_map[i[0]][i[1]] = '.'

    def merge_maps(self):
        for i in range(len(self.test_my_map)):
            for j in range(len(self.test_my_map[i])):
                if self.test_my_map[i][j] != '.':
                    self.my_map[i][j] = self.test_my_map[i][j]


for i in proc_gen(1).my_map:
    print(i)


