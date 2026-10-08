from collections import deque
import math
import random
import numpy
import pandas

# this project will be a way for me to practice my code.
# It will build upon itself
# I want to create a game of life with multiple characters that move around and make decisions
# The world will have natural disasters as well

# TODO LIST
# create fire using BFS: DONE
# Create earthquake using DFS:
# Kadane algo for storms:
# Character memories for previous x positions to skew movement towards something, assigned to self.positions:
# Potential disaster zone rescue (shortest path):
# Food / resources:

# use DSA for complex character movement, assignment of traits, and other environmental factors
# Have the list print every second with updates

# Currently, new characters are given random positions on the map, added to a dict, and then the dict is written to a characters file
# The characters file is retrieved on each startup
# Old characters that are not initialized persist despite not being initialized as the app pulls from what exists (in get_stats()) first

class world:
    def __init__(self, size, character: list[str]):
        self.size = size # set size input
        self.character = character # set character amount
        self.tick = None # create time 
        self.positions = {} # create dict of positions
        self.worlddict = {} # create dict of world info
        self.grid = []
        self.marked = []
        for char in self.character: self.positions[char] = None

    def time(self): # build time function
        with open("Time.txt", "r") as w:
            contents = w.read()
            time = contents.split(",")
            if contents:
                print(time)
                self.worlddict["Time"] = time
                self.tick = int(time[0]) 
        if self.worlddict: # if the time is recorded
            self.worlddict["Time"] = self.tick # set time equal to the current time
            self.tick += 1 # increment time by 1
        else: # else
            self.tick = 0 # set time equal to 0 if time is none
            self.worlddict["Time"] = self.tick # then create the key in the dict with the time
            self.tick += 1 # increment time by 1
            print(self.tick) # print the current time

    def trigger_disaster(self):
        class natural_disasters():
            def __init__(nd, left, right, up, down, leftup, leftdown, rightup, rightdown): # create disaster directions
                nd.left = left
                nd.right = right
                nd.up = up
                nd.down = down
                nd.leftup = leftup
                nd.leftdown = leftdown
                nd.rightup = rightup
                nd.rightdown = rightdown
                nd.dirlist = [nd.right, nd.left, nd.up, nd.down, nd.leftup, nd.leftdown, nd.rightup, nd.rightdown]
                nd.visited = {} # create dict of coordinates to show whats been visited

            def update(nd):
                with open("Disaster.txt", "r") as d:
                    contents = d.read()
                    spots = contents.split("\n")
                    for spot in spots: # loop through lists of coords per key
                        if not spot:
                            continue # if the line is only an empty string, continue
                        spottype = spot.split(",") # split the stats of each spot found into parts
                        if spottype[0] in self.worlddict: # if the particular key does exist
                            self.worlddict[spottype[0]].append([int(x) for x in spottype[1:]]) # at spottype (the key), convert the list to ints and append each list to the key values
                            coord = tuple(int(x) for x in spottype[1:]) # set coord equal to a tuple of the lists
                            nd.visited[coord] = spottype[0] # create a key for the lists at the coord tuple
                        else:
                            self.worlddict[spottype[0]] = [[int(x) for x in spottype[1:]]] # rebuild self.worlddict dict from Disaster.txt and set the positions as integers
                            coord = tuple(int(x) for x in spottype[1:])
                            nd.visited[coord] = spottype[0] 
            
            def fire_BFS(nd): # create fire function
                if self.tick % 30 == 0: # if the tick is a multiple of 30, kill the fire
                    self.worlddict["Fire"] = [] # set fire to an empty list
                else:
                    oldfire_coords = [coord for coord, type in nd.visited.items() if type == "Fire"] # find the fire coordinates from the previous round and set it to oldfire
                    for coord in oldfire_coords: # loop through oldfire
                        del nd.visited[coord] # delete the previous records of oldfire inside the visited dict
                    if oldfire_coords:
                        queue = deque(oldfire_coords) # build queue for dfs by creating a list with the start coordinates 
                        dir = random.sample(nd.dirlist, 3) # set dir to a list of 3 randomly selected directions
                        for spot in list(oldfire_coords): # loop through the oldfire coordinates
                            spot = queue.popleft() # pop the first coordinate and set equal to spot
                            for i in dir: # loop through directions
                                # pick a random number between the 0 and the amount of fire spots times 5, 
                                # and if the remainer of that number divided by the fire spots divided by 2 is 0, spread the fire in the selected direction
                                if random.randint(0, len(self.worlddict["Fire"]) * 5) % ((len(self.worlddict["Fire"]) + 1) // 2) == 0:  
                                    s = list(spot) # s is the listed version of the tuple, spot
                                    newcoords = [(s[0] + i[0]) % (self.size), (s[1] + i[1]) % (self.size // 2)] # newcoords is the corrected coordinates (for out of bounds) of the fire
                                    newspot = tuple(newcoords) # convert newcoords list of updated coordinates back to a tuple
                                    if newspot in nd.visited: # if these coords already exist, ignore them
                                        continue
                                    else: # if they do exist, add to the visited dict with the value "fire"
                                        queue.append(newspot) 
                                        nd.visited[tuple(newspot)] = "Fire"
                                else:
                                    continue
                            
                    elif self.tick % 21 == 0: # if the time is a multiple of 11 start a fire
                        print("A fire has started! (marked as X)")
                        start = [random.randint(0, self.size - 1), random.randint(0, (self.size // 2) - 1)] # set a random coordinate on the map on fire
                        queue = deque([start]) # build queue for dfs by creating a list with the start coordinates tupled
                        dir = random.sample(nd.dirlist, 3)
                        nd.visited[tuple(start)] = "Fire" # add the new start coords to fire inside visited

                    self.worlddict["Fire"] = list(nd.visited) # set worlddict at fire to the updated visited list

        nd = natural_disasters([-1, 0], [1, 0], [0, 1], [0, -1], [-1, 1], [-1, -1], [1, 1], [1, -1]) # initialize natural disaster class with movement directions
        # call each natural disaster
        nd.update()
        nd.fire_BFS()

    def land(self):    
        self.grid = [["."] * self.size for i in range(self.size // 2)] # create a grid for the characters to traverse
        for char in self.positions: # for each character in the dict
            x = self.positions[char][0] # x coordinate value in self.positions 
            y = self.positions[char][1] # y coordinate value in self.positions 
            self.grid[y][x] = "@" # set the grid spot at position row x col to an @ symbol to indicate a character's position
        for condition in self.worlddict: # loop through worlddict
            if condition != "Time" and condition: # if the condition name is not time and exists
                assign = self.worlddict[condition] # set assign to the list of lists at condition
                for coords in assign: # loop through the list
                    x = coords[0] # set x to the 0th index in the list
                    y = coords[1] # set y to the 1st index in the list
                    if condition == "Fire": # if condition string is fire mark the grid coords wih an X
                        self.grid[y][x] = "X"
        return self.grid

    def get_stats(self):
            with open("characters.txt", "r") as f: # open db of characters and their positions
                contents = f.read() # create object of contents
                lines = contents.split("\n") # becomes a list of the contents split by newline (endl)
                for line in lines: # loop through list of lines
                    if not line:
                        continue # if the line is only an empty string, continue
                    charstat = line.split(",") # split the stats of each character found into parts
                    print(charstat) # print the stats
                    self.positions[charstat[0]] = [int(x) for x in charstat[1:]] # rebuild self.positons dict from characters.txt and set the positions as integers

    def characters(self):
        for char in self.character:
            c = [x for x in self.positions.values() if x is not None] # create a list of the positions recorded
            if len(c) >= (self.size // 2) * self.size: # if the length of the positions exceeds or is equal to the size of the map
                print("Cannot Assign Character, All Spots Full") # print this message and break
                break
            if self.positions[char] is None: # if the character is already found, leave it be, if not found, assign a position
                while True:
                    x = random.randint(0, self.size - 1) # set random col from 0 to the input size
                    y = random.randint(0, (self.size // 2) - 1) # set random row from 0 to the input size
                    s = [x, y] # set s to a list with the x and y coords of the char
                    for value in self.positions.values(): # loop thru values inside self.positions
                        if value == s: # if a value (a current char position) already matches s, try again
                            print("reassigning")
                            break
                    else: # if not
                        self.positions[char] = s # set the random position in the dict given the new character 
                        break

    def movement(self):
        class moves():
            def __init__(move, left, right, up, down, ): # initialize move object, then directions
                move.left = left
                move.right = right
                move.up = up
                move.down = down

        for char in self.positions:
            for key in self.worlddict:
                if self.positions[char] in self.worlddict[key] and key != "Time":
                    self.marked.append(char)
            if char in self.marked: # if the current character is marked for death, skip
                continue
            else:
                move = moves(random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)) # set directions to random values
                xchange = move.right - move.left # simplify down to a move on x axis
                ychange = move.up - move.down # simplify to a move on y axis
                self.positions[char][0] = (self.positions[char][0] + xchange) % self.size # keep positions within bounds
                self.positions[char][1] = (self.positions[char][1] + ychange) % (self.size // 2)
                for x in self.positions:
                    if x in self.marked: # if the other character has been added to marked, skip
                        continue
                    else:
                        # if the second character is equal to the current moving character's position and the current moving isn't itself, do...
                        if self.positions[x] == self.positions[char] and self.positions[x] is not self.positions[char]: 
                            roll = random.randint(0, 1) # random interaction picker
                            if roll == 1: # first interaction --> random death
                                s = random.randint(0, 10)
                                if s >= 6: # if coinflip is greater than 5
                                    self.marked.append(char) # mark current moving char for death
                                if s <= 5: # if coinflip is less than 6
                                    self.marked.append(x) # mark char already in position for death
        for name in set(self.marked): 
            print(f"{name} dies!")
            del self.positions[name] 
                           
    def save(self):
        with open("characters.txt", "w") as f: 
            for char in self.positions: # loop though positions dict
                f.write(f"{char},{self.positions[char][0]},{self.positions[char][1]}\n") # write character positions to the charcters file as a save
        with open("Time.txt", "w") as w: # open time file save
            w.write(f"{self.tick}") # save self.tick written from the loop in time()
        with open("Disaster.txt", "w") as w: # open disaster progress file
            if self.worlddict.get("Fire", []): # if the worlddict at fire exists
                for coord in self.worlddict.get("Fire", []): # loop through the coordinates at the fire key
                    w.write(f"Fire,{coord[0]},{coord[1]}\n") # splite each coordinate value by comma and hea with "Fire"
       
w = world(20, ["Cole"])
w.time()
w.get_stats()
w.characters()
w.trigger_disaster()
w.movement()
w.save()
for row in w.land():
    print("".join(row))