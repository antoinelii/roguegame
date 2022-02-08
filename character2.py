from platform import java_ver
import random as rd
from turtle import pos

class Player:
    def __init__(self, position, items, hits, str, gold, armor, stepcount=0):
        self.position = position
        self.items = items #dict of Item class items
        self.hits = hits   # number of hits when defeat lose hits when victory gain hits
        #1 hit point is gained every 18 steps
        self.str = str     # I didn't understand its use
        self.gold = gold   # number of pieces grabbed, can pay rooms' gardens
        self.armor = armor  #level of protection, less chances to lose a fight when high
        #grab armors to increase protection
        self.stepcount = stepcount # counts the moves done to 18
    

# items_list = [armor, gold, food]

class Item:
    def __init__(self, x, y, type, value):
        #item_positions is a list of 4 elements lists 2 firsts indicate position
        #the 3rd the type ('a', 'g' or 'f'), the 4th the value
        self.x = x
        self.y = y
        self.type = type
        self.value = value

class Monster:#Je ne construit qu'un type de monstre
    def __init__(self, x, y):
        self.x = x
        self.y = y

