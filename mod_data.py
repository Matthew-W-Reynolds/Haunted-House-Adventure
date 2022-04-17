# Haunted House Adventure - DATA
# Written by Matthew Reynolds, 31/03/2022
#
# BASIC Arrays
#
# mod_data.rooms
#   D$ = Room Names (0..63)
#   R$ = Room Exits (0..63)
#
# O$ = Items (1..W)
#   L  = Room Numbers (Locations) for Items (1..G) G for "gettable" items. 0 is a *SPECIAL* item
#   F  = Flags for all Items. Indicates status (Visible or not, Normal or not) so 0: Visible, Normal, 1: Hidden, Altered, or On / Off
#   C  = Holds "gettable" Items that have been picked up the player
#
# mod_data.verbs:
#   V$ = Verbs (0..V)
# 

# Some starting values
#
STARTING_ROOM = 57
DEFAULT_PLAYER_MESSAGE = "Ok"
DEFAULT_GAME_PROMPT = "\nWhat will you do now? "
VERB_NOT_UNDERSTOOD = ".\nType 'help' for list of verbs I understand."

# Verbs key is the verb itself
#
IDX_VERB_REQUIRES_ARGS = 0
IDX_VERB_DESCRIPTION = 1

# rooms key is the Room Number
#
IDX_ROOM_NAME = 0
IDX_ROOM_EXITS = 1
IDX_ROOM_PREFIX = 2
IDX_ROOM_DESCRIPTION = 3

# items key is the Item Name
#
IDX_ITEM_ROOM_NUMBER = 0
IDX_ITEM_IS_VISIBLE = 1
IDX_ITEM_IS_PICKED_UP = 2
IDX_ITEM_DESCRIPTION = 3

candle_is_lit = False
candle_light = -1
max_getable_items = 0
max_rooms = 0

movement_verbs = (
    "n", "north", "s", "south", "w", "west", "e", "east", "u", "up", "d", "down"
)

# verbs DICTIONARY
#   key = verb
#   Verb Index 0 = Does this verb require an argument
#   Verb Index 1 = Detailed help description for this verb
# 
verbs = {
    "help" : [True, "help | help <command> - Shows a list of all commands or details of a particular command"],
    "inventory" : [False, "inventory - Shows everything the player is carrying"],
    "carrying" : [False, "carrying - Shows everything the player is carrying"],
    "go" : [True, "go <direction> - Move in desired direction"],
    "n" : [False, "n - Move North"],
    "north" : [False, "north - Move North"],
    "s" : [False, "s - Move South"],
    "south" : [False, " - Move South"],
    "w" : [False, "w - Move West"],
    "west" : [False, "west - Move West"],
    "e" : [False, "e - Move East"],
    "east" : [False, "east - Move East"],
    "u" : [False, "u - Move Up"],
    "up" : [False, "up - Move Up"],
    "d" : [False, "d - Move Down"],
    "down" : [False, "down - Move Down"],
    "get" : [True, "get <item> - Pick up and carry an item"],
    "take" : [True, "take <item> - Pick up and carry an item"],
    "grab" : [True, "grab <item> - Pick up and carry an item"],
    "open" : [True, "open <item> - Open an item"],
    "look" : [True, "look <item> - Eexamine an item"],
    "examine" : [True, "examine <item> - Eexamine an item"],
    "read" : [True, "read <item> - Read an item"],
    "say" : [True, "say <word> - Say a word out loud"],
    "dig" : [False, "dig - Dig a hole"],
    "swing" : [True, "swing <item> - Swings an item"],
    "climb" : [True, "climb <item> - Climb something"],
    "light" : [True, "light <item> - Light an item"],
    "unlight" : [True, "unlight <item> - Extinguish an item"],
    "douse" : [True, "douse <item> - Extinguish an item"],
    "extinquish" : [True, "extinguish <item> - Extinguish an item"],
    "spray" : [True, "spray <item> - Spray something"],
    "use" : [True, "use <item> - Use an item"],
    "unlock" : [True, "unlock <item> - Unlock something"],
    "drop" : [True, "drop <item> - Drop an item"],
    "leave" : [True, "leave <item> - Drop an item"],
    "quit" : [False, "quit - Quit the game"],
    "score" : [False, "score - Display the players current score"]
}

room_prefix = ("by", "on", "in", "at", "Beneath")

# rooms DICTIONARY
#   key = room number
#   List Index 0 = room name
#   List Index 1 = room exits
#   List Index 2 = room name prefix
#   List Index 3 = room description
#
rooms = {
     0 : ["Dark Corner", "SE", 0, ""],
     1 : ["Overgrown Garden", "WE", 1, ""],
     2 : ["Large Woodpile", "WE", 0, ""],
     3 : ["Yard By Rubbish", "SWE", 2, ""],
     4 : ["Weedpatch", "WE", 2, ""],
     5 : ["Forest", "WE", 2, ""],
     6 : ["Thick Forest", "SWE", 2, ""],
     7 : ["Blasted Tree", "WS", 0, ""],

     8 : ["Corner Of House", "NS", 3, ""],
     9 : ["Entrance To Kitchen", "SE", 2, ""],
    10 : ["Kitchen & Grimy Cooker", "WE", 2, ""],
    11 : ["Scullery Door", "NW", 0, ""],
    12 : ["Room With Inches Of Dust", "SE", 2, ""],
    13 : ["Rear Turret Room", "W", 2, ""],
    14 : ["Clearing By House", "NE", 2, ""],
    15 : ["Grassy Path", "NSW", 1, ""],

    16 : ["West Side Of The House", "NS", 0, ""],
    17 : ["Back Of The Hallway", "NS", 2, ""],
    18 : ["Dark Alcove", "SE", 2, ""],
    19 : ["Small Dark Room", "WE", 2, ""],
    20 : ["Bottom Of A Spiral Staircase", "NWUD", 3, ""],
    21 : ["Wide Passage", "SE", 2, ""],
    22 : ["Slippery Steps", "WSUD", 1, ""],
    23 : ["Clifftop", "NS", 1, ""],

    24 : ["Crumbling Wall", "N", 0, ""],
    25 : ["Gloomy Passage", "NS", 2, ""],
    26 : ["Pool Of Light", "NSE", 2, ""],
    27 : ["Impressive Vaulted Hallway", "WE", 2, ""],
    28 : ["Hall By A Thick Wooden Door", "WE", 2, ""],
    29 : ["Trophy Room", "NSW", 2, ""],
    30 : ["Cellar With A Barred Window", "NS", 2, ""],
    31 : ["Cliff Path", "NS", 1, ""],

    32 : ["Cupboard With a Hanging Coat", "S", 2, ""],
    33 : ["Front Hall", "NSE", 2, ""],
    34 : ["Sitting Room", "NSW", 2, ""],
    35 : ["Secret Room", "S", 2, ""],
    36 : ["Steep Marble Stairs", "NSUD", 1, ""],
    37 : ["Dining Room", "N", 2, ""],
    38 : ["Deep Cellar With A Coffin", "N", 2, ""],
    39 : ["Cliff Path", "NS", 1, ""],

    40 : ["Closet", "NE", 2, ""],
    41 : ["Front Lobby", "NW", 2, ""],
    42 : ["Library Of Evil Books", "NE", 2, ""],
    43 : ["Study With Desk & Hole In Wall", "W", 2, ""],
    44 : ["Damp Cobwebby Room", "NSE", 2, ""],
    45 : ["Very Cold Chamber", "WE", 2, ""],
    46 : ["Spooky Room", "N", 2, ""],
    47 : ["Cliff Path By Marsh", "NS", 1, ""],

    48 : ["Rubble Strewn Verandah", "SE", 1, ""],
    49 : ["Front Porch", "NSW", 1, ""],
    50 : ["Front Tower", "E", 2, ""],
    51 : ["Sloping Corridor", "WE", 2, ""],
    52 : ["Upper Gallery", "NW", 2, ""],
    53 : ["Marsh By Wall", "S", 2, ""],
    54 : ["Marsh", "SW", 2, ""],
    55 : ["Soggy Path", "NW", 1, ""],

    56 : ["Twisted Railing", "NE", 0, ""],
    57 : ["Path Through The Iron Gate", "NWE", 1, ""],
    58 : ["Railings", "WE", 0, ""],
    59 : ["Front Tower", "WE", 4, ""],
    60 : ["Debris From Crumbling Facade", "WE", 0, ""],
    61 : ["Large Fallen Brickwork", "NWE", 0, ""],
    62 : ["Rotting Stone Arch", "NWE", 0, ""],
    63 : ["Crumbling Clifftop", "W", 1, ""]
}

# items DICTIONARY
#   key = item name
#   List Index 0 = item room index
#   List Index 1 = is item visible
#   List Index 2 = is the player carring the item
#   List Index 3 = item description
#
# NOTE: An Item is "getable" is the item room index >= 0, if -1 then you can't get it
#       The BASIC source code used a 0 indexed array with a special NOT FOUND item at position 0.
#       So all items are essentially start at 1 in the index
#
items = {
    "painting" : [46, True, False, ""],
    "ring" : [38, False, False, ""],
    "magic spells" : [35, True, False, ""],
    "goblet" : [50, True, False, ""],
    "scroll" : [13, True, False, ""],
    "coins" : [18, True, False, ""],
    "statue" : [28, True, False, ""],
    "candlestick" : [42, True, False, ""],
    "matches" : [10, True, False, ""],
    "vacuum" : [25, True, False, ""],
    "batteries" : [26, True, False, ""],
    "shovel" : [4, True, False, ""],
    "axe" : [2, True, False, ""],
    "rope" : [7, True, False, ""],
    "boat" : [47, True, False, ""],
    "aerosol" : [60, True, False, ""],
    "candle" : [43, False, False, ""],
    "key" : [32, False, False, ""],
    "north" : [-1, True, False, ""],
    "south" : [-1, True, False, ""],
    "west" : [-1, True, False, ""],
    "east" : [-1, True, False, ""],
    "up" : [-1, True, False, ""],
    "down" : [-1, False, False, ""],
    "door" : [-1, True, False, ""],
    "bats" : [-1, False, False, ""],
    "ghosts" : [-1, True, False, ""],
    "drawer" : [-1, False, False, ""],
    "desk" : [-1, True, False, ""],
    "coat" : [-1, True, False, ""],
    "rubbish" : [-1, True, False, ""],
    "coffin" : [-1, True, False, ""],
    "books" : [-1, True, False, ""],
    "xzanfar" : [-1, False, False, ""],
    "wall" : [-1, True, False, ""],
    "spells" : [-1, True, False, ""]
}

compass = {
    "N" : "North",
    "S" : "South",
    "W" : "West",
    "E" : "East",
    "U" : "Up",
    "D" : "Down"
}