#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016  Utkarsh Tiwari
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Contact information:
# Utkarsh Tiwari    iamutkarshtiwari@gmail.com

from gettext import gettext as _

from gi.repository import Gtk
from gi.repository import GObject

from sugar3.graphics import style
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.toolbarbox import ToolbarButton
from sugar3.graphics.toggletoolbutton import ToggleToolButton


class FiddlerMenu(ToolButton):
    '''
    Generates the submenu for the JS-Fiddler and
    attaches it to the Fiddler toolbutton.
    '''
    __gtype_name__ = 'FiddlerMenu'

    __gsignals__ = {
        'go-webconsole': (GObject.SignalFlags.RUN_FIRST, None, ([])),
        'save-file-webconsole': (GObject.SignalFlags.RUN_FIRST, None, ([])),
        'open-file-webconsole': (GObject.SignalFlags.RUN_FIRST, None, ([])),
        'run-webconsole': (GObject.SignalFlags.RUN_FIRST, None, ([])),
        'add-image-webconsole': (GObject.SignalFlags.RUN_FIRST, None, ([])),
    }

    def __init__(self, activity, **kwargs):
        ToolButton.__init__(self, 'js-fiddler', **kwargs)
        self.set_tooltip(_('JS-Fiddler'))
        self.palette_invoker.props.toggle_palette = True
        self.palette_invoker.props.lock_palette = True
        self.props.hide_tooltip_on_click = False
        self._palette = self.get_palette()

        #self.connect('clicked', self._go_webconsole_cb)

        menu_box = PaletteMenuBox()

        save_button = ToolButton('save-as')
        menu_box.append_item(save_button, item_name='Save As')
        save_button.connect('clicked', self._save_file_webconsole_cb)
        save_button.show()

        open_button = ToolButton('open')
        menu_box.append_item(open_button, item_name='Open')
        open_button.connect('clicked', self._open_file_webconsole_cb)
        open_button.show()

        run_button = ToolButton('run')
        menu_box.append_item(run_button, item_name='Run')
        run_button.connect('clicked', self._run_webconsole_cb)
        run_button.show()

        add_image = ToolButton('add-image')
        menu_box.append_item(add_image, item_name='Add Image')
        add_image.connect('clicked', self._add_image_webconsole_cb)
        add_image.show()

        self._palette.set_content(menu_box)
        menu_box.show_all()

    def _go_webconsole_cb(self, button):
        self.emit('go-webconsole')

    def _save_file_webconsole_cb(self, button):
        self.palette.popdown(True)
        self.emit('save-file-webconsole')

    def _open_file_webconsole_cb(self, button):
        self.palette.popdown(True)
        self.emit('open-file-webconsole')

    def _run_webconsole_cb(self, button):
        self.palette.popdown(True)
        self.emit('run-webconsole')

    def _add_image_webconsole_cb(self, button):
        self.palette.popdown(True)
        self.emit('add-image-webconsole')

class PaletteMenuBox(Gtk.HBox):
    def __init__(self):
        Gtk.HBox.__init__(self)

    def append_item(self, item_or_widget, item_name=None):

        item = item_or_widget
        item_name = item_name

        self.vbox = Gtk.VBox()
        self.vbox.pack_start(item, False, False, 0)

        self._item_label = Gtk.Label()
        self._item_label.set_text(_(item_name))
        self.vbox.pack_start(self._item_label, False, False, 0)
        self._item_label.show()

        self.pack_start(self.vbox, False, False, style.DEFAULT_SPACING)
'''
class PaletteMenuItemSeparator(Gtk.EventBox):
    """Contains a HSeparator and has the proper height for the menu."""

    __gtype_name__ = 'FiddlerPaletteMenuItemSeparator'

    def __init__(self):
        Gtk.EventBox.__init__(self)
        separator = Gtk.VSeparator()
        self.add(separator)
        separator.show()
        self.set_size_request(-1, style.DEFAULT_SPACING * 2)
'''