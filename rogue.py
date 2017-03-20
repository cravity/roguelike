# Author: cravity

import libtcodpy as libtcod

# Constant Variables:
# Actual size of window:
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
LIMIT_FPS = 20

class Object:
    # This is a generic object: The player, a monster, an item, the stairs...
    # It is always represented by a character on screen
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        # Move by the given amount
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

# Main Loop:
while not libtcod.console_is_window_closed():

    # draw all objects in the list
    for object in objects:
        object.draw()

    # Blit the contents of con to the root console and present it
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_flush()

    # Erase all objects at their old location, before they move
    for object in objects:
        object.clear()
    # handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break

