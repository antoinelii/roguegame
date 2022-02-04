#create map
#We cut the 90x60 cells screen into a 3x3 grid of 30x20 cells rectangles
#In each rectangle, we randomly draw a room
import random as rd
import numpy as np
import pygame as pg

#### CONSTANTS ######
W, H = 10, 10  # Cell width and height
X, Y = 90 , 60 # nb of cells horizontally and vertically
#I chose 90, 60 so we can divide the screen in a 3x3 grid of 30,20 rectangles

ORANGE = (255, 127, 0)       # player's color
YELLOW = (255, 255, 0)       # item's color
WHITE = (255, 255, 255)      # monsters' color
GREEN = (57, 255, 20)        # green points to symbolize floor
BLACK = (0, 0, 0)      # background's color
BROWN = (180, 85, 0)         # walls' color
GREY =  (60, 60, 60)      # paths' color

def map_pattern():
    """Returns a 2 element- list with a list of rectangles where there will be 
    a rooom and a list of paths (pairs) between those rooms.
    We randomly choose a number of rooms between 4 and 9
    To simplify, we choose to have a central room and the 4 rooms next to it
    and add 0 to 4 rooms
    distributed in the other rectangles. 
    We enumerate them from left to right, down to top, left-down
    rectangle is rectangle number 0"""
    rooms = [4, 1, 3, 5, 7] #central room is the first element of the list
    nb_added_rooms = rd.randint(0,4)
    rooms += rd.sample([0, 2, 6, 8], nb_added_rooms)
    #we only build paths between rooms of contiguous rectangles ie
    paths = []
    for i in rooms:
        for j in rooms:
            if i<j: #we don't want (x, y) and (y, x)
                if abs(i-j)==3 or (abs(i-j)==1 and i//3 ==j//3):
                    paths.append((i,j)) 
    return [rooms, paths]

def random_room(width = 30, height = 20):
    """Returns a 4-tuple (x, y, dx, dy) position and size of a randomly created 
    room in a rectangle.
    We want to define rooms within the big rectangles. We randomly choose the size 
    of the room (width between 2 and width-6, height bet2 and height-4)
    We will then add walls around it.
    Then we randomly choose the position with consideration to the size of the room
    We also want to leave room between the wall and the edges of the rectangle so we 
    can build paths between rooms"""
    dx = rd.randint(3, width - 6)
    dy = rd.randint(3, height - 4)
    #Choose down-left corner brick position
    x = rd.randint(1, width - (dx + 3))
    y = rd.randint(1, height - (dy + 3))
    return x, y, dx, dy

def random_map():
    """ 
    Returns a dict of colors' lists of cells and rooms' data
    Each cell (x, y) is represented by a color to define its type
    For each permanent element of the map( walls/brown, floor/green, path/grey)
    we build a list of the cells coordinates in the specified color. 
    We don't need to do a list of black elements (it will be the color of the background)
    """
    rooms, paths = map_pattern()
    brown = []
    green = []
    grey = []
    rooms_edges = {}
    #we draw the rectangles
    for i in rooms: 
        #set origin of the relative rectangle
        x0, y0 = i%3*30, i//3*20
        x, y, dx, dy = random_room()
        #we record rooms' data in a dict
        rooms_edges[f'{i}'] = [x0 + x, x0 + x + dx + 1, y0 + y, y0 + y +dy + 1]
        #draw the rectangle
        #bottom wall and top wall
        for k in range (x0 + x, x0 + x + dx +2):
            brown.append([k, y0 + y])
            brown.append([k, y0 + y + dy +1])
        #other walls and floor
        for l in range (y0 + y + 1, y0 + y + dy + 1):
            brown.append([x0 + x, l]) #left wall
            brown.append([x0 + x + dx +1, l])#right wall
            for k in range (1, dx + 1):
                green.append([x0 + x + k, l]) #floor
    #############
    #we draw the paths
    for i, j in paths:
        ileft, iright, idown, iup = rooms_edges[f'{i}']
        jleft, jright, jdown, jup = rooms_edges[f'{j}']
        if j - i == 3: # j is above i
            #we will draw a path from i top edge to j bottom edge
            k = rd.randint(ileft + 1, iright - 1)
            l = iup
            grey.append([k, l])
            m = rd.randint(jleft + 1, jright - 1)
            n = jdown
            grey.append([m, n])
            #we first join them vertically
            while n-l > 1:
                l = l + 1
                n = n - 1
                grey.append([k, l])
                grey.append([m, n])
            if n - l == 1:
                l = l + 1
                grey.append([k, l])
            #we then join them horizontally
            if k < m:
                while k < m:
                    k = k + 1
                    grey.append([k, l])
            else:
                while m < k:
                    k = k - 1
                    grey.append([k, l])
        else: #i and j are on the same line i on j's left
            #we will draw a path from i right edge to j left edge
            l = rd.randint(idown + 1, iup - 1)
            k = iright
            grey.append([k, l])
            n = rd.randint(jdown + 1, jup - 1)
            m = jleft
            grey.append([m, n])
            #we first join them horizontally
            while m - k > 1:
                k = k + 1
                m = m - 1
                grey.append([k, l])
                grey.append([m, n])
            if m - k == 1:
                k = k + 1
                grey.append([k, l])
            #we then join them vertically
            if l < n:
                while l < n:
                    l = l + 1
                    grey.append([k, l])
            else:
                while n < l:
                    l = l - 1
                    grey.append([k, l])
    colors = {'brown': brown, 'green': green, 'grey': grey}
    return colors, rooms_edges
    
def draw_tile(screen, x, y, color):
    """
    x and y in tiles coordinates
    translate into pixel coordinates for painting
    """
    rect = pg.Rect(x * W, y * H, W, H)
    pg.draw.rect(screen, color, rect)

def draw_point(screen, x, y, color):
    """
    x and y in tiles coordinates
    translate into pixel coordinates for painting
    """
    rect = pg.Rect(x * W + W//2, y * H + H//2, 1, 1)
    pg.draw.rect(screen, color, rect)

map, rooms_edges = random_map()

def draw_map(screen, map):
    '''Draws the background, floors, walls, paths'''
    screen.fill(BLACK)
    for x, y in map['brown']:
        draw_tile(screen, x, y, BROWN)
    for x, y in map['grey']:
        draw_tile(screen, x, y, GREY)
    for x, y in map['green']:
        draw_point(screen, x, y, GREEN)
