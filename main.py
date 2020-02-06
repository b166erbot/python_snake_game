from contextlib import suppress

from src.snake_game import main

if __name__ == '__main__':
    with suppress(KeyboardInterrupt, EOFError):
        main()
