
from engine.holdemengine import HoldemEngine
from ui.console.simple import SimplePokerConsole

ui = SimplePokerConsole()
engine = HoldemEngine(ui.events_handler)
engine.start()