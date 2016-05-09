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

from browser import Browser
from browser import ZOOM_ORIGINAL
import json


class OptionsToolbar(Gtk.Toolbar):
    '''
    This class expands the Browse toolbar and provides for
    the extra space needed to add new Toolbuttons in future.
    '''
    __gsignals__ = {
        'save-file-webconsole': (GObject.SignalFlags.RUN_FIRST, None, ([])),
        'open-file-webconsole': (GObject.SignalFlags.RUN_FIRST, None, ([])),
        'run-webconsole': (GObject.SignalFlags.RUN_FIRST, None, ([])),
        'add-image-webconsole': (GObject.SignalFlags.RUN_FIRST, None, ([])),
    }

    def __init__(self, activity):
        GObject.GObject.__init__(self)

        self._browser = None

        self._activity = activity

        '''
        # Adds the fiddler toolbutton
        self._fiddler_menu = FiddlerMenu(ToolButton)
        self.insert(self._fiddler_menu, -1)
        self._fiddler_menu.show()
        '''

        run_button = ToolButton('run')
        run_button.set_tooltip(_('Run'))
        self.insert(run_button, -1)
        run_button.connect('clicked', self._run_webconsole_cb)
        run_button.show()

        open_button = ToolButton('open')
        open_button.set_tooltip(_('Open'))
        self.insert(open_button, -1)
        open_button.connect('clicked', self._open_file_webconsole_cb)
        open_button.show()

        save_button = ToolButton('save-as')
        save_button.set_tooltip(_('Save'))
        self.insert(save_button, -1)
        save_button.connect('clicked', self._save_file_webconsole_cb)
        save_button.show()

        add_image = ToolButton('add-image')
        add_image.set_tooltip(_('Add image'))
        self.insert(add_image, -1)
        add_image.connect('clicked', self._add_image_webconsole_cb)
        add_image.show()

        # Adds view-page-source toolbutton
        self._view_source = ToolButton('view-source-files')
        self._view_source.set_tooltip(_('View page source'))
        self._view_source.connect('clicked', self._view_page_source_cb)
        self.insert(self._view_source, -1)
        self._view_source.show()


    def _view_page_source_cb(self, button):
        browser = self._activity._tabbed_view.props.current_browser

        text = browser.get_main_frame().get_data_source().get_data()

        text = str(text.str)
        browser = self._activity._tabbed_view.add_tab(next_to_current=True)
        browser.load_string(text, "text/plain", "UTF-8", '/')

    def _save_file_webconsole_cb(self, button):
        self.emit('save-file-webconsole')

    def _open_file_webconsole_cb(self, button):
        self.emit('open-file-webconsole')

    def _run_webconsole_cb(self, button):
        self.emit('run-webconsole')

    def _add_image_webconsole_cb(self, button):
        self.emit('add-image-webconsole')

    def __tray_toggled_cb(self, button):
        if button.props.active:
            self._activity.tray.show()
        else:
            self._activity.tray.hide()
        self.update_traybutton_tooltip()


