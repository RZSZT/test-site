from PIL import Image
import sys
from random import randint


class Process():
    
    def __init__(self, filename):
        
        self.filename = filename
        print(filename)

        # make image black and white
        image_file = Image.open(filename) # open colour image
        image_file = image_file.convert('RGBA')
        image_file = image_file.convert('1') # convert image to black and white
        # name the B+W file    
        if "/" in filename:    
            parts = filename.split("/") # chr(92)
            part1 = parts[0] + "/" + parts[1]
            part2 = "BW_" + parts[2]
            BW_filename = part1 + "/" + part2
        #else:
            #BW_filename = "temp_images/BW_" + filename
        image_file.save(BW_filename)
        image_file.close()
        # save to temp, open from temp
        self.file_name = BW_filename

        # define variables
        self.pixel_chunk = []
        self.line = ""
        
        # get the B+W image
        self.img = Image.open(self.file_name) #jpg, png, etc.
        # get the colour image
        self.imgCol = Image.open(self.filename)
        self.imgCol = self.imgCol.convert('RGBA')
        #pix = self.img.load()

        # get the dimensions
        (self.boundry_x, self.boundry_y) = self.img.size

        # define increment
        self.increment = int(self.boundry_x / 80)
        if self.increment < 1:
            self.increment = 1
        self.boundry_x -= 2
        self.boundry_y -= 2
        # define start and end of segment to grab
        self.start_x = 0
        self.end_x = self.start_x + self.increment

        self.start_y = 0
        self.end_y = self.start_y + self.increment


    # grab pixel bunch
    # builds a line of " " and "#" tto denote black( ) or white(#) pixels
    def get_square(self, start_x, end_x, start_y, end_y, file_name):

        
        number_on = 0
        number_here = 0
        # get B+W image
        img = Image.open(file_name) #jpg, png, etc.
        pix = img.load()
        # get colour image
        pixCol = self.imgCol.load()
        R = 0
        S = 0
        T = 0
        for y in range(start_y, end_y):

            for x in range(start_x, end_x):

                a = pix[x, y]
                
                (r, s, t, qq) = pixCol[x, y]
                
                R += r
                S += s
                T += t
                #print(a)
                number_here += 1

                if a > 128:

                    number_on += 1
        
        img.close()
        
        # process and assign average colour
        rr = int(R / number_here)
        ss = int(S / number_here)
        tt = int(T / number_here)
        colour = (rr,ss,tt)
        
        # process numbers and assign the block a shade number 1 (white) - 5 (black)
        if number_on > 0:
            percent = int((number_on / number_here) * 100)
        else:
            percent = 0

        return percent, colour


    def assess_shade(self, percent):

        if percent == 100:			# white

            shade = 1

        elif percent < 100 and percent > 66:

            shade = 2

        elif percent <= 66 and percent > 33:

            shade = 3

        elif percent <= 33 and percent > 5:

            shade = 4

        else:
            shade = 5			# black

        return shade


    # define our dictionary


    # grab the first 2 squares associated with a charachter
    def get_character(self, start_x, end_x, start_y, end_y, increment, file_name, boundry_y):

        sstart_y = end_y
        eend_y = end_y + increment
        sstart_x = start_x
        eend_x = end_x

        characters = {
            "11": "@", "12": "#", "13": ["M", "W", "N"], "14": ["%", "&"], "15": ["*", "+"],
            "21": ["0", "O"], "22": ["@", "G"], "23": "B", "24": ["9", "P", "F", "R"], "25": "^",
            "31": "8", "32": ["$", "S"], "33": ["3", "E"], "34": ["?", "7"], "35": '"',
            "41": "b", "42": "h", "43": ";", "44": "!", "45": "'",
            "51": ["m", "s", "e"], "52": ["o", "u", "c", "r", "n"], "53": [":", ";"], "54": ".", "55": " "
            }

        percent, colour = self.get_square(start_x, end_x, start_y, end_y, file_name)

        shade_top = self.assess_shade(percent)
        (r,s,t) = colour
        # go down a block
        
        if eend_y <= boundry_y:

            percent2, colour2 = self.get_square(sstart_x, eend_x, sstart_y, eend_y, file_name)
            shade_bottom = self.assess_shade(percent2)
            (rr,ss,tt) = colour
        else:
            shade_bottom = 5
            rr = 0
            ss = 0
            tt = 0
        # with a shade assessment for top and bottom we can assign the 25 combinations to a charachter
        #
        #	.,'"`~;:-_=+!{}[]1234567890@#$%^&*()abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ|?/
        R = int((r + rr) / 2)
        S = int((s + ss) / 2)
        T = int((t + tt) / 2)
        Colour = (R,S,T)

        char = str(shade_top)
        acter = str(shade_bottom)
        char_acter = char + acter

        character = characters.get(char_acter)
        if type(character) == list:
            rand = randint(0, len(character) - 1)
            newChar = character[rand]
            character = newChar
        #print(character, "")
        return character, Colour


    def get_line(self, start_x, end_x, start_y, end_y, increment, file_name, boundry_y):

        # get a line of charcters
        build_line = ""
        colours = []
        for across in range(0,80):

            character, colour = self.get_character(start_x, end_x, start_y, end_y, increment, file_name, boundry_y)

            build_line = build_line + character
            colours.append(colour)
            start_x += increment
            end_x += increment

        return build_line, colours


    def main(self):
        
        colourLists = []
        new_file = open(self.filename + ".txt", "w") #"temp_images/" + 
        while self.end_y <= self.boundry_y:

            line, colours = self.get_line(self.start_x, self.end_x, self.start_y, self.end_y, self.increment, self.file_name, self.boundry_y)
            new_file.write(line + "\n")
            colourLists.append(colours)
            self.start_y = self.end_y + self.increment
            self.end_y = self.start_y + self.increment

            inc = int((self.end_y / self.boundry_y) * 100)
            print(f"{inc}%")
        print("\n DONE!")

        new_file.close()
        self.img.close()
        self.imgCol.close()
        with open(self.filename + ".txt") as new_file:#"temp_images/" + 
            print(new_file.read())
        return self.filename + ".txt", colourLists
