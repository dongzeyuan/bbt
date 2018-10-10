import libtcodpy as tcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
MAP_WIDTH = 80
MAP_HEIGHT = 45
LIMITS_FPS = 30
player_x = (SCREEN_WIDTH // 2)
player_y = (SCREEN_HEIGHT // 2)

# font_path = 'D:\code\BBT\\fonts\\arial10x10.png'
font_path = 'E:\Python\\bbt\\fonts\\arial10x10.png'
font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
tcod.console_set_custom_font(font_path, font_flags)

window_title = 'Bored Battle Theater'
fullscreen = False
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, fullscreen)
con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
tcod.sys_set_fps(LIMITS_FPS)


class Object(object):
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        tcod.console_set_default_foreground(con, self.color)
        tcod.console_put_char(con, self.x, self.y, self.char, tcod.BKGND_NONE)

    def clear(self):
        tcod.console_put_char(con, self.x, self.y, " ", tcod.BKGND_NONE)


def handle_keys():
    global player_x, player_y
    key = tcod.console_check_for_keypress()
    if key.vk == tcod.KEY_ENTER and tcod.KEY_ALT:
        tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
    elif key.vk == tcod.KEY_ESCAPE:
        return True

    if tcod.console_is_key_pressed(tcod.KEY_UP):
        player_y = player_y - 1
    elif tcod.console_is_key_pressed(tcod.KEY_DOWN):
        player_y = player_y + 1
    elif tcod.console_is_key_pressed(tcod.KEY_LEFT):
        player_x = player_x - 1
    elif tcod.console_is_key_pressed(tcod.KEY_RIGHT):
        player_x = player_x + 1


player = Object(player_x, player_y, "@", tcod.white)
npc = Object(player_x - 5, player_y, "@", tcod.yellow)
objects = [player, npc]


while not tcod.console_is_window_closed():
    tcod.console_set_default_background(con, tcod.white)
    for object in objects:
        object.draw()
        object.clear()

    tcod.console_flush()

    exit = handle_keys()

    if exit:
        break
