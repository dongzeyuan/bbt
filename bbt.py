import time
import tcod


# setup the font
tcod.console_set_custom_font('bbt\\fonts\\arial10x10.png',
                             tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD,)

# initialize the root console in a context.
tcod.console_init_root(80,60,"title",False)

while not tcod.console_is_window_closed():
    tcod.console_set_default_foreground(0,tcod.white)
    tcod.console_put_char(0,1,1,"@",tcod.BKGND_NONE)
    tcod.console_flush()