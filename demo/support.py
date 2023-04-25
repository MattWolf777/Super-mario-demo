import os
import pygame


def import_folder(path):
    states = {}
    root_folder = path

    for forms in os.listdir(root_folder):
        full_path = root_folder + forms + "/"
        states[forms] = {}

        for moves in os.listdir(full_path):
            full_path = root_folder + forms + "/" + moves + "/"
            states[forms][moves] = []

            for _, __, img_files in os.walk(full_path):
                for img in img_files:
                    full_path = root_folder + forms + "/" + moves + "/" + img
                    image_surface = pygame.image.load(full_path)
                    states[forms][moves].append(image_surface)

    return states
