#!/usr/bin/env python3
"""
Chain - A 16-bit Adventure Side-Scroller
========================================

Help Chain rescue the lost princess from the evil Cannon!

Run this file to start the game:
    python main.py

Controls:
    - Arrow Keys / WASD: Move
    - Space: Jump (in levels)
    - Z: Attack
    - X: Cast selected spell
    - 1-4: Select spell
    - Enter: Interact / Enter level
    - ESC: Pause / Menu
"""

from game import Game


def main():
    """Entry point for the game"""
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
