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
        old_sel = view.sel()[0]
        while True:
            size = view.size()
            cursor_region = move_cursor(view, size, size)[0]
            content = view.full_line(cursor_region)

            if size == 0:
                break
            if re.match(RE, view.substr(content)):
                previous_cursor_region = move_cursor(
                    view, cursor_region.a - 1, cursor_region.b - 1
                )[0]
                pre_content = view.substr(
                    view.full_line(previous_cursor_region)
                )

                if re.match(RE, pre_content):
                    view.run_command("right_delete")
                else:
                    break
        t_sel = move_cursor(view, old_sel.a, old_sel.b)
        view.show(t_sel)
