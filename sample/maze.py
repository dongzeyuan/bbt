import tcod
from random import sample, randint, choice


class Tile:
    '''
    地图上的砖块，三个属性，blocked, block_sight, color.
    '''

    def __init__(self, blocked, block_sight=None, color=tcod.grey):
        self.blocked = blocked

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight
        self.color = color


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.x2 = x+w
        self.y1 = y
        self.y2 = y+h
        self.w = w
        self.h = h
        self.c_x = (self.x1 + self.x2) // 2
        self.c_y = (self.y1 + self.y2) // 2

    def intersect(self, other):
        # returns true if this rectangle intersects with another one.
        # 这里修改了重叠判定算法
        return ((abs(self.c_x - other.c_x) < (self.w + other.w) // 2 + 1) and
                (abs(self.c_y - other.c_y) < (self.h + other.h) // 2 + 1))


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)]
                 for x in range(self.width)]

        for x in range(self.width):
            for y in range(self.height):
                if (x % 2 == 1 and y % 2 == 1):
                    tiles[x][y].color = tcod.yellow

        return tiles

    def make_map(self, max_tried, room_min_size, room_max_size, map_width, map_height):
        rooms = []
        num_rooms = 0

        for r in range(max_tried):
            # random width and height
            w = sample(room_max_size, 1)[0]
            h = sample(room_min_size, 1)[0]
            # random position without going out of the boundaries of the map
            x = randint(1, map_width - w - 1)
            y = randint(1, map_height - h - 1)

            if self.tiles[x][y].color == tcod.yellow:
                # 'Rect' class makes rectangles easier to work with
                new_room = Rect(x-1, y-1, w, h)

            # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
            # 这个else的缩进错误，花费了1小时去修正
                else:
                    # this means there are no intersections, so this rooms is valid

                    # 'paint' it to the map's tiles
                    self.create_room(new_room)
                # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1
        self.create_maze()

    def create_room(self, room):
        # go throught the tiles in the rectangele and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_maze(self):
        # 随机选取一点
        fail = False
        # top, bottom, left, right = (0,-2), (0,2), (-2,0)
        dir_dict = {'top': (0, -2), 'bottom': (0, 2),
                    'left': (-2, 0), 'right': (2, 0)}
        brige_dict = {'top': (0, -1), 'bottom': (0, 1),
                    'left': (-1, 0), 'right': (1, 0)}
        path = []



def handle_key(key):  # ESC退出
    if key.vk == tcod.KEY_ESCAPE:
        return{'exit': True}
    return {}


def render_all(con, game_map, colors):
    for y in range(game_map.height):
        for x in range(game_map.width):

            wall = game_map.tiles[x][y].block_sight

            if not wall:
                tcod.console_set_char_background(
                    con, x, y, colors.get('dark_ground'), tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(
                    con, x, y, game_map.tiles[x][y].color, tcod.BKGND_SET)


def main():
    screen_width = 81
    screen_height = 51

    map_width = 81
    map_height = 51

    room_max_size = [10, 12]
    room_min_size = [10, 12]
    max_tried = 300

    colors = {
        'dark_wall': tcod.Color(0, 0, 100),
        'dark_ground': tcod.orange,
        'light_wall': tcod.Color(130, 110, 50),
        'light_ground': tcod.Color(200, 180, 50)
    }

    tcod.console_set_custom_font(
        "BBT\\fonts\\arial12x12.png", tcod.FONT_TYPE_GRAYSCALE | tcod.FONT_LAYOUT_TCOD)
    tcod.console_init_root(screen_width, screen_height,
                           'Maze Generator', False)

    con = tcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_tried, room_min_size,
                      room_max_size, map_width, map_height)

    while not tcod.console_is_window_closed():

        tcod.console_set_default_foreground(0, tcod.white)
        tcod.console_put_char(con, 0, 0, '@', tcod.BKGND_NONE)
        tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

        render_all(con, game_map, colors)

        tcod.console_flush()

        key = tcod.console_check_for_keypress()
        action = handle_key(key)

        exit = action.get('exit')
        if exit:
            return True


if __name__ == "__main__":
    main()
