#import keras
from pygame import *
import sys
from assets import *
from time import sleep

disp_x, disp_y = 1800, 1000
tower_dim = [100, 600]

p1_png = [image.load('soldier.png'), image.load('tank.png'), image.load('berserker.png')]
p2_png = [image.load('soldier2.png'), image.load('tank2.png'), image.load('berserker2.png')]
background_png = image.load('background.jpg')
tower1_png = image.load('tower1.png')
tower2_png = image.load('tower2.png')

"""
Version 1 is for normal gameplay. There are not AIs implemented. 
"""
def initialization():
    global disp_x, disp_y, fonts, screen, p1_tower, p2_tower, \
    white, red, blue, aqua, green, black, pink, purple, orange, \
    p1_points, p2_points, p1_assets, p2_assets, p1_asset_pos, p2_asset_pos, p1_start_pos, p2_start_pos, p1_health, p2_health

    init()
    font.init()
    fonts = [font.SysFont('Comic Sans MS', 15), font.SysFont('Comic Sans MS', 150), font.SysFont('Gothic', 30)]
    screen = display.set_mode((disp_x, disp_y), 0, 32)
    white = (255, 255, 255);    aqua= (0, 200, 200)
    red = (255, 0, 0);          green = (0, 255, 0)
    blue = (0, 0, 255);         black = (0, 0, 0)
    pink = (255,20,147);        purple = (75,0,130)
    ornge = (255,69,0)

    p1_health = p2_health = tower_dim[1]
    p1_tower = (0,                      disp_y - p1_health, tower_dim[0], p1_health)
    p2_tower = (disp_x-tower_dim[0],    disp_y - p2_health, tower_dim[0], p2_health)
    p1_points = p2_points = 50
    p1_assets = list()
    p2_assets = list()
    p1_asset_pos = list()
    p2_asset_pos = list()
    p1_start_pos = tower_dim[0]
    p2_start_pos = disp_x - tower_dim[0]

def blit():
    global disp_x, disp_y, fonts, screen, p1_tower, p2_tower, \
    white, red, blue, aqua, green, black, pink, purple, orange, \
    p1_points, p2_points, p1_assets, p2_assets, p1_asset_pos, p2_asset_pos, p1_start_pos, p2_start_pos, p1_health, p2_health

    #screen.fill(white)
    screen.blit(background_png, (0, 0))

    draw.rect(screen, red, (0, disp_y - p1_health, tower_dim[0], p1_health))
    draw.rect(screen, blue, (disp_x-tower_dim[0], disp_y - p2_health, tower_dim[0], p2_health))

    for index, i in enumerate(p1_assets):
        screen.blit(p1_png[i.name], (p1_asset_pos[index] - i.size/2, disp_y - i.size))
        #draw.rect(screen, i.color, (p1_asset_pos[index] - i.size/2, disp_y - i.size, i.size, i.size))
    for index, i in enumerate(p2_assets):
        screen.blit(p2_png[i.name], (p2_asset_pos[index] - i.size/2, disp_y - i.size))
        #draw.rect(screen, i.color, (p2_asset_pos[index] - i.size/2, disp_y - i.size, i.size, i.size))
    display.update() 

size = 100

def environment(action1, action2):
    global disp_x, disp_y, fonts, screen, p1_tower, p2_tower, \
    white, red, blue, aqua, green, black, pink, purple, orange, \
    p1_points, p2_points, p1_assets, p2_assets, asset_list, p1_asset_pos, p2_asset_pos, p1_start_pos, p2_start_pos, p1_health, p2_health, p1_kill, p2_kill
    p1_reward = p2_reward = 0
    winner = ""
    terminal = False
    if action1 != 3:
        if action1 == 0:
            asset_a = soldier()
        elif action1 == 1:
            asset_a = tank()
        elif action1 == 2:
            asset_a = Berserker()
        if len(p1_assets) > 10 or p1_points < asset_a.cost:
            p1_reward -= 10
        else:
            p1_assets.append(asset_a)
            p1_asset_pos.append(p1_start_pos + size / 2)
            p1_points -= asset_a.cost
    #print(len(p1_assets))
    if action2 != 3:
        if action2 == 0:
            asset_b = soldier()
        elif action2 == 1:
            asset_b = tank()
        elif action2 == 2:
            asset_b = Berserker()
        if len(p2_assets) > 10 or p2_points < asset_b.cost:
            p2_reward -= 10
        else:
            p2_assets.append(asset_b)
            p2_asset_pos.append(p2_start_pos - size / 2)
            p2_points -= asset_b.cost

    for index, i in enumerate(p1_assets):
        moved_flag = 0
        for index2, j in enumerate(p2_assets):
            if p1_asset_pos[index] + i.size / 2 >= p2_asset_pos[index2] - j.size / 2:
                p1_asset_pos[index] = p1_asset_pos[index] - (p1_asset_pos[index] + i.size / 2 - p2_asset_pos[index2] - j.size / 2)#p1_asset_pos[index] + i.size / 2 - p2_asset_pos[index2] - j.size / 2
                j.health -= i.attack
                i.health -= j.attack
                moved_flag = 1
        if moved_flag == 0:
            if p1_asset_pos[index] + i.size / 2 >= disp_x - tower_dim[0]:
                p1_asset_pos[index] = disp_x - tower_dim[0] - i.size / 2
                p2_health -= i.attack
                if p2_health <= 0:
                    terminal = True
                    winner = "1"
            else:
                p1_asset_pos[index] += i.speed

    for index, i in enumerate(p2_assets):
        moved_flag = 0
        for index2, j in enumerate(p1_assets):
            if p2_asset_pos[index] - i.size / 2 <= p1_asset_pos[index2] + j.size / 2:
                p2_asset_pos[index] = p2_asset_pos[index] + p1_asset_pos[index2] + j.size / 2 - p2_asset_pos[index] - i.size / 2#[p2_asset_pos[index] + i.size / 2 - p2_asset_pos[index] + i.size / 2 - p1_asset_pos[index2] - j.size / 2]
                j.health -= i.attack
                i.health -= j.attack
                moved_flag = 1
        if moved_flag == 0:
            if p2_asset_pos[index] - i.size / 2 <= tower_dim[0]:
                p2_asset_pos[index] = tower_dim[0] + i.size / 2
                p1_health -= i.attack
                if p1_health <= 0:
                    terminal = True
                    winner = "2"
            else:
                p2_asset_pos[index] -= i.speed

    for index, i in enumerate(p1_assets):
        if i.health <= 0:
            p1_assets.remove(i)
            p1_asset_pos.remove(p1_asset_pos[index])
            p2_kill += 1
    for index, i in enumerate(p2_assets):
        if i.health <= 0:
            p2_assets.remove(i)
            p2_asset_pos.remove(p2_asset_pos[index])
            p1_kill += 1

    return terminal, winner



"""--------------------------GAME LOOP--------------------------"""
while True:
    initialization()
    terminal = False
    p1_kill = 1
    p2_kill = 1
    episode = 0
    a_lastturn = 0
    b_lastturn = 0
    while not terminal:
        episode += 1
        for e in event.get():
            if e.type==QUIT:
                quit()
                sys.exit()

        keys = key.get_pressed()
        if a_lastturn >= 5:
            if keys[K_q]:
                p1_a = 0
            elif keys[K_w]:
                p1_a = 1
            elif keys[K_e]:
                p1_a = 2
            a_lastturn = 0
        else:
            p1_a = 3
            a_lastturn += 1

        if b_lastturn >= 5:
            if keys[K_i]:
                p2_a = 0
            elif keys[K_o]:
                p2_a = 1
            elif keys[K_p]:
                p2_a = 2
            b_lastturn = 0
        else:
            p2_a = 3
            b_lastturn += 1
        print(p1_a, p1_points, len(p1_assets))
        terminal, winner = environment(p1_a, p2_a)
        blit()
        if episode % 10 == 0:
            p1_points += int(p1_kill*2)
            p2_points += int(p2_kill*2)