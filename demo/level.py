import pygame
from tiles import Tile
from setting import tile_size, screen_width
from player import Player


class Level:
    # Level Setup+

    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.count = 0
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):

                x = col_index * tile_size
                y = row_index * tile_size

                if cell != "M" and cell != " ":
                    if cell == "X":
                        tile_color = "brown"
                    elif cell == "?":
                        tile_color = "yellow"
                    elif cell == "P":
                        tile_color = "green"
                    elif cell == "B":
                        tile_color = "brown"
                    elif cell == "E":
                        tile_color = "grey"

                    tile = Tile((x, y), tile_size, tile_color)
                    self.tiles.add(tile)

                elif cell == "M":
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width * 0.6 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left

                elif player.direction.x < 0:
                    player.rect.left = sprite.rect.right

    def vertical_movement_collision(self):
        player = self.player.sprite
        self.standing = True
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0

                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 1

    def run(self):

        # Level Tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        # Player
        self.player.update()
        self.player.draw(self.display_surface)
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
