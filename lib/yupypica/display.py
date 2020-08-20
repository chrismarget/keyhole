import asyncio
import math
import random
import datetime
import time
import urwid
import weakref

from .screen_welcome import Welcome
from .screen_lines import Lines


class Display(object):
    palette = []
    button_count = 0
    last = 0

    def __init__(self, app):
        self.app = app

        header = self._init_header()
        footer = self._init_footer()
        self.main_box = urwid.Filler(Welcome())
        self.frame = urwid.AttrMap(urwid.Frame(self.main_box, header, footer), 'background')

        self.main_loop = urwid.MainLoop(
            widget=self.frame,
            event_loop=urwid.AsyncioEventLoop(loop=self.app.asyncio_loop),
            unhandled_input=self.unhandled_input,
        )

    def unhandled_input(self, key):
        raise urwid.ExitMainLoop()

    def add_button(self, button):
        self.app.palette.append((self.button_count, "", "", "", "black", button.color))
        self.button_count += 1

    def _init_header(self):
        self.app_name = urwid.Text(self.app.name, align='center')
        self.screen_name = urwid.Text("initial screen_name", align='right')
        header = urwid.Columns([
            (len(self.app.name)+4, urwid.AttrMap(self.app_name, 'app_name')),   # (length, widget)
            urwid.AttrMap(self.screen_name, 'screen_name'),                     # just widget
        ])
        return urwid.AttrMap(header, 'header')

    def _init_footer(self):
        self.clock = urwid.Text("")
        self.status = urwid.Text("Idle")
        return urwid.AttrMap(urwid.Columns([
            urwid.AttrMap(self.clock, 'clock'),
            urwid.AttrMap(self.status, 'status'),
            ]), 'footer')

    def logo(self):
        return ["                         o          ",
                ",   ..   .,---.,   .,---..,---.,---.",
                "|   ||   ||   ||   ||   |||    ,---|",
                "`---|`---'|---'`---||---'``---'`---^",
                "`---'     |    `---'|               ",
                ]


    def set_screen_name(self, screen_name):
        self.screen_name.set_text(screen_name)

    def update_clock(self, loop=None, data=None):
        now = datetime.datetime.now(tz=self.app.tz)
        self.clock.set_text(now.strftime(self.app.conf['clock_format']))

        next_second = math.ceil(time.time())
        self.main_loop.set_alarm_at(next_second, self.update_clock)

    def populate_frame(self, loop=None, data=None):
        self.main_box.set_body(
                urwid.AttrMap(
                    urwid.Pile([
                        urwid.Text("                              o            ", align='center'),
                        urwid.Text(",   . .   . ,---. ,   . ,---. . ,---. ,---.", align='center'),
                        urwid.Text("|   | |   | |   | |   | |   | | |     ,---|", align='center'),
                        urwid.Text("`---| `---' |---' `---| |---' ` `---' `---^", align='center'),
                        urwid.Text("`---'       |     `---' |                  ", align='center'),
                        urwid.Text("", align='center'),
                        urwid.Text("Stand-alone Certificate Authority", align='center'),
                        urwid.Text("v 1.0.7", align='center'),
                    ]),
                'logo')
                #Lines(count=self.button_count, selected=self.last % self.button_count)
        )
        self.last += 1

    def button_event(self, loop=None, data=None):
        self.populate_frame(loop=loop, data=data)

    def start(self):
        self.main_loop.screen.set_terminal_properties(colors=88)
        self.main_loop.screen.register_palette(self.app.conf['palette'])
        self.update_clock()
        self.main_loop.set_alarm_in(2, self.populate_frame)
        self.main_loop.run()
