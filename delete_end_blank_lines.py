# -*- coding: utf-8 -*-
# @author: Ya Kazama <kazamaya.y@gmail.com>
""""""
import sublime
import sublime_plugin


platform = sublime.platform()


if platform == "windows":
    new_line_char = "\r\n"
elif platform == "osx":
    new_line_char = "\r"
else:
    new_line_char = "\n"


def _cursor(view, start=0, end=0, region=True):
    sel = view.sel()
    sel.clear()
    sel.add(sublime.Region(start, end))
    if region:
        return sel[0]
    return sel


class DeleteEndBlankLinesCommand(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        sel_current = view.sel()[0]

        while True:
            size = view.size()
            region_line_end = _cursor(view, size, size)
            fl_region_line_end = view.full_line(region_line_end)

            if size < 1:
                break

            if fl_region_line_end.empty():
                region_line_previous = _cursor(
                    view,
                    fl_region_line_end.a - 1,
                    fl_region_line_end.b - 1
                )
                fl_region_line_previous = view.full_line(region_line_previous)
                offset = fl_region_line_previous.b - fl_region_line_previous.a
                # if view.substr(fl_region_line_previous) == new_line_char:
                if offset <= 1 or fl_region_line_previous.empty():
                    _cursor(view, size, size)
                    view.run_command("move_to", {"to": "bol", "extend": True})
                    view.run_command("add_to_kill_ring", {"forward": False})
                    view.run_command("left_delete")
                else:
                    break
            else:
                _cursor(view, size, size)
                view.run_command("insert", {"characters": new_line_char})
                _size = view.size()
                if _size - size > 1:
                    view.run_command("move_to", {"to": "bol", "extend": True})
                    view.run_command("add_to_kill_ring", {"forward": False})
                    view.run_command("left_delete")
                break

        size = view.size()
        offset = sel_current.b - size
        if offset >= -1:
            view.show(_cursor(view, size, size))
        else:
            view.show(_cursor(view, sel_current.a, sel_current.b))
