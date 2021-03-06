import time
import tcod


# actual size of the window
SCREEN_WIDTH = 101
SCREEN_HEIGHT = 81

# size of the game_map
MAP_WIDTH = 101
MAP_HEIGHT = 81

# number of the room
ROOM_MAX_SIZE = 14
ROOM_MIN_SIZE = 6
MAX_ROOMS = 20
TRIED_TIMES = 2000

LIMIT_FPS = 30  # 20 frames-per-second maximum

color_dark_ground = tcod.Color(245, 245, 245)
color_dark_wall = tcod.Color(128, 128, 128)


class Tile:
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight


class Rect():
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.w = w
        self.h = h
        self.c_x = (self.x1 + self.x2) // 2
        self.c_y = (self.y1 + self.y2) // 2

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return(center_x, center_y)

    def intersect(self, other):
        # 比较两者中心点X轴和y轴距离，若大于两者宽度之和的一半和长度之和的一半
        # 说明两者无重叠，若小于，则两者重叠. 后面的self.w + other.w式子整体越大，房间间距越大
        return ((abs(self.c_x - other.c_x) < (self.w + other.w) // 2 + 4) and
                (abs(self.c_y - other.c_y) < (self.h + other.h) // 2 + 4))


def create_room(room):
    global game_map
    for x in range(room.x1, room.x2 + 1):
        for y in range(room.y1, room.y2 + 1):
            game_map[x][y].blocked = False
            game_map[x][y].block_sight = False


def make_game_map():
    global game_map

    game_map = [[Tile(True) for y in range(SCREEN_HEIGHT)]
                for x in range(SCREEN_WIDTH)]

    rooms = []
    tried = 0

    for r in range(TRIED_TIMES):
        w = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)
        h = tcod.random_get_int(0, ROOM_MIN_SIZE, ROOM_MAX_SIZE)

        x = tcod.random_get_int(0, 0, MAP_WIDTH - w - 1)
        y = tcod.random_get_int(0, 0, MAP_HEIGHT - h - 1)

        new_room = Rect(x, y, w, h)
        failed = False

        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break
        if not failed:
            create_room(new_room)
            (new_x, new_y) = new_room.center()

            rooms.append(new_room)
            tried += 1


def render_all():
    global color_light_wall
    global color_light_ground

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = game_map[x][y].block_sight
            if wall:
                tcod.console_set_char_background(
                    con, x, y, color_dark_wall, tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(
                    con, x, y, color_dark_ground, tcod.BKGND_SET)

    tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def handle_keys():
    # key = tcod.console_check_for_keypress()  #real-time
    key = tcod.console_wait_for_keypress(True)  # turn-based

    if key.vk == tcod.KEY_ESCAPE:
        return True  # exit game
    else:
        return True



# setup the font
tcod.console_set_custom_font('bbt\\fonts\\arial10x10.png',
                             tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD,)

# initialize the root console in a context.
tcod.console_init_root(MAP_WIDTH, MAP_HEIGHT, "title", False)

tcod.sys_set_fps(LIMIT_FPS)
con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

make_game_map()

# MAIN LOOP
while not tcod.console_is_window_closed():
    # 渲染地图
    render_all()
    # 刷新
    tcod.console_flush()
    # handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break
