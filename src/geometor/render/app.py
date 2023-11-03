"""
run the main app
"""
from .render import Render


def run() -> None:
    reply = Render().run()
    print(reply)
