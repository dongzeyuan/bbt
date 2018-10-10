import libtcodpy as tcod

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMITS_FPS = 30
player_x = (SCREEN_WIDTH // 2)
player_y = (SCREEN_HEIGHT // 2)

font_path = 'D:\code\BBT\\fonts\\arial10x10.png'
font_flags = tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
tcod.console_set_custom_font(font_path, font_flags)

window_title = 'Bored Battle Theater'
fullscreen = False
tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, window_title, fullscreen)
con = tcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
tcod.sys_set_fps(LIMITS_FPS)


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


while not tcod.console_is_window_closed():
    tcod.console_set_default_background(0, tcod.white)
    tcod.console_put_char(0, player_x, player_y, '@', tcod.BKGND_NONE)
    tcod.console_flush()
    tcod.console_put_char(0, player_x, player_y, ' ', tcod.BKGND_NONE)
    exit = handle_keys()

    if exit:
        break
