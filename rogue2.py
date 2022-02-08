# rogue final game

# Python Standard Library
import copy
import random

# Third-Party Libraries
import pygame as pg

# Local Modules
from game import Game
from character2 import *
from map import *

####### GAME CONSTANTS ############

FPS = 10

DIRECTIONS = {
    "DOWN": (0, +1),
    "UP": (0, -1),
    "RIGHT": (+1, 0),
    "LEFT": (-1, 0),
}
######functions ########
def which_room(position, rooms_edges):
    for elem in rooms_edges.keys():
        ileft, iright, idown, iup = rooms_edges[elem]
        if ileft < position[0] and position[0] < iright and idown < position[1] and position[1] < iup:
            return ileft, iright, idown, iup, elem

# Game state
# ------------------------------------------------------------------------------

class State:
    def __init__(self, player, map, rooms_edges, monsters_list, items_list):
        self.player = player
        self.map = map
        self.rooms_edges = rooms_edges
        #list of Monster class elements
        self.monsters_list = monsters_list
        #list of Item class elements
        self.items_list = items_list
    #On veut définir une fonction pour déplacer le player et les 
    #éventuels monstres dans la salle
    def move(self, direction):
        x, y = self.player.position
        dx, dy = direction
        pos = [x + dx, y + dy]
        path = map['grey']
        floor = map['green']
        #On peut se déplacer sur le sol ou les chemins
        #on commence par voir si on est sur un chemin
        if pos in path:
            #dans ce cas (je ne mets pas de monstre/objet dans les chemins
            # pour simplifier) on déplace simplement le player
            self.player.position = pos
        elif pos in floor:
            il, ir, id, iu, room = which_room(pos, self.rooms_edges)
            if self.player.position in path: #ie entrée dans une salle depuis chemin
                if rd.uniform(0,1) < 0.3 + self.player.armor*0.005: #on génère un monstre
                    items_positions = [[elem.x, elem.y] for elem in self.items_list]
                    monsters_positions = [[elem.x, elem.y] for elem in self.monsters_list]
                    x = rd.randint(il+1, ir-1)
                    y = rd.randint(id + 1, iu - 1)
                    while [x, y] in items_positions or [x, y] in monsters_positions:
                        x = rd.randint(il+1, ir-1)
                        y = rd.randint(id + 1, iu - 1)
                    state.monsters_list.append(Monster(x, y))
                if rd.uniform(0,1) < 0.2: #on génère un objet
                    items_positions = [[elem.x, elem.y] for elem in self.items_list]
                    monsters_positions = [[elem.x, elem.y] for elem in self.monsters_list]
                    c = rd.uniform(0, 1)
                    if c < 0.5: #ca sera du gold
                        x = rd.randint(il+1, ir-1)
                        y = rd.randint(id + 1, iu - 1)
                        while [x, y] in items_positions or [x, y] in monsters_positions:
                            x = rd.randint(il+1, ir-1)
                            y = rd.randint(id + 1, iu - 1)
                        v = rd.randint(10,60)
                        state.items_list.append(Item(x, y, 'g', v))
                    elif c < 0.8: # ca sera du armor
                        x = rd.randint(il+1, ir-1)
                        y = rd.randint(id + 1, iu - 1)
                        while [x, y] in items_positions or [x, y] in monsters_positions:
                            x = rd.randint(il+1, ir-1)
                            y = rd.randint(id + 1, iu - 1)
                        v = rd.randint(1, 3)
                        state.items_list.append(Item(x, y, 'a', v))
                    else: #ca sera du food
                        x = rd.randint(il+1, ir-1)
                        y = rd.randint(id + 1, iu - 1)
                        while [x, y] in items_positions or [x, y] in monsters_positions:
                            x = rd.randint(il+1, ir-1)
                            y = rd.randint(id + 1, iu - 1)
                        v = rd.randint(5, 20)
                        state.items_list.append(Item(x, y, 'f', v))
            self.player.position = pos
            self.player.stepcount += 1
            #si le player est dans la même salle qu'un monstre, le monstre le poursuit
            #salle du player
            for r in range(len(self.monsters_list)):
                elem = self.monsters_list[r]
                #si même salle 
                if il < elem.x and elem.x < ir and id < elem.y and elem.y < iu:
                #on cherche la direction qui rapproche le plus du player
                    i, j = elem.x, elem.y
                    k, l = pos
                    #si assez loin du player
                    if abs(k-i) + abs(j-l) > 1:
                        if i < k:
                            i += 1
                        elif j > l:
                            j += -1
                        elif j < l:
                            j += 1
                        elif i > k:
                            i += -1
                        items_positions = [[elem.x, elem.y] for elem in self.items_list]
                        monsters_positions = [[elem.x, elem.y] for elem in self.monsters_list]
                        if [x, y] not in items_positions and [x, y] not in monsters_positions:
                            self.monsters_list[r].x = i
                            self.monsters_list[r].y = j
        else:
            pass
    def grab_item(self, position, items_list):
        to_pop = []
        for i in range(len(items_list)):
        #si on tombe sur un objet, on le récupère
            if position == [items_list[i].x, items_list[i].y]:
                if items_list[i].type == 'f':
                    self.player.items[items_list[i].type + 'ood'] = items_list[i].value
                elif items_list[i].type == 'g':
                    self.player.gold += items_list[i].value
                elif items_list[i].type == 'a':
                    self.player.armor += items_list[i].value
                to_pop.append(i)
        for i in to_pop[::-1]:
            items_list.pop(i)
    def fight_monster(self, monsters_list):
        to_pop = []
        for i in range(len(monsters_list)):
            monster_pos = [monsters_list[i].x, monsters_list[i].y]
            if self.player.position == monster_pos:# si on tombe sur un monstre, on le combat
                if rd.uniform(0,1) > 0.8 - self.player.armor*0.005: #victoire
                    self.player.hits += rd.randint(1,2)
                else:
                    self.player.hits += -rd.randint(1,2)
                to_pop.append(i)
        for i in to_pop[::-1]:
            monsters_list.pop(i)
#######Initiate the game#########

#On génère une map aléatoire
map, rooms_edges = random_map()
#on récupère un élément de sol de notre salle centrale (numéro 4) 
#pour pouvoir y placer notre personnage
x0, x1, y0, y1 = rooms_edges['4']
position = (x0 + 1, y0 + 1)

state = State(Player(position, {}, 12, 16, 0, 5), map, rooms_edges, [], [])

###### Integration into the general Game frame#######

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
                    state.move(DIRECTIONS["DOWN"])
                elif event.key == pg.K_UP:
                    state.move(DIRECTIONS["UP"])
                elif event.key == pg.K_RIGHT:
                    state.move(DIRECTIONS["RIGHT"])
                elif event.key == pg.K_LEFT:
                    state.move(DIRECTIONS["LEFT"])
        #regarde si tombe objet
        #le prend et le supprime
        state.grab_item(state.player.position, state.items_list)
        #regarde si tombe monstre et le combat
        state.fight_monster(state.monsters_list)
        #recharge des hits
        if state.player.stepcount >18:
            state.player.hits += 1
            state.player.stepcount = 0
        #death condition
        if state.player.hits < 1:
            self.quit(error="R.I.P")
    def draw(self):
        self.caption = f"hits = {state.player.hits}, str = {state.player.str}, gold = {state.player.gold}, armor = {state.player.armor}, items = {state.player.items}"
        draw_map(self.screen, state.map)
        for elem in state.monsters_list:
            x, y = elem.x, elem.y
            draw_tile(self.screen, x, y, WHITE)
        for elem in state.items_list:
            x, y = elem.x, elem.y
            draw_tile(self.screen, x, y, YELLOW)
        x, y = state.player.position
        draw_tile(self.screen, x, y, ORANGE)

if __name__ == "__main__":
    rogue_game = RogueGame(size=(X * W, Y * H), fps=FPS)
    rogue_game.start()