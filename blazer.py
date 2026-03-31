import pygame
import os
import json
import shutil
import calendar
import datetime
import tkinter as tk
from tkinter import filedialog

CONF = os.path.join(os.path.dirname(__file__), 'config.json')
COMMITSJSON = os.path.join(os.path.dirname(__file__), '.commits.json')
REPOSDIR = os.path.join(os.path.dirname(__file__), '.repos')

HEIGHT = 640
WIDTH = 640

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blazer")
clock = pygame.time.Clock()

with open(CONF, "r") as f:
    config = json.load(f)

userconfig = config['USER']

COLOURS = tuple(config['colourschemes'][userconfig['colourscheme']])

LIGHTEST = COLOURS[4]
LIGHT = COLOURS[3]
MID = COLOURS[2]
DARK = COLOURS[1]
DARKEST = COLOURS[0]

BGCOLOURS = tuple(config['background'][userconfig['background']])
BGPRIMARY = BGCOLOURS[0]
BGSECONDARY = BGCOLOURS[1]

SMALLESTFONT = pygame.font.SysFont(config['font'][userconfig['font']], userconfig['fontsize'] - 25)
SMALLFONT = pygame.font.SysFont(config['font'][userconfig['font']], userconfig['fontsize'] - 20)
FONT = pygame.font.SysFont(config['font'][userconfig['font']], userconfig['fontsize'])
BIGFONT = pygame.font.SysFont(config['font'][userconfig['font']], userconfig['fontsize'] + 20)


date = datetime.date.today()
splitdate = str(date).split("-")
year = splitdate[0]
month = splitdate[1]
day = splitdate[2]

daysincurrentmonth = int(calendar.monthrange(int(year),int(month))[1])


tkroot = tk.Tk()
tkroot.withdraw()

class Commit:
    def __init__(self, message, files, timestamp, repo):
        self.message = message
        self.files = files
        self.timestamp = timestamp
        self.repo = repo

    def makedictionary(self):
        return {
            'message': self.message,
            'files': self.files,
            'timestamp': self.timestamp,
            'repo' : self.repo
        }

    def savecommit(self):
        self.addtolog()
        with open(COMMITSJSON, 'r') as f:
                    commits = json.load(f)
        commits.append(self.makedictionary())
        with open(COMMITSJSON, 'w') as f:
            json.dump(commits, f, indent=2)
        for file in self.files:
            filename = file.split("/")[-1]
            repopath = os.path.join(REPOSDIR, self.repo)

            newpath = os.path.join(repopath, filename)
            shutil.copy(file, newpath)

    def addtolog(self):
        repolog = os.path.join(REPOSDIR, self.repo, 'log.txt')
        with open(repolog, 'a') as f:
            f.write(f'{self.timestamp}~{self.message}~{self.files}\n')

def setup():
    if not os.path.exists(COMMITSJSON):
        with open(COMMITSJSON, 'w') as f:
            json.dump([], f)
    if not os.path.exists(REPOSDIR):
        os.mkdir(REPOSDIR)
    miscpath = os.path.join(REPOSDIR, 'misc')
    if not os.path.exists(miscpath):
        os.mkdir(miscpath)
        open(os.path.join(miscpath, 'log.txt'), 'w').close()



def square(x, y, width, height, colour, border_radius):
    pygame.draw.rect(screen, colour, (x, y, width, height), border_radius=border_radius)

def text(font, text, colour):
    return font.render(text, True, colour)



def displaypastdays(days, commits):
    gap = 10
    step = 40 + gap
    startx = WIDTH * 0.12
    starty = HEIGHT * 0.3
    squaresperrow = int((WIDTH * 0.8) // step)
    amounts = commitsperday(commits)
    monthstart = date.replace(day=1)

    for i in range(days):
        row = i // squaresperrow
        col = i % squaresperrow
        x = startx + col * step
        y = starty + row * step
        squaredate = str(monthstart + datetime.timedelta(days=i))
        amountofcommits = amounts.get(squaredate, 0)

        if amountofcommits == 0:
            colour = DARKEST
        elif amountofcommits == 1:
            colour = DARK
        elif amountofcommits == 2:
            colour = MID
        elif amountofcommits ==3:
            colour = LIGHT
        else:
            colour = LIGHTEST

        square(x, y, 40, 40, colour, 5)

def loadcommits():
    commits = []

    with open(COMMITSJSON) as f:
        data = json.load(f)

    for i in data:
        commit = [i['message'], i['files'], i['timestamp'], i['repo']]
        commits.append(commit)
    return commits

def commitsperday(commits):
    amounts = {}
    for commit in commits:
        datestr = commit[2]
        amounts[datestr] = amounts.get(datestr, 0) + 1

    return amounts

def addfile():
    filepath = filedialog.askopenfilename(
        parent=tkroot,
        title="Open File",
        initialdir=os.path.expanduser("~")
    )
    return filepath

def getrepos():
        return os.listdir(REPOSDIR)

def displayhomescreen(commits):
    screen.blit(text(BIGFONT, "Blazer", MID), (50, 20))
    square(50, 90, 20, 20, DARKEST, 5)
    square(80, 90, 20, 20, DARK, 5)
    square(110, 90, 20, 20, MID, 5)
    square(140, 90, 20, 20, LIGHT, 5)
    square(170, 90, 20, 20, LIGHTEST, 5)

    screen.blit(text(SMALLFONT, year, MID), (500,30))
    screen.blit(text(SMALLFONT, f"{day}-{month}", MID), (500,55))

    square(WIDTH*0.1,HEIGHT*0.2, WIDTH * 0.8, HEIGHT*0.6, BGSECONDARY, 5)

    square(50,550,200,50,DARK,5)
    screen.blit(text(SMALLFONT, "Add misc commit", MID), (60, 565))

    square(270,550,200,50,DARK,5)
    screen.blit(text(SMALLFONT, "View repos", MID), (310, 565))

    displaypastdays(daysincurrentmonth, commits)

def displaycommitscreen(files, message, repo):
    screen.blit(text(FONT, f'repo:{repo}', MID), (27, 580))

    square(40, 30, 200, 40, BGSECONDARY, 5)
    square(40, 90, 560, 120, BGSECONDARY, 5)
    screen.blit(text(FONT, "Message:", MID), (50, 27))

    square(40, 230, 175, 40, BGSECONDARY, 5)
    square(40, 290, 560, 180, BGSECONDARY, 5)
    screen.blit(text(FONT, "Files:", MID), (50, 228))

    square(40, 500, 175, 45, DARK, 5)
    screen.blit(text(FONT, "COMMIT", MID), (40, 500))

    square(400, 500, 175, 45, DARK, 5)
    screen.blit(text(FONT, "Home", MID), (400, 500))

    fontwidth,fontheight = SMALLFONT.size('m')

    charsperline = int(560/fontwidth)
    rows = int(180/fontheight)

    words = message.split()
    lines = []
    current = ''

    for word in words:
        if SMALLFONT.size(current + word)[0] < 560:
            current += word + " "
        else:
            lines.append(current)
            current = word + " "
    lines.append(current)

    for i,line in enumerate(lines):
        screen.blit(text(SMALLFONT, str(line), MID), (50, 100 + i * 20))

    if len(files) > 0:
        for file in files:
            displayfile = file
            index = files.index(file)
            ycord = 300 + index * 20

            if len(file) > charsperline:
                displayfile = file
                while SMALLFONT.size(displayfile)[0] > 560:
                    displayfile = displayfile[:-1]
                displayfile = displayfile[:-3] + '...'

            if files.index(file) == rows:
                screen.blit(text(SMALLFONT, '...', MID), (50,ycord))
                break
            screen.blit(text(SMALLFONT, displayfile, MID), (50,ycord))

def displayreposscreen(repos, typing, reponame, scroll):
    screen.blit(text(BIGFONT, "Repos", MID), (50, 20))

    square(400, 30, 175, 45, DARK, 5)
    screen.blit(text(FONT, "Back", MID), (400, 30))

    for i, repo in enumerate(repos):
        y = 100 + i * 70 - scroll
        square(40, y, 560, 60, BGSECONDARY, 5)
        screen.blit(text(FONT, repo, MID), (50, y + 15))

    ycord = 100 + len(repos) * 70 - scroll
    square(190, ycord, 210, 60, DARK, 5)
    screen.blit(text(FONT, 'add repo', MID), (200, ycord + 15))

    if typing:
        square(40, ycord + 80, 560, 60, BGSECONDARY, 5)
        screen.blit(text(FONT, reponame, MID), (50, ycord + 95))

def displayspecificrepo(repo):
    screen.blit(text(BIGFONT, repo, MID), (50, 20))
    with open(os.path.join(REPOSDIR, repo, 'log.txt')) as f:
        lines = f.readlines()
    for i, line in enumerate(reversed(lines[-5:])):
        ycord = 90 + 80 * i
        square(40, ycord, 500, 60, BGSECONDARY, 5)
        parts = line.split('~')
        for part in parts:
            screen.blit(text(SMALLESTFONT, part, MID), (50, ycord + 20*parts.index(part)))

    square(270,550,200,50,DARK,5)
    screen.blit(text(SMALLFONT, "Add commit", MID), (310, 565))

    square(50,550,200,50,DARK,5)
    screen.blit(text(SMALLFONT, "Back", MID), (60, 565))



def main():
    setup()

    running = True
    typing = False

    state = 'home'
    text = ''
    repo = 'misc'

    files = []
    commits = loadcommits()

    scroll = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if state == 'home':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(50, 550, 200, 50).collidepoint(event.pos):
                        state = 'commit'
                    if pygame.Rect(270,550,200,50).collidepoint(event.pos):
                        state = 'repos'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        state='commit'

            elif state == 'commit':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(40, 500, 175, 45).collidepoint(event.pos):
                        if len(text) > 0 and len(files) > 0:
                            Commit(text, files, str(date), repo).savecommit()
                            commits = loadcommits()
                        state = 'home'
                        files = []
                        repo = 'misc'
                        typing = False

                    elif pygame.Rect(40, 290, 560, 120).collidepoint(event.pos):
                        files.append(addfile())
                        typing = False
                    elif pygame.Rect(40, 90, 560, 120).collidepoint(event.pos):
                        typing = True
                    elif pygame.Rect(400, 500, 175, 45).collidepoint(event.pos):
                        state = 'home'

                if event.type == pygame.KEYDOWN:
                    if typing:
                        if event.key == pygame.K_RETURN:
                            typing = False
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

                    else:
                        if event.key == pygame.K_f:
                            files.append(addfile())
                        if event.key == pygame.K_j:
                            typing = True


            elif state == 'repos':
                addbuttonycord = 100 + len(getrepos()) * 70
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(190, addbuttonycord, 210, 60).collidepoint(event.pos):
                        typing = True
                    elif pygame.Rect(00, 30, 175, 45).collidepoint(event.pos):
                            state = 'home'
                    for i, reponame in enumerate(getrepos()):
                        if pygame.Rect(40, 100 + i * 70, 560, 60).collidepoint(event.pos):
                            state='specificrepo'
                            repo = reponame

                elif event.type == pygame.KEYDOWN:
                    if typing:
                        if event.key == pygame.K_RETURN:
                            if len(text) > 0:
                                repopath = os.path.join(REPOSDIR, text)
                                os.mkdir(repopath)
                                open(os.path.join(repopath, 'log.txt'), "w").close()
                                text = ''
                            typing = False
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
                elif event.type == pygame.MOUSEWHEEL:
                        scroll -= event.y * 70
                        scroll = max(0, scroll)

            elif state == 'specificrepo':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(270,550,200,50).collidepoint(event.pos):
                        state = 'commit'
                    elif pygame.Rect(50,550,200,50).collidepoint(event.pos):
                        state = 'repos'

        screen.fill(BGPRIMARY)

        if state == 'home':
            displayhomescreen(commits)
        elif state == 'commit':
            displaycommitscreen(files,text,repo)
        elif state == 'repos':
            displayreposscreen(getrepos(), typing, text,scroll)
        elif state == 'specificrepo':
            displayspecificrepo(repo)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
