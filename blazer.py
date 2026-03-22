import pygame
import os
import json
import calendar
import datetime
import tkinter as tk
from tkinter import filedialog

BASEDIR = os.path.dirname(__file__)
CONF = os.path.join(BASEDIR, 'config.json')


pygame.init()

screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Blazer")
clock = pygame.time.Clock()

with open(CONF, "r") as f:
    config = json.load(f)

user = config['USER']

COLOURS = tuple(config['colourschemes'][user['colourscheme']])
LIGHTEST = COLOURS[3]
LIGHT = COLOURS[2]
MID = COLOURS[1]
DARK = COLOURS[0]

BG = tuple(config['background'][user['background']])
FONT = pygame.font.SysFont(config['font'][user['font']], user['fontsize'])


timeframeinmonths = 1

date = str(datetime.date.today()).split("-")
year = date[0]
month = date[1]
day = date[2]

daysincurrentmonth = calendar.monthrange(int(year),int(month))[1]


tkroot = tk.Tk()
tkroot.withdraw()

def square(x, y, width, height, colour, border_radius):
    pygame.draw.rect(screen, colour, (x, y, width, height), border_radius=border_radius)

def text(font, text, colour):
    return font.render(text, True, colour)

def formatmonth(days):
    pass

def main():
    filepath = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    filepath = filedialog.askopenfilename(
                        parent=tkroot,
                        title="Open File",
                        initialdir=os.path.expanduser("~")
                    )
                    print(filepath)

        screen.fill(BG)
        screen.blit(text(FONT, "Blazer", MID), (50, 25))
        square(50, 100, 20, 20, DARK, 5)
        square(80, 100, 20, 20, MID, 5)
        square(110, 100, 20, 20, LIGHT, 5)
        square(140, 100, 20, 20, LIGHTEST, 5)

        screen.blit(text(FONT, year, MID), (500,25))
        screen.blit(text(FONT, month, MID), (500,55))


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
