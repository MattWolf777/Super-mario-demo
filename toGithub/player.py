import pygame
from support import import_folder
import settings
import time


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        pos,
    ):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.25
        self.player_size = settings.player_size

        # Player Movement
        self.direction = pygame.math.Vector2(0, 0.01)
        self.position = pygame.math.Vector2(pos[0], pos[1])
        self.speed = 5
        self.gravity = 0.6
        self.jump_speed = -18

        # Player Status
        self.status = "idle"
        self.facing_right = True
        self.size = "small"
        self.crouching = False

        # import assets
        self.import_character_asstes()
        self.image = pygame.transform.scale(
            self.forms[self.size]["idle"][self.frame_index], self.player_size
        )
        self.rect = self.image.get_rect(bottomleft=pos)

    def import_character_asstes(self):
        character_path = "../Packages/Textures/player/mario/"
        self.forms = import_folder(character_path)

    def animate(self):
        animation = self.forms[self.size][self.status]

        # loop over the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]

        if self.facing_right:
            self.image = image

        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN] and self.size != "small":
            if not self.crouching:
                self.crouching = True
                self.status = "crouch"
                self.rect = pygame.Rect(
                    self.rect.left,
                    self.rect.top + 60,
                    self.rect.width,
                    self.rect.height - 60,
                )

        elif not keys[pygame.K_DOWN]:
            if self.crouching:
                self.crouching = False
                self.rect = pygame.Rect(
                    self.rect.left,
                    self.rect.top - 60,
                    self.rect.width,
                    self.rect.height + 60,
                )

        if keys[pygame.K_SPACE] and self.direction.y == 0:
            self.jump()

        if keys[pygame.K_1]:
            if self.size == "big":
                self.rect = pygame.Rect(
                    self.rect.left + 15,
                    self.rect.top + 45,
                    self.rect.width - 15,
                    self.rect.height - 45,
                )
                self.size = "small"
                self.jump_speed = -18

        if keys[pygame.K_2]:
            if self.size == "small":
                self.rect = pygame.Rect(
                    self.rect.left - 15,
                    self.rect.top - 45,
                    self.rect.width + 15,
                    self.rect.height + 45,
                )
                self.size = "big"
                self.jump_speed = -20

        if keys[pygame.K_RIGHT]:
            if not self.crouching:
                self.direction.x = 1
            elif self.crouching and self.direction.x > 0:
                self.status = "slide"
                self.direction.x -= 0.02
            self.facing_right = True

        elif keys[pygame.K_LEFT]:
            if not self.crouching:
                self.direction.x = -1
            elif self.crouching and self.direction.x < 0:
                self.status = "slide"
                self.direction.x += 0.02
            self.facing_right = False

        else:
            self.direction.x = 0

    def get_status(self):
        if self.direction.y == 0 or self.direction.y == 0.6:
            if self.direction.x == 0 and not self.crouching:
                self.status = "idle"
                self.animation_speed = 0.08
            elif self.direction.x != 0 and not self.crouching:
                self.status = "run"
                self.animation_speed = 0.25

        else:
            self.animation_speed = 0.25
            if self.direction.y < 0:
                self.status = "jump"
            elif self.direction.y > 0:
                self.status = "fall"
        if self.crouching:
            self.status = "crouch"

        if self.status == "fall" or self.status == "jump":
            self.position.y += self.direction.y
        self.position.x += self.direction.x

    def jump(self):
        self.direction.y = self.jump_speed

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.get_status()
        self.get_input()
        self.animate()
