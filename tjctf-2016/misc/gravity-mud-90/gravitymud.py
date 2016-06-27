import time

print("Good Enough Entertainment Inc. presents")
print("GRAVITYMUD")
print()
print("*not actually multi-user")
print()
print()

roommap = {

"giftshop": {
    "north": "forest",
    "up": "attic-hallway"
},

"attic-hallway": {
    "east": "atticroom1",
    "west": "atticroom2"
},

"forest": {
    "north": "almost-town"
},

"almost-town": {
    "north": "street1"
},

"street1": {
    "west": "library",
    "east": "museumofhistory",
    "north": "street2"
},

"museumofhistory": {
    "east": "exhibithall"
},

"street2": {
    "north": "street3"
},

}

descriptions = {

"giftshop": """\
The first floor of the Mystery Shack consists of a gift shop with numerous
novelties.""",

"attic-hallway": """\
The second floor of the Mystery Shack is an attic with a few rooms.""",

"almost-town": """\
You're not quite in the forest, but you're not quite in town either. You can
see buildings in the distance, to the north.""",

"forest": """\
You are in a forest. You can see the Mystery Shack to the south.""",

"street1": """\
You're in a town. To the east and west are buildings.""",

"library": """\
You're standing in a library, surrounded by books.""",

"museumofhistory": """\
You're standing in the Museum of History, surrounded by exhibits. There is an
exhibit hallway to the east.""",

"exhibithall": """\
You are surrounded by visual documentation of this town's past. None of it seems
to be recent. Also a lot of eyes are mounted on the wall.""",

"street2": """\
You are in a town. There must once have been buildings to the west and east, but
they are in ruins now.""",

"street3": """\
You are in town. The forest isn't visible from here. There is nothing interesting here.""",

"meetingroom": """\
You are in a room that appears to be hundreds of years older than the rest of
the building. Several pnuematic tubes are mounted to the ceiling, and an eye
with a cross through it is drawn on the wall opposite you. You feel like someone
is watching you. On a table is a book.""",

"atticroom1": """\
It's a room in the attic. There appears to be something written on the wall.""",

"atticroom2": """\
It's a mostly empty room."""
}

items = {
"giftshop": ["rug", "eyeballjar", "cashregister"],
"attic-hallway": [],
"forest": ["paper"],
"almost-town": ["tree"],
"street1": ["lamppost"],
"street2": [],
"street3": [],
"library": ["journal2"],
"museumofhistory": [],
"exhibithall": ["fireplace", "paintedeye"],
"meetingroom": ["book"],
"atticroom1": ["wall"],
"atticroom2": ["uvlight"]
}

itemdesc = {
"rug": """\
You always knew Grunkle Stan kept his arrest warrants under the rug, but you
didn't know that he kept parts of his flag under the rug:

tjctf{y0u_m1ght_h@v3_""",

"cashregister": """\
There sure is a lot of money in here.""",

"eyeballjar": """\
Ick, it's a jar with a floating eyeball inside.""",

"journal2": """\
This book appears to have a gold six-fingered hand glued to the front, with the
number "2" written on it. The book looks strangely familiar, but you can't seem
to place it. You feel that it is out of place. You flip through the pages, and
note some interesting text towards the end:

b33n_m1$sing_t3h_

There is also a section on cryptography. You memorize it, just in case.""",

"fireplace": """\
This fireplace looks rather suspicious.""",

"paintedeye": """\
This eye is painted on a part of the wall that is outset from the rest. You
try to push it into the wall, and the fireplace is replaced with a staircase!""",

"book": """\
It's just a regular book.

Wait, no it's not. You flip through the pages, and see some odd text. It seems
to be encoded with some strange scheme...""",

"paper": """\
It looks like a blank piece of paper. Upon closer inspection, you can barely
read some text. It looks like part of a flag, written in invisible ink. If
only you had something to read it with...
""",

"wall": """\
There is text etched into the wall:

TRUST NOONE""",

"uvlight": """\
An ultraviolet light source."""
}

roomnames = {"giftshop": "Mystery Shack Gift Shop", "attic-hallway": "Mystery Shack Attic",
             "forest": "Forest", "almost-town": "Clearing", "street1": "Town", "street2": "Town",
             "street3": "Town", "library": "Library", "museumofhistory": "Museum of History",
             "exhibithall": "Exhibit Hall", "meetingroom": "Meeting Room", "atticroom1": "Attic room",
             "atticroom2": "Attic room"}
skills = {"cryptography": False}
startroom = "almost-town"


def replace_fireplace_with_staircase():
    if "fireplace" in items["exhibithall"]:
        items["exhibithall"].remove("fireplace")
    roomexits["exhibithall"]["down"] = "meetingroom"
    roomexits["meetingroom"]["up"] = "exhibithall"

def give_crypto_knowledge():
    itemdesc["book"] += """
Fortunately, the knowledge of cryptography you gained from reading the strange
book with the gold hand lets you decode it. It says:
    
SOMETHING IS HIDDEN IN THE TREE IN THE CLEARING"""
    print("You have gained the cryptography skill!")
    skills["cryptography"] = True

def discover_tree():
    if not skills["cryptography"]:
        return
    itemdesc["tree"] = """You wouldn't think to check here without reading that book...
The tree looks metallic and dusty. You see what looks to be a door in the tree.
Inside the tree is what appears to be a control box. You flip some switches,
but nothing happens. Upon closer examination of the control box, you see strange
writing. Good thing you know cryptography. It says:
    
fl4g_but_"""

def take_uvlight():
    itemdesc["paper"] += "\nAha! You shine the UV light on the paper, and read:\n\nYOUR_A1M_IS_G3TT1NG_B3TT3R}"
    items["atticroom2"] = []
    print("You take the UV light.")

itemhooks = {"paintedeye": replace_fireplace_with_staircase,
        "journal2": give_crypto_knowledge, "book": discover_tree, "uvlight": take_uvlight}

##
roomexits = {}
dirmap = {"north": "south", "south": "north", "east": "west", "west": "east", "up": "down", "down": "up"}

for room in descriptions:
    roomexits[room] = {}

for room in roommap:
    roomexits[room].update(roommap[room])
    for direction, destroom in roomexits[room].items():
        roomexits[destroom][dirmap[direction]] = room

room = startroom
for turn in range(50):
    print(50 - turn, "turns remain")
    print("You are currently in: {}".format(roomnames[room]))
    print()
    print(descriptions[room])
    print()
    if items[room]:
        print("Here you see {}.".format(", ".join(items[room])))
    print("Exits: {}".format(", ".join(list(roomexits[room].keys()))))

    st = time.time()
    command = input("> ").split(maxsplit=1)
    if time.time() - st > 0.5:
        print("Too slow!")
        exit()

    if len(command) == 1:
        command, arg = command[0], ""
    elif len(command) == 2:
        command, arg = command
    else:
        print("Invalid command.")
        exit()

    if command in dirmap:
        if command in roomexits[room]:
            room = roomexits[room][command]
        else:
            print("There is no exit that way.")
    elif command == "examine":
        if arg in items[room]:
            if arg in itemdesc:
                print(itemdesc[arg])
            else:
                print("It's just a regular {}.".format(arg))
            if arg in itemhooks:
                itemhooks[arg]()
        else:
            print("I don't see any of those around here.")
    else:
        print("Unknown command")
