import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_width, screen_height
from tiles import Tile, StaticTile, Background, AnimatedTile
from enemies import Enemy
from player import Player


class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.tile_animation_speed = 0.2

        # animated
        animated_layout = import_csv_layout(level_data["animated"])
        self.animated_sprites = self.create_tile_group(animated_layout, "animated")

        # player
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Terrain setup
        terrain_layout = import_csv_layout(level_data["base"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "base")

        # ENEMIES

        # goombas
        goomba_layout = import_csv_layout(level_data["enemies"])
        self.goomba_sprites = self.create_tile_group(goomba_layout, "enemies")

        # constrains
        constrains_layout = import_csv_layout(level_data["constrains"])
        self.constrains_sprites = self.create_tile_group(
            constrains_layout, "constrains"
        )

        # background_setup
        background_layout = import_csv_layout(level_data["background"])
        self.background_sprites = self.create_tile_group(
            background_layout, "background"
        )

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        self.path = "../Packages/Textures/map/"
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    # base-blocks
                    if type == "base":
                        terrain_tile_list = import_cut_graphics(
                            "../Packages/Textures/map/blocks/static/super_mario_bros__tile_revamp_by_malice936_d5ik1aw_scaled_4x_pngcrushed (1).png"
                        )
                        print(val)
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)
                        sprite_group.add(sprite)

                    # Enemies

                    # goombas
                    if type == "enemies":
                        sprite = Enemy(
                            tile_size,
                            x,
                            y,
                            1,
                            "../Packages/Textures/map/enemies/enemies.png",
                        )
                        sprite_group.add(sprite)

                    if type == "animated":
                        sprite = AnimatedTile(
                            tile_size,
                            x,
                            y,
                            1,
                            "../Packages/Textures/map/blocks/animated/question-block.png",
                        )
                        sprite_group.add(sprite)

                    # constrain
                    if type == "constrains":
                        sprite = Tile(tile_size, x, y)
                        sprite_group.add(sprite)

                    # background-assets
                    if type == "background":
                        if val == "0":
                            sprite = Background(
                                "../Packages/Textures/map/decor/bush.png",
                                tile_size,
                                x,
                                y,
                            )
                            sprite_group.add(sprite)
                        elif val == "1":
                            sprite = Background(
                                "../Packages/Textures/map/decor/cloud.png",
                                tile_size,
                                x,
                                y,
                            )
                            sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):

                x = col_index * tile_size
                y = row_index * tile_size
                if val == "1":
                    sprite = Player((x, y))
                    self.player.add(sprite)
                if val == "0":
                    sprite = Tile(tile_size, x, y)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.goomba_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constrains_sprites, False):
                enemy.reverse()

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
        collidable_sprites = (
            self.terrain_sprites.sprites() + self.animated_sprites.sprites()
        )

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x > 0:
                    player.rect.right = sprite.rect.left

                elif player.direction.x < 0:
                    player.rect.left = sprite.rect.right

    def vertical_movement_collision(self):
        player = self.player.sprite
        self.standing = True
        player.apply_gravity()
        collidable_sprites = (
            self.terrain_sprites.sprites() + self.animated_sprites.sprites()
        )

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0

                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 1

    def run(self):

        # background-blocks
        self.background_sprites.update(self.world_shift)
        self.background_sprites.draw(self.display_surface)

        # terrain-blocks
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # animated-blocks
        self.animated_sprites.update(self.world_shift)
        self.animated_sprites.draw(self.display_surface)

        # enemies
        self.goomba_sprites.update(self.world_shift)
        self.constrains_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.goomba_sprites.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
