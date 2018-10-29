import tcod
from random import sample, randint, choice


class Tile:
    '''
    地图上的砖块，三个属性，blocked, block_sight, color.
    '''

    def __init__(self, blocked, block_sight=None, maze=0, color=tcod.grey):
        self.blocked = blocked

        # By default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight
        self.maze = maze
        self.color = color


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.x2 = x + w
        self.y1 = y
        self.y2 = y + h
        self.w = w
        self.h = h
        self.c_x = (self.x1 + self.x2) // 2
        self.c_y = (self.y1 + self.y2) // 2

    def intersect(self, other):
        # returns true if this rectangle intersects with another one.
        # 这里修改了重叠判定算法
        return ((abs(self.c_x - other.c_x) < (self.w + other.w) // 2 + 0) and
                (abs(self.c_y - other.c_y) < (self.h + other.h) // 2 + 0))


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
                new_room = Rect(x - 1, y - 1, w, h)

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
                self.tiles[x][y].color = tcod.orange

    def create_maze(self):

        # top, bottom, left, right = (0,-2), (0,2), (-2,0)

        dir_dict = {'top': (0, -2), 'bottom': (0, 2),
                    'left': (-2, 0), 'right': (2, 0)}
        brige_dict = {'top': (0, -1), 'bottom': (0, 1),
                      'left': (-1, 0), 'right': (1, 0)}

        find_start = False

        dir_list1 = []
        dir_list2 = []

        path = []

        # 寻找初始点，如果初始点坐标的图块是黄色，将其变为红色
        # 加入path，将find_start改为True，终止寻找
        while not find_start:
            x = randint(1, self.width - 1)
            y = randint(1, self.height - 1)
            if self.tiles[x][y].color == tcod.yellow and self.tiles[x][y].blocked == True:
                self.tiles[x][y].color = tcod.red
                path.append((x, y))
                find_start = True
            else:
                continue

        # 判断path长度，如果path为空，len（path）=0，停止循环
        while len(path):
            x, y = path[-1]
            # 判断四个方向坐标是否在地图内，如果在地图内，将其加入dir_list1
            for key in dir_dict:
                dx, dy = dir_dict.get(key)
                if 1 <= x + dx <= self.width - 1 and 1 <= y + dy <= self.height - 1 and self.tiles[x + dx][y + dy].color == tcod.yellow:
                    dir_list1.append(dir_dict.get(key))
            # 判断dir_list1的长度，如果长度不为0，说明path[-1]周围至少有一个点可以向外延伸
            # 如果为0，说明path[-1]点是个死胡同，需要删除，返回上一个点
            if len(dir_list1):
                # 从dir_list1中随机一个方向
                dx, dy = sample(dir_list1, 1)[0]
                # 向此处延伸一个格子，涂红
                self.tiles[x + dx][y + dy].color = tcod.red
                # 加入path
                path.append((x + dx, y + dy))
                # 重置dir_list1
                dir_list1 = []
                # 下面四个语句判断延伸的方向，将两个格子中间位置涂红
                if dx == -2:
                    self.tiles[x - 1][y].color = tcod.red
                if dx == 2:
                    self.tiles[x + 1][y].color = tcod.red
                if dy == -2:
                    self.tiles[x][y - 1].color = tcod.red
                if dy == 2:
                    self.tiles[x][y + 1].color = tcod.red
            # path[-1]点不满足要求，需删除
            else:
                path.pop()


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
                    con, x, y, game_map.tiles[x][y].color, tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(
                    con, x, y, game_map.tiles[x][y].color, tcod.BKGND_SET)


def main():
    screen_width = 81
    screen_height = 67

    map_width = 81
    map_height = 67

    room_max_size = [8, 10, 12]
    room_min_size = [8, 10, 12]
    max_tried = 500

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
