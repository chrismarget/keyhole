import datetime
import math
import time
from urwid import ExitMainLoop, AttrMap, Columns, Filler, Frame, Text, Padding


def theme_to_palette(theme):
    palette = []
    for name, colors in theme.items():
        palette.append((name, "", "", "", *colors))
    return palette


class Display(object):
    palette = {}
    button_palette =[]
    button_count = 0
    last = 0

    def __init__(self, loop, conf):
        self.loop = loop
        self.conf = conf

        themes = self.conf.get("themes", {})
        for t in themes:
            self.palette[t] = theme_to_palette(themes[t])

        loop.screen.set_terminal_properties(colors=256)

        header = self._init_header()
        footer = self._init_footer()
        self.main_box = Filler(Text(""))
        self.frame = Frame(self.main_box, header, footer)

    def activate(self):
        self.loop.widget = AttrMap(self.frame, "background")

    def unhandled_input(self, key):
        raise ExitMainLoop()

    def init_button_palette(self, key_color_map):
        for theme in self.palette:
            self.palette[theme] = self.palette[theme] + theme_to_palette(key_color_map)

    def _init_header(self):
        self.app_name = Text(self.conf["app_name"], align="right")
        self.screen_name = Text("...")
        header = Columns(
            [
                AttrMap(Padding(self.screen_name, align="left", left=1), "screen_name"),
                AttrMap(self.app_name, "app_name"),
            ]
        )
        return AttrMap(header, "header")

    def _init_footer(self):
        self.clock = Text("")
        self.status = Text("Idle", align="right")
        return AttrMap(
            Columns([AttrMap(self.clock, "clock"), AttrMap(self.status, "status"),]),
            "footer",
        )

    def set_screen_name(self, screen_name):
        self.screen_name.set_text(screen_name)

    def set_status(self, status):
        self.status.set_text(status)

    def update_clock(self, loop, data=None):
        now = datetime.datetime.now()  # tz=self.conf['clock_timezone'])
        self.clock.set_text(now.strftime(self.conf["clock_format"]))

        next_second = math.ceil(time.time())
        loop.set_alarm_at(next_second, self.update_clock)

    def set_body(self, body):
        self.frame.contents["body"] = (body, None)
