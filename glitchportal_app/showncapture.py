from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 



class ThisImage():
    
    def __init__(self, filename, colourLists):
        
        self.img = Image.new(mode = "RGB", size = (800, 800))
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.truetype("glitchportal_app/novamono.ttf", 32)
        NameList = filename.split(".")
        self.filename = NameList[0]
        document = open(filename)
        self.lines = document.readlines()
        self.colours = colourLists
        
    def now(self):
        
        saved = False
        print(self.filename + ".jpeg")
        
        Y = 0
        X = 0
        
        for row in range(0, len(self.lines)):
            Line = self.lines[row].strip("\n")
            for char in range(0, len(Line)):
                self.draw.text((X, Y),Line[char],self.colours[row][char],font=self.font)
                X += 10
            Y += 16
            X = 0
        
        
        if not saved:
            self.img.save(self.filename + ".jpeg")
            saved = True
        
        return self.filename + ".jpeg"
