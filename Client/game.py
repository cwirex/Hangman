import random
import sys
from PyQt5 import QtWidgets
from Server.dbase import Base, Session, engine
from Client.windows.allWindows import Windows
from Client.round import Round
from Server.player import Player
from Server.score import Score
from Server.word import Word


class Game:
    """
    Class representing a game. Holds information about the players, categories, words, scores...
    """
    def __init__(self):
        """
        Initialize object of a class Game with defaults.

        """
        self.app = QtWidgets.QApplication(sys.argv)
        self.game_id = 1
        self.players = []
        self.scores = {}  # {nickname: score}
        self.words = []
        self.categories = []
        self.online = False
        self.session = None
        self.round = Round(self)
        self.rounds_in_game = 2
        self.windows = Windows(self)

    def run(self):
        """
        Run game and show login window.

        """
        self.windows.show_formNickname()
        sys.exit(self.app.exec_())

    def start_game(self):
        """
        Prepare game to start: chooses category, word and start new round.

        """
        cat = self.round.category
        word = self.get_random_word()
        self.round = Round(self, cat, word)
        self.windows.mainWindow.timer_start()
        self.windows.mainWindow.update()

    def game_over(self):
        """
        Stop game and show scores

        """
        self.windows.mainWindow.timer_stop()
        self.windows.formScores.update()
        self.windows.show_formScores()

    def get_current_nickname(self):
        """Returns nickname of current player

        :return: string
        """
        return self.round.current_player.nickname

    def player_add(self, nickname, email, avatar, gender):
        """Create a new player from given parameters and add it to the game (and database)

        :param nickname: string representing the player
        :param email: string
        :param avatar: integer
        :param gender: boolean
        """
        if nickname not in [p.nickname for p in self.players]:
            player = Player(nickname, email, avatar, gender)
            self.players.append(player)
            self.scores[nickname] = 0
            if self.online:
                try:
                    if nickname not in [p.nickname for p in self.session.query(Player).all()]:
                        self.session.add(player)
                        self.session.commit()
                except:
                    print("Registering new player to the db failed.")
        self.windows.mainWindow.update_players()

    def player_remove(self, name):
        """
        Remove player from the game

        :param name: string representing the player
        """
        for i in range(len(self.players)):
            if self.players[i].nickname == name:
                self.players.remove(i)
                break
        self.windows.mainWindow.update_players()

    def player_remove_all(self):
        """
        Remove all players from the game
        """
        self.players = []
        self.scores = {}
        self.windows.mainWindow.update_players()

    def playerExists(self, nick):
        """
        Returns True if the player exists

        :param nick: string representing the player
        :return: boolean
        """
        players = self.players
        if self.online:
            try:
                players = self.session.query(Player).all()
            except:
                print("Query from db failed.")
        for p in players:
            if p.nickname == nick:
                return True
        return False

    def playerLogin(self, nick):
        """
        Login player with given nick by fetching data from db

        :param nick: string representing the player
        """
        players = self.players
        if self.online:
            try:
                players = self.session.query(Player).all()
            except:
                print("Query from db failed.")
        for p in players:
            if p.nickname == nick:
                self.player_add(p.nickname, p.email, p.avatar, p.gender)

    def set_category(self, name):
        """
        Change current category to given category name

        :param name: string representing the category
        """
        self.round.category = name
        self.windows.mainWindow.update_category()
        self.update_words()

    def update_words(self):  # Todo add Offline mode, pobierz plik json z bazy słów
        """
        Update list of words
        """
        if self.online:
            self.words = []
            cat = self.round.category
            words = self.session.query(Word).all()
            for w in words:
                if w.category == cat:
                    self.words.append(w.word)

    def set_game_id(self, id):
        """
        Set the game id and update mainWindow

        :param id: integer
        """
        self.game_id = id
        self.windows.mainWindow.update_game_id()

    def set_online(self):
        """
        Set game to online mode
        """
        self.online = True
        try:
            Base.metadata.create_all(engine)
            self.session = Session()
            self.update_categories()
            self.set_category(self.categories[0])
            self.set_game_id(self.get_game_id())
        except:
            print('game.set_online failed')
            self.online = False

    def update_categories(self):  # Todo if !online
        """
        Update list of categories
        """
        words = self.session.query(Word).all()
        temp = []
        [temp.append(w.category) for w in words if w.category not in temp]  # uniq(categories)
        self.categories = temp
        self.categories.sort()
        self.windows.mainWindow.update_categories()

    def get_game_id(self):
        """
        Finds available game id in database

        :return: integer representing game id
        """
        scores = self.session.query(Score).all()
        return 1 + max([s.game_id for s in scores])

    def get_random_word(self):
        """
        Looks for a new word in list of words

        :return: string representing the random word
        """
        words = self.words.copy()
        if self.round.word in words:
            words.remove(self.round.word)
        return random.choice(words)
