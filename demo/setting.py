level_map = [
    "                                                                                                                                                                                                                            ",
    "                                                                                                                                                                                                                             ",
    "          M                                                                                                                                                                                                                 ",
    "                                                                                                                                                                                                                            ",
    "                        ?                                                         BBBBBBBB   BBB?                ?            BBB    B??B                                                           EE                      ",
    "                                                                                                                                                                                                   EEE                      ",
    "                                                                                                                                                                                                  EEEE                      ",
    "                                                                                                                                                                                                 EEEEE             CCC      ",
    "                 ?    B?B?B                       PP       PP                  B?B              B      B      ?  ?  ?      B          BB       E  E           EE  E                             EEEEEE             CCC      ",
    "                                          PP      PP       PP                                                                                 EE  EE         EEE  EE           BB?B            EEEEEEE            CCCCC     ",
    "                               PP         PP      PP       PP                                                                                EEE  EEE       EEEE  EEE     PP               PP EEEEEEEE            CCCCC     ",
    "                               PP         PP      PP       PP                                                                               EEEE  EEEE     EEEEE  EEEE    PP               PPEEEEEEEEE        E   CCCCC     ",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
]

tile_size = 64
screen_width = 1280
player_size = (56, 70)
screen_height = tile_size * len(level_map)
player_state = "big"


#original main file:

import pygame, sys
from setting import *
from tiles import Tile
from level import Level

# Pygame Setup
pygame.init()
from setting import *


screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill("black")
    level.run()

    pygame.display.update()
    clock.tick(60)