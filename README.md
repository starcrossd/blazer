# Blazer

A gui to track progress on anything - such as revision, in a way to provide maximum customisation options to make it your own.
Built as a small proof of concept / passion project to practice code and get experience making guis as I've only made clis til now.
The github commit history essentially got me addicted to coding for a bit just so I can see more green squares on the timeline so I thought if I made a general purpouse one I'd want to study more.
File selection is kinda ugly, sorry about that - had to use tkinter cos pygame doesn't work as well for it, maybe changed in a future patch.


## Install
To install this ,as its a python program, you need to install pip or pipx
```bash
# Recommended
pipx install git+https://github.com/starcrossd/blazer.git

# Or with pip
pip install --user git+https://github.com/starcrossd/blazer.git
```

## Uninstall
```bash
pipx uninstall blazer
```

## Usage - *IMPORTANT PLEASE READ*
```bash
blzr # runs the program -> thats if youre using terminal, as its a gui you can also find it in aplication managers
```
You can use the gui buttons to operate the program or specific keys whilst in the window.
If you want to use a mouse to add files or a commit message click on the provided area.

### Home Screen
    a - opens the misc Commit Screen
    r - opens repo view
The misc commit folder is for general or quick commits that dont fit neatly into anything else or you cant be bothered to make a repo
To view wht has been commited on a specific day of the month simply click on that square on the homescreen

### Commit Screen
    f - adds a file 
    j - allows you to start typing the commit message, `Enter` to stop
    h - returns to home screen
Clicking `Home` discards the current commit and returns to the home screen
    
### Repos screen
    a - allows you to start typing name of new repo
    h - returns to home screen
    
### Specific day screen 
    h - returns to home screen

### Repo Screen
Clicking a repo opens it, showing the 5 most recent commits from its log.
From here you can click `Add commit` to start a commit pre-assigned to that repo, or `Back` to return.
Holding down on the delete button for 1.5s deletes that repo

# Customisation
Go into `config.json`, under the `USER` section, select the options you want to use for your Blazer app

*For example*: 
```json
//example setup
  "USER": {
    "colourscheme": "forest",   // Changing forest -> ocean to change the base pallet to be blue
    "background": "dark23",     // Changing dark23 -> solarized to change the background
    "font": "notoserif",        // you probably get it by now
    "fontsize": 40              // There aren't presets for font size so you can change it yourself
    // but be aware as there's no presets for font size it may cause the program to look ugly
  },
```

# Boring documentation for nerds
###### Don't get offended, you gotta be a certain level of nerd to wanna know how a specific program works

## Getting the configuration for user's customisations

The config is stored as a `.json` file.
This is so there can be set presets without them needing to be hardcoded into the python.
Personally I'd much rather edit a json than a python file for customisation.
THEREFORE, it allows for more user customisation as you can add or remove whatever you like!
Which is what you should do with all apps to make them truly yours.

So in python we need to:
```python
import os
import json

CONF = os.path.join(os.path.dirname(__file__), 'config.json')
# bunch of code
 
with open(CONF, "r") as f:
    config = json.load(f)

userconfig = config['USER']

COLOURS = tuple(config['colourschemes'][userconfig['colourscheme']]) # example of data gotten from USER
# bunch of code 
```
The `CONF = [...]` line is to make sure we're using the right config file, in the same folder as the program.
The data from that file is then saved as `config` using the json library.
Then the part we actually care about, `USER` is set as `userconfig` which is a list of the user choices.
```python
tuple() 
```
is used for making the list into an array that is needed for certain pygame features.

The code then finds the user `colourscheme` in the `colourschemes` part of the json file and reads the list of colours as arrays.
A similar process is used for all the other parts of the user's config.

## The user interface

Blazer uses `pygame` as a gui, there are much better ways I'm sure but oh well.
To display the main user interface the program uses:
```python
# functions already defined earlier in the code
if state == 'home':
    displayhomescreen()
elif state == 'commit':
    displaycommitscreen()
elif state == 'repos':
    displayreposscreen()
elif state == 'specificrepo':
    displayspecificrepo()
```
This checks what `state` the gui should be in and renders it appropriately.
To display actual ui elements the functions use rectangles and text with functions:
```python
def square(x, y, width, height, colour, border_radius):
    pygame.draw.rect(screen, colour, (x, y, width, height), border_radius=border_radius)

def text(font, text, colour):
    return font.render(text, True, colour)
```
These functions make creating ui elements easier, for example:
```python
def displaycommitscreen():
    square(40, 30, 200, 40, BGSECONDARY, 5)
    square(40, 90, 560, 120, BGSECONDARY, 5)
    screen.blit(text(FONT, "Message:", MID), (50, 27))

    square(40, 230, 175, 40, BGSECONDARY, 5)
    square(40, 290, 560, 120, BGSECONDARY, 5)
    screen.blit(text(FONT, "Files:", MID), (50, 228))

    square(232, 500, 175, 45, DARK, 5)
    screen.blit(text(FONT, "COMMIT", MID), (240, 500))
    ...
```

## Taking user input
### Main system
Inputs are taken using `pygame events`.
The program first checks what `state` the gui is in to ensure that the keypress does the right thing, for example:
```python
if state == 'home': # ----> checks the state of the gui
    if event.type == pygame.MOUSEBUTTONDOWN: # ---> checks for clicks
        if pygame.Rect(50, 550, 200, 50).collidepoint(event.pos): 
            state = 'commit'
    if event.type == pygame.KEYDOWN: # ----> checks for key presses
        if event.key == pygame.K_a:
            state = 'commit'
```
### Files and Messages
As `pygame` renders the window `multiple times a second`, we need to store the variables for files and the message `outside of the main loop`.
```python
def main():
    setup()

    running = True
    typing = False

    state = 'home'
    typedtext = ''  # -----> string to use it as text

    files = []  # ---> list as multiple files can be added
    commits = loadcommits()

    while running:
        ...
```
This means that even though the `frame will reset`, it will still be drawing the `same text` onto the screen.

### Typing
To handle the commit message being typed, the program uses a `typing` boolean to track whether the user is currently typing or not.
When the user clicks the message box or presses `j`, `typing` is set to `True`. Each keypress then appends to the `typedtext` string:
```python
if typing:
    if event.key == pygame.K_RETURN:
        typing = False  # ---> stop typing on enter
    elif event.key == pygame.K_BACKSPACE:
        typedtext = typedtext[:-1]  # ---> remove last character
    else:
        typedtext += event.unicode  # ---> add character to message
```
`event.unicode` is used rather than checking each key individually as it handles any character the user types, including symbols and spaces.

## Fixing overflows
When you type or add a file sometimes it may be too long...
Blazer handles this by checking the actual rendered pixel width using pygame's font renderer, trimming characters off the end until it fits, then slapping a `...` on. It's slower than guessing based on character count but it actually works, which is nice.
```python
displayfile = file

while SMALLFONT.size(displayfile)[0] > 560:  # ---> keep trimming until it fits
    displayfile = displayfile[:-1]            # ---> chop one character at a time

displayfile = displayfile[:-3] + '...'       # ---> replace last 3 chars with ellipsis
```
`SMALLFONT.size(displayfile)[0]` returns the rendered pixel width of the string, so unlike estimating from a single character this accounts for the actual width of every character in the string.

## Saving commits
Commits are saved to a hidden `.commits.json` file in the same directory as the program.
Each commit is a dictionary with a message, list of files, a timestamp, and a repo:
```json
{
  "message": "did some work",
  "files": ["/home/user/project/main.py"],
  "timestamp": "2026-03-28",
  "repo": "misc"
}
```
In python, the `Commit` class handles creating and saving these:
```python
class Commit:
    def __init__(self, message, files, timestamp, repo):
        self.message = message
        self.files = files
        self.timestamp = timestamp
        self.repo = repo
```
When committed, it reads the existing json, appends the new commit, and writes it back. This means all previous commits are preserved rather than overwritten.

## The commit grid
The home screen displays a grid of squares representing each day of the current month, similar to a github contributions graph.
The program first builds a frequency table of how many commits were made on each date:
```python
def commitsperday(commits):
    amounts = {}
    for commit in commits:
        datestr = commit[2]
        amounts[datestr] = amounts.get(datestr, 0) + 1
    return amounts
```
Then each square is coloured based on that count — more commits means a lighter square, no commits stays dark. The grid always starts from the 1st of the current month so the squares line up with the actual calendar days.

Colour levels:
- No commits — darkest
- 1 commit — dark
- 2 commits — mid
- 3 commits — light
- 4+ commits — lightest

## Repos
Repos are where commits to do with specific topics are sent to, they get a copy of the committed file and they have their own log. There is a default `misc` repo for general commits, accessible from the home screen via `Add misc commit`.

Each repo is stored as a folder under `.repos/`, containing:
- `log.txt` — a log of all commits to that repo
- copies of any files committed to it

On the repos screen you are able to `scroll` with your mouse to see all of your repos.
This is done through:
```python
def displayreposscreen(repos, typing, reponame, scroll):
    screen.blit(text(BIGFONT, "Repos", MID), (50, 20))
    ...
    ycord = 100 + len(repos) * 70 - scroll  # -----> this displaces each row by the scroll amount
    square(190, ycord, 210, 60, DARK, 5)
    screen.blit(text(FONT, 'add repo', MID), (200, ycord + 15))
    ...
# and
        elif event.type == pygame.MOUSEWHEEL:
            scroll -= event.y * 70  # ----> 70 is the height of each row
            scroll = max(0, scroll)

# scroll is then passed as an argument to displayreposscreen()
```
