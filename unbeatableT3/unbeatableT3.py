# Version checking
import kivy
kivy.require("1.1.1")

# Core Application
from kivy.app import App

# Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.core.window import Window

# Event
from kivy.clock import Clock

# Properties
from kivy.properties import ObjectProperty, AliasProperty

# Standard libraries
import time, math

# Local Module
from .game_engine import (board, HUMAN, COMP, minimax, wins,
                          empty_cells, reset_board)

board_state = board


class StartScreen(Screen):

    def on_press(self, *args):
        self.manager.current = "main"

        # Calling root widget
        root_widget = main_app.get_running_app().root

        # Scheduling game event
        Clock.schedule_interval(root_widget.game_loop, 0.5)


class MainScreen(Screen):

    game_board = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def on_press(self, *args):
        self.manager.current = "start"
        reset_board(board_state)

        # Calling root widget
        root_widget = main_app.get_running_app().root

        # First turn is Human
        root_widget.current_turn = HUMAN
        root_widget.turn_label.text = "Human Turn"

        # Render the board at the very beginning of the game
        root_widget.render(board_state)


class GameBoard(GridLayout):

    def __init__(self, **kwargs):
        super(GameBoard, self).__init__(**kwargs)

        self.cols = 3
        self.move = True

        config = {"text":"-_-", "font_size":40, }
        self.btn_dict = {
            x : Button(**config) for x in range(1,10)}

        for widget in self.btn_dict.values():
            self.add_widget(widget)
            widget.bind(on_release=self.callback)

    def callback(self, button):
        root_widget = main_app.get_running_app().root
        root_widget.human_turn(board_state, button)


class GameResult(Popup):
    pass


class RootScreen(ScreenManager):

    def __init__(self, **kwargs):
        super(RootScreen, self).__init__(**kwargs)

        self.turn_label = self.ids["turn_label"]
        self.game_board = self.ids["game_board"]

        self.btn_dict = self.game_board.btn_dict
        self.current_turn = HUMAN

    def game_loop(self, *args):
        if not wins(board_state, HUMAN) and not wins(board_state, COMP):
            if self.current_turn == HUMAN:
                pass

            elif len(empty_cells(board_state)) == 0:
                self.end_game()

            else:
                self.ai_turn(board_state)

        else:
            self.end_game()

    def end_game(self):
        Clock.unschedule(self.game_loop)

        self.turn_label.text = "Game Over"
        for button in self.btn_dict.values():
            button.disabled = 1

        human_win = GameResult(title="Human wins",
                               content=Label(text="You are insane !"))
        ai_win = GameResult(title="A.I wins",
                            content=Label(text="Now, I can take over the world !"))
        draw = GameResult(title="Tie",
                          content=Label(text="It's a tie, nothing happens"))

        if wins(board_state, HUMAN):
            human_win.open()
        elif wins(board_state, COMP):
            ai_win.open()
        else:
            draw.open()

    def change_turn(self, player):
        if player == HUMAN:
            self.turn_label.text = "Human Turn"
            self.current_turn = HUMAN
        else:
            self.current_turn = COMP

    def test(self, *args):
        print("rakka", args)

    def human_turn(self, state, button):
        moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2], }

        key = self.get_key(button)
        x, y = moves[key]
        board_state[x][y] = 1

        self.render(state)

        # Change the current turn to Computer
        self.turn_label.text = "A.I Turn"
        self.change_turn(COMP)

    def ai_turn(self, state):
        depth = len(empty_cells(state))
        row, col, score = minimax(state, depth, COMP)
        state[row][col] = COMP

        self.render(state)

        # Change the current turn to Human
        self.change_turn(HUMAN)

    def get_key(self, value):
        for key, val in self.btn_dict.items():
            if val == value:
                return key

    def render(self, state):
        legend = {0: "-_-", 1: "X", -1: "O"}
        flatten = [item for sublist in state for item in sublist]

        for button, symbol in zip(self.btn_dict.values(), flatten):
            button.text = legend[symbol]
            if button.text in ["X", "O"]:
                button.disabled = 1
            else:
                button.disabled = 0

    def wait(self, dt):
        """Do nothing"""
        return None


class UnbeatableT3App(App):

    def build(self):
        sm = RootScreen(transition=FadeTransition())
        Window.size = 360, 480
        return sm


main_app = UnbeatableT3App()


if __name__ == '__main__':
    UnbeatableT3App().run()