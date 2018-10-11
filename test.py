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


if __name__ == "__main__":
    make_map()
    pprint.pprint(game_map[0][3])
    
