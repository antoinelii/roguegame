#manages character
class Player:
    def __init__(self, position, items, hits, str, gold, armor):
        self.position = position
        self.items = items #dict of items
        self.hits = hits   # number of hits when defeat lose hits when victory gain hits
        #1 hit point is gained every 18 steps
        self.str = str     # I didn't understand its use
        self.gold = gold   # number of pieces grabbed, can pay rooms' gardens
        self.armor = armor  #level of protection, less chances to lose a fight when high
        #grab armors to increase protection
    def move(self, direction, map):
        x, y = self.position
        dx, dy = direction
        pos = [x + dx, y + dy]
        possible = map['green'] + map['grey']
        if pos in possible:
            self.position = pos
        else:
            pass




