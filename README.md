# Blazer

A gui to track progress on anything - such as revision, in a way to provide maximum customisation options to make it your own
Designed to guilt trip you and keep you addicted to keeping up your productivity steak, with full customisibility
File selection is kinda ugly, sorry about that had to use tkinter cos pygame dosent work as well for it 
Currently only linux compatible, if theres demmand for whatever reason and someone actually good at coding cant be bothered to make a better 
version there will be compatibility updates for mac and windows
## Install
```bash
# Recommended
pipx install git+https://github.com/demtellme/Blazer.git

# Or with pip
pip install --user git+https://github.com/demtellme/Blazer.git
```

## Uninstall
```bash
pipx uninstall Blazer
```

## Usage
```bash
blzr # runs the program
```
You can use the gui buttons to operate the program or specific keys whilst in the window,
If you want to use a mouse to add files or a commit message click on the provided area
### Home Screen
    a - opens the Commit Screen
### Commit Screem
    f - adds a file 
    j - allows you to start typing the commit message, `Enter` to stop 
# Customisation
Go into `config.json`, under the `USER` section, select the options you want to use for your Blazer app

*For example*: 

```json
//one of my prefered setups
  "USER": {
    "colourscheme": "forest",   // Changing forest -> ocean to change the base pallet to be blue
    "background": "dark23",     // Changing dark23 -> solarized to change the background
    "font": "notoserif",        // you probably get it by now
    "fontsize": 40              // There arent presets for font size so you can change it yourself
    // but be aware as theres no presets for font size it may cause the program to look ugly
  },
```



# Boring documentatation for nerds
###### Dont get offended, you gotta be a certain level of nerd to wanna know how a specific program works
## Getting the configuration for user's customisations

The config is stored as a `.json` file,
This is so there can be set presets without them needing to be hardcoded into the python, 
personally id much rather edit a json than a python file for customisation
THEREFORE, it allows for more user customisation as you can add or remove whatever you like!
Which is what you should do with all apps to make them truly yours

so in python we need to
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
The `CONF = [...]` line is to make sure were using the right config file, in the same folder as the program
The data from that file is then saved as `config` using the json library
Then the part we actually care about, `USER` is set as `userconfig` which is a list of the user choices.

```python
tuple() 
```
is used for making the list into an array () that is needed for certain pygame features () 

The code then finds the user `colourscheme` in the `colourschemes` part of the json file and reads the list of colours as arrays
A similar process is used for all the other parts of the user's config

## The user interface

Blazer uses `pygame` as a gui, there are much better ways im sure but oh well
To display the main user iterface the program uses 
```python
#functions already defined earlier in the code
 if state == 'home':
            dipslayhomescreen()
elif state == 'commitscreen':
    displaycommitscreen()
```
this checks what `state` the gui should be in and renders it appropriatley
to display actual ui elements the functions use rectangles and text with functions:
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
            state = 'commitscreen'
    if event.type == pygame.KEYDOWN: # ----> checks for key presses
        if event.key == pygame.K_a:
            state='commitscreen'
```
### Files and Messages
As `pygame` renders the window `multiple times a seccond`, we need to store the variables for files and the message `outside of the main loop`.
```python
def main():
    setup()

    running = True
    typing = False

    state = 'home'
    message = '' # -----> string to use it as text

    files = [] # ---> list as multiple files can be added
    commits = loadcommits()

    while running:
        ...
```
This will mean that even though the `frame will reset`, it will still be drawing the `same text` onto the screen

### Typing
To handle the commit message being typed, the program uses a `typing` boolean to track whether the user is currently typing or not.
When the user clicks the message box or presses `j`, `typing` is set to `True`. Each keypress then appends to the `message` string:
```python
if typing:
    if event.key == pygame.K_RETURN:
        typing = False  # ---> stop typing on enter
    elif event.key == pygame.K_BACKSPACE:
        message = message[:-1]  # ---> remove last character
    else:
        message += event.unicode  # ---> add character to message
```
`event.unicode` is used rather than checking each key individually as it handles any character the user types, including symbols and spaces

## Saving commits
Commits are saved to a hidden `.commits.json` file in the same directory as the program.
Each commit is a dictionary with a message, list of files, and a timestamp:
```json
{
  "message": "did some work",
  "files": ["/home/user/project/main.py"],
  "timestamp": "2026-03-28"
}
```
In python, the `Commit` class handles creating and saving these:
```python
class Commit:
    def __init__(self, message, files, timestamp):
        self.message = message
        self.files = files
        self.timestamp = timestamp
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
