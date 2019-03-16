
from ui.eventhandlers.console import ConsoleEventHandler
from ui.inputhandler.console import ConsoleInputHandler

class SimplePokerConsole:
    def __init__(self):
        self.__event_handler_instance = ConsoleEventHandler()
        self.__input_handler_instance = ConsoleInputHandler()

    def get_event_hanlder(self):
        return self.__event_handler_instance.event_handler

    def get_input_handler(self):
        return self.__input_handler_instance.input_handler