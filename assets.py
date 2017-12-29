"""
4(5?) types of parameters:
    1. Attack or Defense        1 or 2
    2. Attack/Defense points    5~20
    3. Remaining health         0~20
    4. Move speed               5~20
    5. Cost                     5~20

6 Types of assets.

1. Soldier      1   5   10   10     5
2. Tank         1   10  20   5      10
3. Berserker    1   20  5    20     10
4. Shield       0   8   -    8      5
5. Phalanx      0   12  -    5      10
6. Batallion    0   16  -    1      10


-------Game specs--------
First, we'll try using only the 3 attack assets. 

"""
white = (255, 255, 255);    aqua= (0, 200, 200)
red = (255, 0, 0);          green = (0, 255, 0)
blue = (0, 0, 255);         black = (0, 0, 0)
pink = (255,20,147);        purple = (75,0,130)
ornge = (255,69,0)
class soldier:
    name = 0
    def __init__(self):
        self.attack = 0.1
        self.health = 6
        self.speed  = 1
        self.cost   = 5
        self.size = 100
        self.color = black
        

class tank:
    name = 1
    def __init__(self):
        self.attack = 0.1
        self.health = 20
        self.speed  = 0.5
        self.cost   = 10
        self.size = 100
        self.color = green

class Berserker:
    name = 2
    def __init__(self):
        self.attack = 0.2
        self.health = 10
        self.speed  = 2
        self.cost   = 10
        self.size = 100
        self.color = pink

class Shield:
    def __init__(self):
        self.defense = 8
        self.speed  = 8
        self.cost   = 5
        self.size = 10
        self.color = aqua
        
class Phalanx:
    def __init__(self):
        self.defense = 12
        self.speed  = 5
        self.cost   = 10
        self.size = 10
        self.color = orange
        
class Batallion:
    def __init__(self):
        self.defense = 16
        self.speed  = 1
        self.cost   = 10
        self.size = 10
        self.color = purple
        