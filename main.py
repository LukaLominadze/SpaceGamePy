from application import Application
from game_data import WIN_RES, GAME_RES, TITLE

if __name__ == '__main__':
    app = Application(TITLE, WIN_RES, GAME_RES)
    app.run()
