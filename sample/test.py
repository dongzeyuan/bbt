import pprint


class Tile(object):
    # a tile of the map and its properties
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight


def make_map():
    global game_map
    # fill map with "unblocked" tiles
    game_map = [[Tile(False) for y in range(50)] for x in range(80)]

    room1 = Rect(20, 15, 10, 15)
    room2 = Rect(50, 15, 10, 15)
    creat_room(room1)
    creat_room(room2)


class Rect():
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h


def creat_room(room):
    global game_map
    for x in range(room.x1, room.x2 + 1):
        for y in range(room.y1, room.y2 + 1)
        game_map[x][y].blocked = False
        game_map[x][y].block_sight = False
        


if __name__ == "__main__":
    make_map()
    pprint.pprint(game_map[0][3])
