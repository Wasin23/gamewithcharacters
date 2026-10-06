import collections
import math
import random
# this project will be a way for me to practice my code.
# It will build upon itself
# I want to create a game of life with multiple characters that move around and make decisions

# how will I first create the layout? and then characters?

# use DSA for complex character movement, assignment of traits, and other environmental factors
# Have the list print every second with updates

# Currently, new characters are given random positions on the map, added to a dict, and then the dict is written to a characters file
# The characters file is retrieved on each startup
# Old characters that are not initialized persist despite not being initialized as the app pulls from what exists (in get_stats()) first

class world:
    def __init__(self, size, character: list[str]):
        self.size = size # set size input
        self.character = character # set character amount
        self.positions = {} # create dict of positions
        for char in self.character: self.positions[char] = None

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
            if self.positions[char] is None: # if the character is already found, leave it be
                while True:
                    x = random.randint(0, self.size - 1) # set random col from 0 to the input size
                    y = random.randint(0, (self.size // 2) - 1) # set random row from 0 to the input size
                    s = [x, y] # set s to a list 
                    for value in self.positions.values(): # loop thru values inside self.positions
                        if value == s: # if a value already matches s, try again
                            print("reassigning")
                            break
                    else: # if not
                        self.positions[char] = s # set the random position in the dict given the new character 
                        break
        with open("characters.txt", "w") as f: 
            for char in self.positions:
                f.write(f"{char},{self.positions[char][0]},{self.positions[char][1]}\n")

    def land(self):
        grid = [["."] * self.size for i in range(self.size // 2)] # create a grid for the characters to traverse
        for char in self.positions: # for each character in the dict
            x = self.positions[char][0] # x coordinate value in self.positions 
            y = self.positions[char][1] # y coordinate value in self.positions 
            grid[y][x] = "@" # set the grid spot at position row x col to an @ symbol to indicate a character's position
        return grid

    def movement(self):
        class moves():
            def __init__(self, left, right, up, down):
                self.left = left
                self.right = right
                self.up = up
                self.down = down

            

w = world(20, ["Brody"])
w.get_stats()
w.characters()
for row in w.land():
    print("".join(row))