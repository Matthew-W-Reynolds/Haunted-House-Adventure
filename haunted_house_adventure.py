# -----------------------
# Haunted House Adventure
# -----------------------
#
# Microsoft BASIC Source Code taken from the book:
#     Title: Write your own Adventure Programs for your microcomputer")
#        By: Jenny Tyler and Les Howarth")
#      ISBN: 0 86020 741 2")
# Published by Usborne, 1983.
#
# PDF: https://colorcomputerarchive.com/repo/Documents/Books/Write%20Your%20Own%20Adventure%20Programs%20(1983)(Usborne).pdf
#
# Ported to Python by Matthew W. Reynolds, 31/03/2022
#
import mod_data
import mod_player
import random
import os
import msvcrt

# Initialise Game
#
def initialise_game():
    mod_player.player_room = mod_data.STARTING_ROOM
    mod_player.player_moves = 0
    mod_player.player_message = mod_data.DEFAULT_PLAYER_MESSAGE
    mod_player.player_quit = False

    mod_data.max_getable_items = 0
    for an_item in mod_data.items:
        if (mod_data.items[an_item][mod_data.IDX_ITEM_ROOM_NUMBER] >= 0):
            mod_data.max_getable_items += 1

    mod_data.max_rooms = len(mod_data.rooms)
    random.seed()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_game():
    clear_terminal()
    display_game_intro_credits()
    main_loop()

def end_game():
    print("\nGoodbye! Thanks for playing!!\n")

def display_game_intro_credits():
    print("")
    print("")
    print("Welcome to the Haunted House Adventure Game v1.0")
    print("Microsoft BASIC Source Code taken from the book:")
    print("")
    print("Title: Write your own Adventure Programs for your microcomputer")
    print("   By: Jenny Tyler and Les Howarth")
    print(" ISBN: 0 86020 741 2")
    print("Published by Usborne, 1983.")
    print("")
    print("PDF: https://colorcomputerarchive.com/repo/Documents/Books/Write%20Your%20Own%20Adventure%20Programs%20(1983)(Usborne).pdf")
    print("")
    print("Ported to Python by Matthew Reynolds, 31/03/2022")

def display_game_title():
    print("")
    print("-----------------------")
    print("Haunted House Adventure")
    print("-----------------------")
    print("")

def display_room_visible_items(room_index):
# Look for any items that are visible in the room and display them
#
    for item_key in mod_data.items:
        if (room_index == item_location(item_key)):
            if (is_item_visible(item_key) == True):
                you_can_see = "You can see a"
                if (item_key[0].upper() == "A"): you_can_see += "n"
                print(you_can_see + " " + item_key + " here.")

def display_room_exits(room_index):
# Display all exits in a readable format for the current room
#
    a_room = mod_data.rooms[room_index]
    the_exits = ""

    for a_direction in a_room[mod_data.IDX_ROOM_EXITS]:
        the_exits += mod_data.compass[a_direction] + ", "
    the_exits = rtrim(the_exits, 2)
    pt = the_exits.rfind(",")
    if (pt >= 0):
        the_exits = the_exits[0:pt] + " and" + the_exits[pt + 1:]

    if (the_exits[0] != "U" and the_exits[0] != "D"):
        str_exits_prefix = "to the "
    else:
        str_exits_prefix = ""

    print("")
    print("There are exits " + str_exits_prefix + the_exits)

def display_room_description(room_index):
    a_room = get_room_description(room_index)
    print("Your are " + mod_data.room_prefix[a_room[mod_data.IDX_ROOM_PREFIX]] + " the " + a_room[mod_data.IDX_ROOM_NAME])

def display_player_message():
    print("==========================")
    print("\n" + get_message())
    set_message(mod_data.DEFAULT_PLAYER_MESSAGE)

def get_room_description(room_index):
    if (room_index >= 0 and room_index < mod_data.max_rooms):
        return mod_data.rooms[room_index]
    else:
        return f"CRITICAL!!! Room Index = {room_index} Not Found!!!"

def get_player_input():
    cmd_line = input(mod_data.DEFAULT_GAME_PROMPT).strip()
    cli_verb, cli_item = lex_input(cmd_line)     # Returns 2 strings
    parse_input(cmd_line, cli_verb, cli_item)

def is_item_visible(an_item):
    return bool(mod_data.items[an_item][mod_data.IDX_ITEM_IS_VISIBLE])

def is_item_picked_up(an_item):
    return bool(mod_data.items[an_item][mod_data.IDX_ITEM_IS_PICKED_UP])

def item_location(an_item):
    return int(mod_data.items[an_item][mod_data.IDX_ITEM_ROOM_NUMBER])

def set_item_visibility(an_item, a_flag):
    mod_data.items[an_item][mod_data.IDX_ITEM_IS_VISIBLE] = bool(a_flag)

def room_idx():
    return int(mod_player.player_room)

def get_message():
    return str(mod_player.player_message)

def set_message(a_message):
    mod_player.player_message = a_message

def press_enter_to_continue():
    print("\nPress ENTER to continue...")
    while True:
        if msvcrt.kbhit():
            key_stroke = msvcrt.getch()
            if (key_stroke == b"\r"):
                break

def rtrim(a_string, amount):
# Cut 'amount' number of characters off the end of the string and return the result
#
    if (len(a_string) > amount):
        a_string = a_string[: -amount]
    return a_string

def lex_input(cmd_line):
    cli_verb = ""
    cli_item = ""

    pt = cmd_line.find(" ")
    if pt == -1:
# IF there is only 1 word entered by the player
#
        cli_verb = cmd_line
        cli_item = ""
    else:
# IF there is more than 1 word entered by the player
#
        cli_verb = cmd_line[: pt].lower()
        cli_item = cmd_line[pt + 1:].lower()

    return cli_verb, cli_item

# *************************************************************************************************
# The parser from the original BASIC source code was veerrrryy simple.
# It expects 2 words separated by a SPACE character.
# - First word is assumed to be a verb / verb, the second word is an item.
#
# If you enter more than that it might not understand you.
#
# An exception is made for certain verbs like help, inventory, quit, score and for moving around the game world.
# So for movement:
#   You can use go north, south, east, west for move in the for compass directions and up, down.
#   You can abbreviate that to just north, south, east, west, up, down and an exception is made for that.
#   You can abbreviate that even further to n, s, e, w, u, d.
#
# 1) It takes the string of input from the player
# 2) looks for a SPACE character
# 3) It then splits the string in two.
#   3.1) The characters before the " " go into a variable. This is assumed to be a verb
#   3.2) All the characters after the " " go into another variable. This is assumed to be an item
# 4) Checks the verb against the list of verbs the game understands stores the result in a variable
# 5) Checks the item against the list of items the game knows about, stores te result in a variable
# 6) Checks some error conditions
# 7) Executes the verb entered
# *************************************************************************************************
def parse_input(cmd_line, cli_verb, cli_item):
    bln_verb_found = False
    bln_item_found = False

# See if what the player entered makes sense so first we check for a matching VERB
#
    if cli_verb in mod_data.verbs:
        for a_verb in mod_data.verbs:
            if cli_verb == a_verb:
                bln_verb_found = True
                break

# Now we check if at least 2 words were entered and if that second word matches an ITEM
#
    if cli_item in mod_data.items:
        for an_item in mod_data.items:
            if cli_item == an_item:
                bln_item_found = True
                break

    if not check_error_messages_and_override_conditions(cmd_line, cli_verb, cli_item, bln_verb_found, bln_item_found):
        # No need to perform any more checks, lets jump back to the main loop
        #
        return
    else:
        if (cli_verb != "" and bln_verb_found == True):
            # If any of the movement verbs were entered then we deal with them separately
            #
            if (cli_verb in mod_data.movement_verbs or (cli_verb == "go")): # and cli_item in mod_data.movement_verbs)):
                cmd_movement(cli_verb, cli_item)
            else:
                # All other verbs are processed and the appropriate function is called here
                #
                str_function_name = 'cmd_' + cli_verb

                # Check if function requires an argument passed in
                #
                if (mod_data.verbs[cli_verb][mod_data.IDX_VERB_REQUIRES_ARGS] == True):
                    globals()[str_function_name](cli_item)
                else:
                    globals()[str_function_name]()

def check_error_messages_and_override_conditions(cmd_line, cli_verb, cli_item, bln_verb_found, bln_item_found):
    if (cli_item != "" and not bln_item_found):
        set_message("That's Silly! Did you take a knock to the head?")
    if (cli_item == ""):
        set_message("You must enter two words." + mod_data.VERB_NOT_UNDERSTOOD)
    if (not bln_verb_found and bln_item_found):
        set_message("You can't '" + cmd_line + "'")
    if (not bln_verb_found and not bln_item_found):
        set_message("You're not making any sense!")
    if (bln_verb_found and bln_item_found and is_item_picked_up(cli_item) == False):
        set_message("You can't do that. You're not carrying the '" + cli_item + "'")

    if (is_item_visible("bats") == False and room_idx() == 13 and random.randrange(1, 4) != 3 and (cli_verb[0] != "w" or (cli_verb == "go" and cli_item[0] != "w"))):
        set_message("Lookout - Bats are attacking!")
        return False
    if (room_idx() == 44 and random.randrange(1, 3) == 1 and is_item_visible("down") != False):
        set_item_visibility("ghosts", False)

    if mod_data.candle_light > 0: mod_data.candle_light -= 1
    if mod_data.candle_light < 1: mod_data.candle_light = -1
    if mod_data.candle_light == 10: set_message("Your candle is fickering and waning!")
    if mod_data.candle_light == 1: set_message("Your candle is out!")

    return True

def cmd_movement(cli_verb, cli_item):
# If the go verb was entered then set it to the direction specified
#
    if (cli_verb == "go"): 
        cli_verb = cli_item

# Get the first letter of the direction specified and convert it to upper case
#
    a_direction = str(cli_verb).upper()[0]

# If the player is in certain rooms and they've elected to move UP or DOWN then set the direction accordingly
# NOTE: The map for this game is stored in a single dimension arrary
    if (room_idx() == 20 and a_direction == "U"): a_direction = "N"
    if (room_idx() == 20 and a_direction == "D"): a_direction = "W"
    if (room_idx() == 22 and a_direction == "U"): a_direction = "W"
    if (room_idx() == 22 and a_direction == "D"): a_direction = "S"
    if (room_idx() == 36 and a_direction == "U"): a_direction = "S"
    if (room_idx() == 36 and a_direction == "D"): a_direction = "N"

# Check some override conditions
#
    if (room_idx() == 7 and is_item_visible("rope") == True):
        set_message("CRASH! You fell out of the tree!")
        set_item_visibility("rope", False)
        return
 
    if (is_item_visible("ghosts") == True and room_idx() == 52):
        set_message("The Ghosts will not let you move!")
        return
 
    if (room_idx() == 45 and is_item_picked_up("painting") == True and is_item_visible("down") == False):
        set_message("There's a magical barrier to the west!")
        return
    
    if ((room_idx() == 26 and mod_data.candle_is_lit == True) and (a_direction == "N" or a_direction == "E")):
        set_message("It's too dark! You need a light!")
        return
    
    if (room_idx() == 54 and is_item_picked_up("boat") != True):
        if (random.randrange(1, 4) == 3):
            set_message("You're stuck!")
            return
        else:
            if (get_message() == "You're stuck!"):
                set_message("You broke free!")

    if (is_item_picked_up("boat") == True and (room_idx() == 53 or room_idx() == 54 or room_idx() == 55 or room_idx() == 47)):
        set_message("You can't carry a boar!")
        return
    
    if ((room_idx() > 26 and room_idx() < 30) and mod_data.candle_is_lit == False):
        set_message("It's too dark to move!")
        return
    
# Check if the direction entered is a valid exit from the room
# If the exit entered by the player isn't available from this room
#
    room_exits = mod_data.rooms[room_idx()][mod_data.IDX_ROOM_EXITS]
    if (a_direction not in room_exits):
        set_message("Go where? You can't that way.")
        return

    potential_direction = 0
    if (a_direction == "N"): 
        potential_direction = room_idx() - 8
        if (potential_direction < 0): return
        mod_player.player_room = potential_direction
    if (a_direction == "S"):
        potential_direction = room_idx() + 8
        if (potential_direction >= mod_data.max_rooms): return
        mod_player.player_room = potential_direction
    if (a_direction == "W"):
        potential_direction = room_idx() - 1
        if (potential_direction < 0): return
        mod_player.player_room = potential_direction
    if (a_direction == "E"):
        potential_direction = room_idx() + 1
        if (potential_direction >= mod_data.max_rooms): return
        mod_player.player_room = potential_direction
    
    mod_player.player_moves += 1
    set_message(mod_data.DEFAULT_PLAYER_MESSAGE)

    if (room_idx() == 41 and is_item_visible("up") == True):
        mod_data.rooms[49][mod_data.IDX_ROOM_EXITS] = "SW"
        set_message("The door slams shut!")
        set_item_visibility("up", False)

# *****************************************************************************
# Player Verb Functions
# *****************************************************************************
def cmd_quit():
    mod_player.player_quit = True
    cmd_score()

def cmd_score():
    carrying_count = 0
    for an_item in mod_data.items:
        if (is_item_picked_up(an_item) == True): carrying_count += 1
    a_score = carrying_count

    print("")
    if (a_score == 17 and is_item_picked_up("boat") == False and room_idx() != mod_data.STARTING_ROOM):
        print("You have picked up everything!")
        print("Return to the " + get_room_description(mod_data.STARTING_ROOM) + " for the final score!")

    if (a_score == 17 and room_idx() == mod_data.STARTING_ROOM):
        a_score = a_score * 2

    print(f"Your score is: {a_score}. You've found {carrying_count} items (out of {mod_data.max_getable_items - 1})")
    print(f"And you've done this in {mod_player.player_moves} moves")

    set_message(mod_data.DEFAULT_PLAYER_MESSAGE)

    if (room_idx() == mod_data.STARTING_ROOM and a_score > 18):
        print("\nYou've beaten the game! Well Done!!")
        mod_player.player_quit = True

    if (mod_player.player_quit == False): press_enter_to_continue()

def cmd_help(a_verb):
    print("")

    if (a_verb == ""):
        all_verbs = ""
        for verb in mod_data.verbs:
            all_verbs += verb + ", "
        all_verbs = rtrim(all_verbs, 2)

        print("Verbs I know:")
        print(all_verbs)
    else:
        if (a_verb in mod_data.verbs):
            print("USAGE: " + mod_data.verbs[a_verb][mod_data.IDX_VERB_DESCRIPTION] + ".")
        else:
            print("I don't understand '" + a_verb + "'" + mod_data.VERB_NOT_UNDERSTOOD)

    set_message(mod_data.DEFAULT_PLAYER_MESSAGE)
    press_enter_to_continue()

def cmd_inventory():
    the_inventory = ""
    for an_item in mod_data.items:
        if (is_item_picked_up(an_item) == True):
            the_inventory += an_item + ", "

    the_inventory = rtrim(the_inventory, 2)
    if (the_inventory == ""):
        the_inventory = "Empty."

    print("")
    print("Your Inventory:")
    print(the_inventory)
    set_message(mod_data.DEFAULT_PLAYER_MESSAGE)
    press_enter_to_continue()

def cmd_take(an_item):
    cmd_get(an_item)

def cmd_grab(an_item):
    cmd_get(an_item)

def cmd_get(an_item):
    if (an_item not in mod_data.items):
        set_message("You can't get '" + an_item + "'")
    else:
        dict_item = mod_data.items[an_item]
        if (int(dict_item[mod_data.IDX_ITEM_ROOM_NUMBER]) != room_idx()):
            set_message("The '" + an_item + "' isn't here")
            return
        if (dict_item[mod_data.IDX_ITEM_IS_VISIBLE] != True):
            set_message("What '" + an_item + "'?")
            return
        if (dict_item[mod_data.IDX_ITEM_IS_PICKED_UP] == True):
            set_message("You are already carrying the '" + an_item + "'")
            return
        
        # Set the item to be picked up and move it out of range of all the rooms
        # The BASIC code set the room number, not sure why
        #
        mod_data.items[an_item][mod_data.IDX_ITEM_IS_PICKED_UP] = True
        mod_data.items[an_item][mod_data.IDX_ITEM_ROOM_NUMBER] = 999
        set_message("You have the '" + an_item + "'")

def cmd_open(an_item):
    if (room_idx() == 43 and (an_item == "drawer" or an_item == "desk")):
        set_item_visibility("candle", True)
        set_message("Drawer open!")

    if (room_idx() == 28 and an_item == "door"):
        set_message("Its locked!")
    
    if (room_idx() == 38 and an_item == "coffin"):
        set_message("That's creepy!")
        set_item_visibility("ring", False)

def cmd_look(an_item):
    cmd_examine(an_item)

def cmd_examine(an_item):
    if (room_idx() == 32 and an_item == "coat"):
        set_item_visibility("key", True)
        set_message("There's something here!")
    
    if (room_idx() == 3 and an_item == "rubbish"):
        set_message("That's disgusting!")
    
    if (room_idx() == 43 and (an_item == "drawer" or an_item == "desk")):
        set_message("There is a drawer!")

    if ((room_idx() == 13 and an_item == "scroll") or (room_idx() == 42 and an_item == "books")):
        cmd_read(an_item)
    
    if (room_idx() == 43 and an_item == "wall"):
        set_message("There is something beynnd...")

    if (room_idx() == 38 and an_item == "coffin"):
        cmd_open(an_item)

def cmd_read(an_item):
    if (room_idx() == 42 and an_item == "books"):
        set_message("They are demonic works!")
    
    if ((an_item == "magic spells" or an_item == "spells") and is_item_picked_up("magic spells") == True and is_item_visible("xzanfar") == False):
        set_message("Use this word with care 'xzanfar'")

    if (an_item == "scroll" and is_item_picked_up("scroll") == True):
        set_message("The script is in an alien tongue!")

def cmd_say(a_word):
    set_message("Ok '" + a_word + "'")

    if (is_item_picked_up("magic spells") == True and a_word == "xzanfar"):
        set_message("* Magic Occurs *")
        if (room_idx() != 45):
            mod_player.player_room = random.randrange(0, 64)
        else:
            set_item_visibility("xzanfar", True)

def cmd_dig():
    if (is_item_picked_up("shovel") == True):
        set_message("You made a hole")
        if (room_idx() == 30):
            set_message("You dug the bars out!")
            mod_data.rooms[room_idx()][mod_data.IDX_ROOM_NAME] = "Cellar With A Hole in the Wall"
            mod_data.rooms[room_idx()][mod_data.IDX_ROOM_EXITS] = "NSE"

def cmd_swing(an_item):
    if (is_item_picked_up("rope") == False and room_idx() == 7):
        set_message("This is no time to play games")

    if (is_item_picked_up("rope") == True and an_item == "rope"):
        set_message("You swung it")

    if (is_item_picked_up("axe") == True and an_item == "axe"):
        set_message("Whoosh!")
        if (room_idx() == 43):
            mod_data.rooms[room_idx()][mod_data.IDX_ROOM_NAME] = "Study With Desk & a Secret Room"
            mod_data.rooms[room_idx()][mod_data.IDX_ROOM_EXITS] = "WN"
            set_message("You broke through the thin wall!")

def cmd_climb(an_item):
    if (an_item == "rope"):
        if (is_item_picked_up(an_item) == True):
            set_message("It isn't attached to anything!")
        else:
            if (room_idx() == 7):
                if (is_item_visible(an_item) == False):
                    set_message("You see a thick forest and then a cliff to the south")
                    set_item_visibility(an_item, True)
                else:
                    set_message("Going down")
                    set_item_visibility(an_item, False)

def cmd_light(an_item):
    if (an_item == "candle" and is_item_picked_up("candle") == True):
        if (is_item_picked_up("candlestick") == False):
            set_message("It will burn your hands!")
        if (is_item_picked_up("matches") == False):
            set_message("You have nothing to light it with")
        if (is_item_picked_up("candlestick") == True and is_item_picked_up("matches") == True):
            set_message("It casts a flickering light")
            mod_data.candle_is_lit = True

def cmd_unlight(an_item):
    cmd_extinquish(an_item)

def cmd_douse(an_item):
    cmd_extinquish(an_item)

def cmd_extinquish(an_item):
    if (an_item == "candle"):
        if (mod_data.candle_is_lit == True):
            set_message("Extinquished")
            mod_data.candle_is_lit = False

def cmd_spray(an_item):
    # 26=bats, 16=aerosol
    if (an_item == "bats" and is_item_picked_up("aerosol") == True):
        set_message("HISSSSS!")
        if (is_item_visible("bats") == True):
            set_item_visibility("bats", False)
            set_message("PFFT! Got them!")

def cmd_use(an_item):
    if (an_item == "vacuum" and is_item_picked_up("vacuum") == True and is_item_picked_up("batteries") == True):
        set_message("You switch on the vacuum")
        set_item_visibility("down", True)
    if (an_item == "ghosts" and is_item_visible("ghosts") == True and is_item_visible("down") == True):
        set_message("Whizz - Vacuumed the Ghosts up!")
        set_item_visibility("ghosts", False)

def cmd_unlock(an_item):
    if (room_idx()  == 43 and (an_item == "ghosts" or an_item == "drawer")):
        cmd_open(an_item)
    if (room_idx() == 28 and an_item == "door" and is_item_visible("door") == False and is_item_picked_up("key") == True):
        set_item_visibility("door", True)
        mod_data.rooms[room_idx()][mod_data.IDX_ROOM_EXITS] = "SEW"
        mod_data.rooms[room_idx()][mod_data.IDX_ROOM_NAME] = "Hall By A Thick Wooden Open Door"
        set_message("The key turns!")

def cmd_leave(an_item):
    cmd_drop(an_item)

def cmd_drop(an_item):
    if (is_item_picked_up(an_item) == True):
        mod_data.items[an_item][mod_data.IDX_ITEM_IS_PICKED_UP] = False
        mod_data.items[an_item][mod_data.IDX_ITEM_ROOM_NUMBER] = room_idx()
        set_message("Done")

def main_loop():
    while not mod_player.player_quit:
        display_game_title()
        display_room_description(room_idx())
        display_room_visible_items(room_idx())
        display_room_exits(room_idx())
        display_player_message()
        if (not mod_player.player_quit): get_player_input()

# Entry Point
#
if __name__ == "__main__":
    initialise_game()
    start_game()
    end_game()
