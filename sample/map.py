import tcod

# actual size of the window
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 80

# size of the map
MAP_WIDTH = 80
MAP_HEIGHT = 70

# number of the room
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

LIMIT_FPS = 30  # 20 frames-per-second maximum


color_dark_wall = tcod.Color(0, 0, 100)
color_dark_ground = tcod.Color(50, 50, 150)


class Tile:
    # a tile of the map and its properties
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight


class Object:
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        # move by the given amount, if the destination is not blocked
        if not game_map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        # set the color and then draw the character that represents this object at its position
        tcod.console_set_default_foreground(con, self.color)
        tcod.console_put_char(
            con, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):
        # erase the character that represents this object
        tcod.console_put_char(con, self.x, self.y, ' ', tcod.BKGND_NONE)


def make_map():
    global game_map, player
    # fill map with "unblocked" tiles
    game_map = [[Tile(True) for y in range(SCREEN_HEIGHT)]
                for x in range(SCREEN_WIDTH)]

    rooms = []
    num_rooms = 0
    for r in range(MAX_ROOMS):
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

            if num_rooms == 0:
                player.x = new_x
                player.y = new_y

            else:
                (prev_x, prev_y) = rooms[num_rooms - 1].center()

                if tcod.random_get_int(0, 0, 1) == 1:
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)

                else:
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)

            rooms.append(new_room)
            num_rooms += 1


class Rect():
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = (self.x1 + self.x2) // 2
        center_y = (self.y1 + self.y2) // 2
        return(center_x, center_y)

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)


def create_room(room):
    global game_map
    for x in range(room.x1, room.x2 + 1):
        for y in range(room.y1, room.y2 + 1):
            game_map[x][y].blocked = False
            game_map[x][y].block_sight = False


def create_h_tunnel(x1, x2, y):
    global game_map
    for x in range(min(x1, x2), max(x1, x2)+1):
        game_map[x][y].blocked = False
        game_map[x][y].block_sight = False


def create_v_tunnel(y1, y2, x):
    global game_map
    for y in range(min(y1, y2), max(y1, y2) + 1):
        game_map[x][y].blocked = False
        game_map[x][y].block_sight = False


def render_all():
    global color_light_wall
    global color_light_ground

    # go through all tiles, and set their background color
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = game_map[x][y].block_sight
            if wall:
                tcod.console_set_char_background(
                    con, x, y, color_dark_wall, tcod.BKGND_SET)
            else:
                tcod.console_set_char_background(
                    con, x, y, color_dark_ground, tcod.BKGND_SET)

    # draw all objects in the list
    for object in objects:
        object.draw()

    # blit the contents of "con" to the root console
    tcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)


def handle_keys():
    # key = tcod.console_check_for_keypress()  #real-time
    key = tcod.console_wait_for_keypress(True)  # turn-based

    if key.vk == tcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

    elif key.vk == tcod.KEY_ESCAPE:
        return True  # exit game

    # movement keys
    if tcod.console_is_key_pressed(tcod.KEY_UP):
        player.move(0, -1)

    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
        player.move(0, 1)

    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
        player.move(-1, 0)

    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
        player.move(1, 0)


#############################################
# Initialization & Main Loop
#############################################

tcod.console_set_custom_font(
    'bbt\\fonts\\arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,
                          'Bored Battle Theater', False)
tcod.sys_set_fps(LIMIT_FPS)
con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

# create object representing the player
player = Object(25, 23, '@', tcod.white)

# create an NPC
# npc = Object(25 - 5, 23, '@', tcod.yellow)

# the list of objects with those two
objects = [player]

# generate map (at this point it's not drawn to the screen)
make_map()
create_h_tunnel(25, 55, 23)


while not tcod.console_is_window_closed():

    # render the screen
    render_all()

    tcod.console_flush()

    # erase all objects at their old locations, before they move
    for object in objects:
        object.clear()

    # handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break
