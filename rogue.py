# rogue final game

# Python Standard Library
import copy
import random

# Third-Party Libraries
import pygame as pg

# Local Modules
from game import Game
from character import *
from map import *

####### GAME CONSTANTS ############

FPS = 5

DIRECTIONS = {
    "DOWN": (0, +1),
    "UP": (0, -1),
    "RIGHT": (+1, 0),
    "LEFT": (-1, 0),
}

# Game state
# ------------------------------------------------------------------------------

class State:
    def __init__(self, player, map, monsters):
        self.player = player
        self.map = map
        self.monsters = monsters

#######Initiate the game#########

map, rooms_edges = random_map()
#on récupère un élément de sol de notre salle centrale (numéro 4) 
#pour pouvoir y placer notre personnage
x0, x1, y0, y1 = rooms_edges['4']
position = (x0 + 1, y0 + 1)

state = State(Player(position, {}, 12, 16, 0, 5), map, 0)

###### Integration into the general Game frame#######
player = state.player

class RogueGame(Game):
    def process_events(self, events):
        for event in events:
            if (
                event.type == pg.QUIT
                or event.type == pg.KEYDOWN
                and event.key == pg.K_q
            ):
                self.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    player.move(DIRECTIONS["DOWN"], state.map)
                elif event.key == pg.K_UP:
                    player.move(DIRECTIONS["UP"], state.map)
                elif event.key == pg.K_RIGHT:
                    player.move(DIRECTIONS["RIGHT"], state.map)
                elif event.key == pg.K_LEFT:
                    player.move(DIRECTIONS["LEFT"], state.map)
        if player.hits < 1:
            self.quit(error="R.I.P")
    def draw(self):
        self.caption = f"hits = {player.hits}, str = {player.str}, gold = {player.gold}, armor = {player.armor}"
        draw_map(self.screen, state.map)
        x, y = player.position
        draw_tile(self.screen, x, y, ORANGE)

if __name__ == "__main__":
    rogue_game = RogueGame(size=(X * W, Y * H), fps=FPS)
    rogue_game.start()


