"""
    Aven F.  Example Game
    Copyright (C) 2022 Aven F
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    If you want a copy of this source code: https://github.com/xftransformers
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import pgzrun
import random
import math
import time

def colliding(temp, check_trees=True, check_boulders=True):
    """
    function to check if an actor is colliding with any trees or boulders
    :param temp: the actor
    :return: returns true if it does collide, false if it does not
    """

    if check_trees:
        for test_tree in trees:
            if temp.colliderect(test_tree):
                return True
    if check_boulders:
        for test in boulders:
            if temp.colliderect(test):
                return True

    return False



def random_position(actor):
    actor.pos = random.randint(0,WIDTH),random.randint(0,HEIGHT)
    while colliding(actor):
        actor.pos = random.randint(0, WIDTH), random.randint(0, HEIGHT)

def generate():
    global trees
    global boulders
    trees = []
    boulders = []
    for x in range(10):
        temp = Actor('tree')
        random_position(temp)
        trees.append(temp)
    for x in range(10):
        temp = Actor('boulder')
        random_position(temp)
        boulders.append(temp)

def draw():
    for x in range(int(WIDTH/grass.width)):
        for y in range(int(HEIGHT/grass.height)):
            screen.blit('grass',(grass.width*x,grass.height*y))
    monster.draw()
    player.draw()
    for x in trees:
        x.draw()
    for x in boulders:
        x.draw()
    for x in swords:
        x.draw()
    screen.draw.text(f"Monster health: {monster_health}", bottomright=(WIDTH,HEIGHT),color=(255, 0, 0), fontsize=32, background="black")
    if is_game_over():
        if monster.colliderect(player) and monster_health > 0:
            screen.draw.text("GAME OVER!", center=(WIDTH / 2, HEIGHT / 2), color=(255, 0, 0), fontsize=32, background="black")
            screen.draw.text("Press enter to restart", center=(WIDTH / 2, HEIGHT / 2 +50), background="black")
        if monster_health <= 0:
            screen.draw.text("YOU WIN!", center=(WIDTH / 2, HEIGHT / 2), color=(255, 0, 0), fontsize=32, background="black")
            screen.draw.text("Press enter to restart", center=(WIDTH / 2, HEIGHT / 2 +50), background="black")

def step(input): # calculates when to change character's image
    output = input // 40 # How often
    output = int(output % 2) # gets rid of the decimal point and gives either a 1 or 0
    return output

def update():
    global monster_health

    if not is_game_over():
        move_link()
        move_monster()
        move_swords()

def is_game_over():
    return (monster.colliderect(player) or monster_health <= 0)



def move_monster():
    global frames_since_hidden
    global monster_hidden_direction
    if not colliding(player, check_boulders=False):
        move_monster_normally()
    else:
        if monster.distance_to(player) > 200:
            frames_since_hidden = 0
            move_monster_normally()
        else:
            if frames_since_hidden == 0:
                monster_hidden_direction = random.randint(-180, 180)

            if frames_since_hidden < 125:
                if not monster.colliderect(player):
                    monster.top -= math.sin(math.radians(monster_hidden_direction)) * monster_speed
                    monster.left += math.cos(math.radians(monster_hidden_direction)) * monster_speed
                    monster_direction(monster_hidden_direction)
                frames_since_hidden += 1
            else:
                frames_since_hidden = 0

def move_swords():
    for x in swords[:]:
        if x.image == 'sword_0':
            x.top += sword_speed
            if x.top > HEIGHT:
                swords.remove(x)
        if x.image == 'sword_1':
            x.left -= sword_speed
            if x.left < 0:
                swords.remove(x)
        if x.image == 'sword_2':
            x.top -= sword_speed
            if x.top < 0:
                swords.remove(x)
        if x.image == 'sword_3':
            x.left += sword_speed
            if x.left > WIDTH:
                swords.remove(x)
        did_sword_hit_monster(x)

def did_sword_hit_monster(x):
    global monster_health
    global swords
    if x.colliderect(monster):
        swords.remove(x)
        monster_health -= 1

def move_link():
    if keyboard.up or keyboard.w:
        player.top -= player_speed
        player.image = f'link_b{step(player.pos[1])}'
        if colliding(player, check_trees=False):
            player.top += player_speed
    if keyboard.down or keyboard.s:
        player.top += player_speed
        player.image = f'link_f{step(player.pos[1])}'
        if colliding(player, check_trees=False):
            player.top -= player_speed
    if keyboard.left or keyboard.a:
        player.left -= player_speed
        player.image = f'link_l{step(player.pos[0])}'
        if colliding(player, check_trees=False):
            player.left += player_speed
    if keyboard.right or keyboard.d:
        player.left += player_speed
        player.image = f'link_r{step(player.pos[0])}'
        if colliding(player, check_trees=False):
            player.left -= player_speed

    if player.left > WIDTH: # when i walk off to the right
        player.right = 0
        generate()
        monster.left -= WIDTH
    if player.right < 0: # when i walk off to the left
        player.left = WIDTH
        generate()
        monster.left += WIDTH
    if player.top > HEIGHT: # when i walk off the bottom
        player.bottom = 0
        generate()
        monster.top -= HEIGHT
    if player.bottom < 0: # when i walk off the top
        player.top = HEIGHT
        generate()
        monster.top += HEIGHT

def move_monster_normally():
    if not monster.colliderect(player):
        monster.top -= math.sin(math.radians(monster.angle_to(player)))*monster_speed
        monster.left += math.cos(math.radians(monster.angle_to(player)))*monster_speed
        monster_direction(monster.angle_to(player))

def monster_direction(movement_angle):
    if movement_angle > 45 and movement_angle < 135:
        monster.image = f'monster_b{step(monster.pos[1])}'
    elif movement_angle > -45 and movement_angle < 45:
        monster.image = f'monster_r{step(monster.pos[0])}'
    elif movement_angle > -135 and movement_angle < -45:
        monster.image = f'monster_f{step(monster.pos[1])}'
    elif movement_angle > 135 or movement_angle < -135:
        monster.image = f'monster_l{step(monster.pos[0])}'

def on_mouse_down():
    sword_mapping = {
        'link_f0':'sword_0',
        'link_f1':'sword_0',
        'link_b0':'sword_2',
        'link_b1':'sword_2',
        'link_l0':'sword_1',
        'link_l1':'sword_1',
        'link_r0':'sword_3',
        'link_r1':'sword_3'
    }

    swords.append(
        Actor(
            sword_mapping[player.image],
            center=player.pos
        )
    )

def on_key_down(key):
    if key == keys.RETURN:
        if is_game_over():
            restart_game()

def restart_game():
    global frames_since_hidden
    global monster_hidden_direction
    global player_speed
    global monster_speed
    global sword_speed
    global trees
    global boulders
    global swords
    global player
    global monster
    global grass
    global monster_health
    frames_since_hidden = 0
    monster_hidden_direction = random.randint(-180,180)

    player_speed = 2
    monster_speed = 1
    sword_speed = 10

    trees = []
    boulders = []
    swords = []

    generate()

    player = Actor('link_f0')
    random_position(player)

    monster = Actor('monster_f0')
    random_position(monster)

    grass = Actor('grass')

    monster_health = 20

WIDTH = 1000
HEIGHT = 600

frames_since_hidden = None
monster_hidden_direction = None

player_speed = None
monster_speed = None
sword_speed = None

trees = None
boulders = None
swords = None

player = None
monster = None

grass = None

monster_health = None

restart_game()

pgzrun.go()

# Things to fix and add:
# Better background patterns
# when walking to a new screen, if there is a boulder there, link will not be able to move
# Monster should push boulders out of the way
# player shouldnt be able to make swords after the game is over
# menu
# mode where there are multiple monsters that have to be hit once