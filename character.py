#manages character
from platform import java_ver
import random as rd
from turtle import pos

class Player:
    def __init__(self, position, items, hits, str, gold, armor, stepcount=0):
        self.position = position
        self.items = items #dict of items
        self.hits = hits   # number of hits when defeat lose hits when victory gain hits
        #1 hit point is gained every 18 steps
        self.str = str     # I didn't understand its use
        self.gold = gold   # number of pieces grabbed, can pay rooms' gardens
        self.armor = armor  #level of protection, less chances to lose a fight when high
        #grab armors to increase protection
        self.stepcount = stepcount # counts the moves done to 18
    def move(self, direction, map, rooms_edges, monster_positions, item_positions):
        x, y = self.position
        dx, dy = direction
        pos = [x + dx, y + dy]
        possible = map['green'] + map['grey']
        if pos in possible:
            if self.position in map['grey'] and pos in map['green']: #ie entrée dans une salle
                #find which room we're in 
                for elem in rooms_edges.keys():
                    ileft, iright, idown, iup = rooms_edges[elem]
                    if ileft < pos[0] and pos[0] < iright and idown < pos[1] and pos[1] < iup:
                        il, ir, id, iu = ileft, iright, idown, iup 
                        break
                if rd.uniform(0,1) < 0.7 : #on génère un monstre
                    x = rd.randint(il+1, ir-1)
                    y = rd.randint(id + 1, iu - 1)
                    while [x, y] in monster_positions or [x, y] in item_positions[:][0:2]:
                        x = rd.randint(il+1, ir-1)
                        y = rd.randint(id + 1, iu - 1)
                    monster_positions.append([x,y])
                if rd.uniform(0,1) < 0.3: #on génère un objet
                    c = rd.uniform(0, 1)
                    if c < 0.5: #ca sera du gold
                        x = rd.randint(il+1, ir-1)
                        y = rd.randint(id + 1, iu - 1)
                        while [x, y] in monster_positions or [x, y] in item_positions[:][0:2]:
                            x = rd.randint(il+1, ir-1)
                            y = rd.randint(id + 1, iu - 1)
                        v = rd.randint(10,60)
                        item_positions.append([x, y, 'g', v])
                    elif c < 0.8: # ca sera du armor
                        x = rd.randint(il+1, ir-1)
                        y = rd.randint(id + 1, iu - 1)
                        while [x, y] in monster_positions or [x, y] in item_positions[:][0:2]:
                            x = rd.randint(il+1, ir-1)
                            y = rd.randint(id + 1, iu - 1)
                        v = rd.randint(1, 3)
                        item_positions.append([x, y, 'a', v])
                    else: #ca sera du food
                        x = rd.randint(il+1, ir-1)
                        y = rd.randint(id + 1, iu - 1)
                        while [x, y] in monster_positions or [x, y] in item_positions[:][0:2]:
                            x = rd.randint(il+1, ir-1)
                            y = rd.randint(id + 1, iu - 1)
                        v = rd.randint(5, 20)
                        item_positions.append([x, y, 'f', v])
            self.position = pos
            self.stepcount += 1
            to_pop = []
            for i in range(len(item_positions)):
                #si on tombe sur un objet, on le récupère
                if pos == item_positions[i][0:2]:
                    if item_positions[i][2] == 'f':
                        self.items.append(item_positions[i])
                        to_pop.append(i)
                    elif item_positions[i][2] == 'g':
                        self.gold += item_positions[i][3]
                        to_pop.append(i)
                    elif item_positions[i][2] == 'a':
                        self.armor += item_positions[i][3]
                        to_pop.append(i)
            for i in to_pop:
                item_positions.pop(i)
            to_pop = []
            for i in range(len(monster_positions)):
                elem = monster_positions[i]
                if pos == elem:# si on tombe sur un monstre, on le combat
                    if rd.uniform(0,1) > 0.7 - self.armor*0.005: #victoire
                        self.hits += rd.randint(1,2)
                        to_pop.append(i)
                    else:
                        self.hits -= rd.randint(1,2)
                        to_pop.append(i)
            for i in to_pop:
                monster_positions.pop(i)
            #si le player est dans la même salle qu'un monstre, le monstre le poursuit
            #salle du player
            if pos in map['green']:    
                for key in rooms_edges.keys():
                    ileft, iright, idown, iup = rooms_edges[key]
                    if ileft < pos[0] and pos[0] < iright and idown < pos[1] and pos[1] < iup:
                        il, ir, id, iu = rooms_edges[key]
                    for r in range(len(monster_positions)):
                        elem = monster_positions[r]
                        #si même salle 
                        if il < elem[0] and elem[0] < ir and id < elem[1] and elem[1] < iu:
                        #on cherche la direction qui rapproche le plus du player
                            i, j = elem
                            k, l = pos
                            if i < k:
                                i += 1
                            if i > k:
                                i-=1
                            if j < l:
                                j += 1
                            if j > l:
                                j -= 1
                            monster_positions[r] = i, j
        else:
            pass

# items_list = [armor, gold, food]

class Items:
    def __init__(self, item_positions):
        #item_positions is a list of 4 elements lists 2 firsts indicate position
        #the 3rd the type ('a', 'g' or 'f'), the 4th the value
        self.item_positions = item_positions

class Monster:#Je ne construit qu'un type de monstre
    def __init__(self, positions):
        #positions is a list of positions( list of 2 elements)
        self.positions = positions
    def add(self, position):
        self.positions.append(position)




