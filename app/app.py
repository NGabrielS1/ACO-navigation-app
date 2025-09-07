import os
import time
import math
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import permutations
import customtkinter as ctk
from PIL import Image, ImageFont, ImageDraw


#app window
class App(ctk.CTk):

    #variables
    start = None
    Priority = []
    Packages = []
    End = None

    init_p = 0.2
    alpha = 1
    beta = 2
    added_p = 10
    evap_rate = 0.1
    ants = 100

    def __init__(self):
        super().__init__()

        # window settings
        self.title("EasyNav: Easy Navigation Software")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(0, 0)
        self.configure(fg_color='#f5f5f7')
        current_path = os.path.dirname(os.path.realpath(__file__))
    
    def custom_text(self, text, font, color, fontsize, bgcolor, anchor="lt", pad_right=0):
        #load font
        font = ImageFont.truetype(font=font, size=fontsize)

        #get size
        dummy_image = Image.new(mode="RGBA", size=(1, 1))
        dummy_draw = ImageDraw.Draw(dummy_image)
        text = text.split("\n") #seperate by newline (enter)
        left, top, right, bottom = dummy_draw.textbbox((0, 0), text=max(text, key=len), font=font, anchor=anchor)
        width = right - left + 10 + pad_right#10px padding
        height = (bottom - top + 10) * len(text)

        #create img
        image = Image.new(mode="RGBA", size=(width, height), color=bgcolor)
        draw = ImageDraw.Draw(image)
        draw.fontmode = "L"
        for i, line in enumerate(text):
            draw.text(xy=(5, 5+height/len(text)*i), text=line, font=font, fill=color, anchor=anchor)
        image = ctk.CTkImage(image, size=(width,height))
        return image

# Run application
if __name__ == "__main__":
    # create app
    app = App()
    
    app.mainloop()
