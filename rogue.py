# Author: cravity

import libtcodpy as libtcod

# Constant Variables:
# Actual size of window:
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

# Size of the map
MAP_WIDTH = 80
MAP_HEIGHT = 45

LIMIT_FPS = 20

color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)

class Tile:
    # A tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class Rect:
    # A rectangle on the map. Used to characterize a room
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

class Object:
    # This is a generic object: The player, a monster, an item, the stairs...
    # It is always represented by a character on screen
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        # Move by the given amounta if the destination is not blocked
        if not map[self.x + dx][self.y + dy].blocked:
            self.x += dx
            self.y += dy

    def draw(self):
        # set the color, then draw this character at its position
        libtcod.console_set_default_foreground(con, self.color)
        libtcod.console_put_char(
            con, self.x, self.y, self.char, libtcod.BKGND_NONE)

    def clear(self):
        # erase the character that represents this object
        libtcod.console_put_char(con, self.x, self.y, ' ', libtcod.BKGND_NONE)

def make_map():
    global map

    # fill map with "unblocked" tiles
    map = [[ Tile(False)
        for y in range(MAP_HEIGHT) ]
           for x in range(MAP_WIDTH) ]

    # Add two pillars as test
    map[30][22].blocked = True
    map[30][22].block_sight = True
    map[30][21].blocked = True
    map[30][21].block_sight = True
    map[30][20].blocked = True
    map[30][20].block_sight = True
    map[50][22].blocked = True
    map[50][22].block_sight = True

def render_all():
    global color_light_wall
    global color_light_ground

    # go through all tiles and set their backround color
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = map[x][y].block_sight
            if wall:
                libtcod.console_put_char_ex(
                    con, x, y, "#", libtcod.white, libtcod.black)
            else:
                libtcod.console_put_char_ex(
                    con, x, y, ".", libtcod.white, libtcod.black)

    # Draw all objects in the list
    for object in objects:
        object.draw()

    # Blit the contents of con to the root console and present it
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

def handle_keys():
    key = libtcod.console_wait_for_keypress(True)
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt + Enter toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return True # exit game

    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0, -1)

    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1)

    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)

    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0)



# Objects
#### START OF GAME CODE ###

# Set Font:
libtcod.console_set_custom_font(
    'arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
# Window Initilazing:
libtcod.console_init_root(
    SCREEN_WIDTH, SCREEN_HEIGHT, 'Alice in Wonderland (WIP)', False)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

# Create an object representing the player
player = Object(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, "@", libtcod.white)

# Create an NPC
npc = Object(SCREEN_WIDTH/2 - 5, SCREEN_HEIGHT/2, "@", libtcod.yellow)

objects = [npc, player]

# generate map ( at this point it's not drawn on the screen )
make_map()

# Main Loop:
while not libtcod.console_is_window_closed():

    # render the screen
    render_all()

    libtcod.console_flush()

    # Erase all objects at their old location, before they move
    for object in objects:
        object.clear()
    # handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break

