from game import *


def main():
    game = Game()
    game.init_game()
    while 1:
        game.listen_for_events()
        game.update()
        game.display()


if __name__ == "__main__":
    main()
