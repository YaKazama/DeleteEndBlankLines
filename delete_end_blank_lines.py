# -*- coding: utf-8 -*-
# @author: Ya Kazama <kazamaya.y@gmail.com>
""""""
import re
import sublime
import sublime_plugin

RE = r"^$"


def move_cursor(view, start=0, end=0):
    sel = view.sel()
    sel.clear()
    sel.add(sublime.Region(start, end))
    return sel


class DeleteEndBlankLinesCommand(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        while True:
            size = view.size()
            cursor_region = move_cursor(view, size, size)[0]
            content = view.full_line(cursor_region)

            if re.match(RE, view.substr(content)):
                _tuple = tuple(cursor_region)
                previous_cursor_region = move_cursor(
                    view, _tuple[0] - 1, _tuple[0] - 1
                )[0]
                pre_content = view.substr(
                    view.full_line(previous_cursor_region)
                )

                if re.match(RE, pre_content):
                    view.run_command("left_delete")
                else:
                    break
        move_cursor(view, size, size)
