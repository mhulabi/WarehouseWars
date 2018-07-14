import sys, pygame, random
from ww import *
pygame.init()
pygame.mixer.music.load("./music/back music.mp3")
pygame.mixer.music.play(-1)
pygame.image.load("./images/back2.png")
pygame.image.load("./images/front.png")
pygame.image.load("./images/surrender.png")
pygame.image.load("./images/fight.png")
ww=Stage(20, 20, 24)
ww.set_player(KeyboardPlayer("icons/face-cool-24.png", ww))

# This loop randomly generates 100 boxes in the game.
num_boxes=0
while num_boxes<100:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(Box("icons/emblem-package-2-24.png", ww, x, y))
        num_boxes+=1

# This loop randomly generates 10 sticky boxes in the game.
numm_boxes=0
while numm_boxes<10:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(StickyBox("icons/realstickybox2.png", ww, x, y))
        numm_boxes+=1

# This loop randomly generates 4 walls in the game.
walls=0
while walls<4:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(Wall("icons/wall.jpg", ww, x, y))
        walls+=1

# This loop randomly generates 4 regular monsters in the game.
devil=0
while devil<4:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(DevilMonster("icons/face-devil-grin-24.png", ww, x, y))
        devil+=1

# This loop randomly generates 2 regular monsters that look different than the first regular monsters in the game.
devil2=0
while devil2<2:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(DevilMonster2("icons/face-devil-sad.png", ww, x, y))
        devil2+=1

# This loop randomly generates 2 suicide monsters in the game.
suidevil=0
while suidevil<2:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(SuicideMonster("icons/face-uneasy.png", ww, x, y))
        suidevil+=1

#This loop randomly generates 2 explosion monsters in the game.
expodevil=0
while expodevil<2:
    x=random.randrange(ww.get_width())
    y=random.randrange(ww.get_height())
    if ww.get_actor(x,y) is None:
        ww.add_actor(ExplosionMonster("icons/face-devilish.png", ww, x, y))
        expodevil+=1


'''This loop checks all events in the game such as player movement and whether or not someone quits the game and
the transition from the start menu to the game.'''
if ww.start_menu():
    ww.game_loop()


