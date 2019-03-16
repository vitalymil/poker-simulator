
from engine.holdemengine import HoldemEngine
from ui.console import SimplePokerConsole

ui = SimplePokerConsole()
engine = HoldemEngine(ui.get_event_hanlder(), ui.get_input_handler())
engine.start()