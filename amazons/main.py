import pygame
from ui.GameGUI import GameGUI


def main():
    # Basic configuration
    pygame.init()

    width = 1_000
    height = 1_000
    tile_size = 100
    gameGUI = GameGUI(width, height, tile_size)

    gameGUI.run()


if __name__ == "__main__":
    main()
