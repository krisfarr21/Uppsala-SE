import argparse
import sys
import random

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()


def generic_error():
    print('Something went wrong :( Try \'commands\'')


# ________________________________________________________

# ROOM

class Room:
    def __init__(self, name):
        self.name = name
        self.items = dict()
        self.doors = dict()

    # FOR DEBUGGING
    def print_room(self):
        print(self.name)

    # FOR DEBUGGING
    def info(self):
        room_info = dict()
        room_info['Room'] = self.name
        room_info['Doors'] = ', '.join(self.doors.keys())
        room_info['Items'] = ', '.join(self.items.keys())
        return room_info

# DOOR____________________________


class Door:
    def __init__(self, dirc, status, current, next):
        self.dirc = dirc
        self.status = status
        self.current = current
        self.next = next

    # FOR DEBUGGING
    def print_door(self):
        print(self.dirc, self.status, self.current, self.next)

# ITEM____________________________


class Item:
    def __init__(self, name, location, species, usage=''):
        # species == type
        self.name = name
        self.location = location
        self.species = species
        self.usage = usage

    # FOR DEBUGGING
    def print_item(self):
        print(self.name, self.location, self.species, self.usage)

# HOUSE____________________________


class House:
    def __init__(self, rooms={}):
        # using dictionaries because that way is much easier to access the room one wants
        self.rooms = rooms

    def add_room(self, room_o):
        # it adds room object (with name, items and doors as attr)
        if room_o.name in self.rooms:
            return generic_error()
        else:
            self.rooms[room_o.name] = room_o
    
    # FOR DEBUGGING
    def print_house(self):
        return self.rooms.keys()
    
    # FOR DEBUGGING
    def info(self):
        for key in self.rooms:
            print(self.rooms[key].info())

# PLAYER____________________________


class Player:
    def __init__(self, position='Kitchen', name='Bob'):
        self.position = position
        self.items = dict()
        self.name = name
        self.standing = True


class Game:
    COMMANDS = ['quit', 'go', 'take', 'drop', 'sit', 'commands', 'show', 'where_at', 'holds', 'item_info', 'unlock',
                'open', 'play', 'easter', 'change_name', 'stand', 'mirror', 'drop_all', 'read']
    
    def __init__(self, filename):
        self.filename = filename
        self.house = House()
        hello_message = "Welcome to the game!" + '\n' + 'To proceed in this game give input and press enter.'

        house = self.house
        with open(self.filename, mode='r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                command, data = line.split(' ', 1)
                data = data.strip()
                if command == 'room':
                    room = Room(data)
                    house.add_room(room)
                else:
                    data = data.split(' ')
                    if command == 'item':
                        if len(data) == 3:
                            item = Item(data[0], data[1], data[2])
                        else:
                            item = Item(data[0], data[1], data[2], data[3])
                        if item.location in house.rooms:
                            room = house.rooms[item.location]
                            room.items[item.name] = item
                    elif command == 'door':
                        door_from = Door(data[0][0], data[1], data[2], data[3])
                        door_to = Door(data[0][2], data[1], data[3], data[2])
                        if data[2] in house.rooms:
                            room = house.rooms[data[2]]
                            room.doors[data[0][0]] = door_from
                        if data[3] in house.rooms:
                            room = house.rooms[data[3]]
                            room.doors[data[0][2]] = door_to
                    elif command == 'player':
                        print(hello_message)
                        name_input = input("First, choose name. Otherwise, it will be Bob." + '\n')
                        if not name_input:
                            self.player = Player(data[0])
                        else:
                            self.player = Player(data[0], name_input)

    def change_name(self, name):
        player = self.player
        player.name = name
        print('Player\'s name has changed to', player.name)

    def go(self, direction):
        player = self.player

        if not player.standing:
            print(self.player.name, 'is sitting.')
            return
        else:
            house = self.house
            room = house.rooms[player.position]
            if len(room.doors) > 0:
                if direction in room.doors:
                    door = room.doors[direction]
                    if door.status == 'open' or door.status == 'unlocked':
                        player.position = door.next
                        print(player.name, 'moved to the', door.next + '.')
                    else:
                        print('The door is locked.')
                else:
                    print(player.name, 'did not move.') 

    def unlock(self, direction):
        player = self.player
        if not player.standing:
            print(self.player.name, 'is sitting.')
            return
        else:
            opposite_direction = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
            house = self.house
            room = house.rooms[player.position]
            for i in player.items:
                i = player.items[i]
                if i.usage == 'unlock':
                    if direction in room.doors:
                        door = room.doors[direction]
                        next_room = house.rooms[door.next]
                        if door.status == 'locked':
                            door.status = 'unlocked'
                            next_room.doors[opposite_direction[direction]].status = 'unlocked'
                            print(player.name, 'unlocked the door.')
                            return
                        elif door.status == 'closed':
                            print(player.name, 'did\'t need a key.', player.name, 'needs to open the door.')
                            return
                        else:
                            print('This door is already open, dummy.')
                            return
                    else:
                        print('There\'s no such door.')
                        return
                else:
                    print(player.name, 'doesn\'t have a key.')

    def read(self, item):
        player = self.player
        if item in player.items:
            item = player.items[item]
            if item.usage == 'read':
                print(player.name, "is reading a", item.name + '.')
        else:
            print(player.name, "is not holding a book.")

    def open(self, direction):
        player = self.player
        if not player.standing:
            print(player.name, 'is currently sitting.')
            return
        else:
            house = self.house
            room = house.rooms[player.position]
            opposite_direction = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
            if direction in room.doors:
                door = room.doors[direction]
                next_room = house.rooms[door.next]
                if door.status == 'closed':
                    door.status = 'open'
                    next_room.doors[opposite_direction[direction]].status = 'open'
                    print(player.name, 'opened the door.')
                    return
                elif door.status == 'locked':
                    print('The door is locked. Find a key.')
                else:
                    print('This door is already opened, dummy.')
            else:
                print('There\'s no such door.')

    def close(self, direction):
        player = self.player
        if not player.standing:
            print(player.name, 'is currently sitting.')
            return
        else:
            house = self.house
            room = house.rooms[player.position]
            opposite_direction = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
            if direction in room.doors:
                door = room.doors[direction]
                next_room = house.rooms[door.next]
                if door.status == 'open':
                    door.status = 'closed'
                    next_room.doors[opposite_direction[direction]].status = 'closed'
                    print(player.name, 'closed the door.')
                    return
                elif door.status == 'locked':
                    print('The door is locked. Find a key.')
                else:
                    print('This door is already opened, dummy.')
            else:
                print('There\'s no such door.')

    def take(self, i):
        player = self.player
        if not player.standing:
            print(player.name, 'is currently sitting.')
            return
        house = self.house
        room = house.rooms[player.position]
        if i in room.items:
            item = room.items[i]
            if item.species == 'STATIONARY' or item.species == 'SIT':
                print(player.name, 'can\'t move this item.')
            else:
                player.items[i] = item
                room.items.pop(i)
                print(player.name, 'took the', item.name + '.')
        else:
            print('No such item.')

    def drop(self, i):
        player = self.player
        if not player.standing:
            print(player.name,'is currently sitting.')
            return
        house = self.house
        room = house.rooms[player.position]
        if i in player.items:
            room.items[i] = player.items[i]
            player.items.pop(i)
        else:
            print(player.name, 'doesn\'t have', i.name)

    def drop_all(self):
        player = self.player
        if not player.standing:
            print(player.name,'is currently sitting.')
            return
        if not player.items:
            print(player.name, 'doesn\'t have any items.')
        else:
            house = self.house
            room = house.rooms[player.position]
            copy_items = player.items.copy()
            for i in copy_items:
                if i in player.items:
                    room.items[i] = player.items[i]
                    player.items.pop(i)
            print(player.name, 'dropped everything.')

    @staticmethod
    def easter():
        print("""
           |_|  /| | / |_~    /| |\|   |_~ /~_ /~_ (~ ~|~ |~)  /|
           | | /~| |/  |__   /~| | |   |__ \_| \_| _)  |  |~\ /~|
          ~~~~~~~~~~~~~~~~~ ~~~~~~~~~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            (~ |~) |_~ /~' |  /| |      |_~  /| (~ ~|~ |_~ |~)  |
            _) |~  |__ \_, | /~| |__    |__ /~| _)  |  |__ |~\  .
           ~~~~~~~~~~~~~~~~~~~~~~~~~~  ~~~~~~~~~~~~~~~~~~~~~~~~~~~

           _________,---------.____------.___
          /_______    `--._______  `--.____ \\
           /__.-' `-----.____    `--._____,`_/_
           ,'                `---.___ ___//    `-.
          /     _.----,,             `---'        \         ,;~~;,
        _|     /        \           .'          ~  |       ;;;;;;;;
      /'/    /          |           '          /|  |      |  ''''  |
     |  |   |        _/'__         ,`,    __       |      ||||||||||
      \  \_  `  ,/   `'~ _\-_____,  `~~~'~ _\     _/      | '''''' |
\\||/  ~'~ `---(__________,'    (___________,'---'   \||/  \,;;;;,/  \||/ \|/
                                                             ~~~~  
     \||/     \|||//               \\|||//             \|||/     \||/
""")

    def mirror(self):
        if 'mirror' in self.player.items:
            print('( ͡❛ ͜ʖ ͡❛)')
        else:
            print(self.player.name, 'needs a mirror.')
    
    def show(self):
        player = self.player
        house = self.house
        if player.position not in house.rooms.keys():
            return print(player.position, 'not in', house.rooms.keys())
        info = house.rooms[player.position].info()
        string = player.name + ' is in the ' + player.position + '. '
        if 'Doors' in info:
            string += 'The room has doors to ' + info['Doors'] + '. '
        if len(info['Items']) > 0:
            string += player.name + ' sees these items: ' + info['Items'] + '. '
        else:
            string += ''
        print(string)

    def where_at(self):
        player = self.player
        print(player.name, 'is in the', player.position + '.')

    def holds(self):
        player = self.player
        if len(player.items) > 0:
            print(player.name, 'is holding these items: ' + ', '.join(player.items.keys()) + '.')
        else:
            print(player.name, 'is not holding anything.')

    def play(self): 
        player = self.player
        if not player.standing:
            return print(player.name,'is currently sitting.')
        house = self.house
        room = house.rooms[player.position]
        if 'piano' in room.items:
            item = room.items['piano']
            if item.species == 'PLAY':
                print('    o    _______________', '\n'
                    '   /\_  _|             |', '\n'
                    '  _\__`[_______________|', '\n'
                    '   ] [ \, ][         ][', '\n')
        else:
            print('There is no piano in this room.')

    def sit(self):
        player = self.player
        if not player.standing:
            print(player.name, "is already sitting.")
        else:
            house = self.house
            current_room = house.rooms[player.position]
            items = current_room.items
            items_to_sit_on = [item for item in items if current_room.items[item].species == 'SIT']
            if not items_to_sit_on:
                print(player.name,"sat down on the floor.")
                player.standing = False
            else:
                print(player.name, f"sat down on the {items_to_sit_on[random.randint(0, len(items_to_sit_on) -1)]}.")
                player.standing = False

    def stand(self):
        player = self.player
        if player.standing:
            print(player.name, 'is already standing.')
        else:
            player.standing = True
            print(player.name, "is now standing up.")

    def item_info(self, i):
        player = self.player
        house = self.house
        room = house.rooms[player.position]
        if i in room.items:
            item = room.items[i]
            print(item.name, item.location, item.species, item.usage) 
            if item.usage == 'unlock':
                print('This item can be used for both locking and unlocking.')
        else:
            generic_error()

    @staticmethod
    def commands():
        print('You can use the following commands:', ', '.join(Game.COMMANDS), '.')

    def boot(self):
        player = self.player
        q = True
        two_input_commands = ['take', 'open', 'drop', 'unlock', 'read']
        game.show()
        while q:
            user_input = input("> ")
            data = user_input.split(' ')
            com = data[0]
            if com not in Game.COMMANDS:
                print(player.name, 'doesn\'t know how to do that. Try \'commands\'.')
            elif com == 'quit' or com == 'q':
                print('Bye bye')
                q = False
            elif len(data) > 1:
                com1, com2 = data[0], data[1]
                com = f'game.{com1}(\'{com2}\')'
                exec(com)
            elif len(data) == 1:
                if com == 'go':
                    print(f'Where should {player.name} go?')
                elif com == 'change_name':
                    print('Name required.')
                elif com == 'item_info':
                    print('Item required.')
                elif com in two_input_commands:
                    print(f"What should {player.name} {com}?")
                else:
                    exec(f'game.{com}()')
            else:
                generic_error()
        sys.exit()
            

# ________________________________________________________


game = Game(args.filename)
game.boot()
