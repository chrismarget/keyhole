import urwid

class Screen(object):
    def __init__(self, app):
        self.app = app

    def activate(self, loop=None, data=None):
        self.set_screen_name()
        self.set_contents()
        self.set_status()
        self.set_keys()

    def set_screen_name(self):
        pass

    def set_contents(self):
        pass

    def set_status(self):
        pass

    def set_keys(self):
        pass
