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
from fiddlermenu import FiddlerMenu


class OptionsToolbar(Gtk.Toolbar):
    '''
    This class expands the Browse toolbar and provides for
    the extra space needed to add new Toolbuttons in future.
    '''
    def __init__(self, activity):
        GObject.GObject.__init__(self)

        self._browser = None

        self._activity = activity

        # Adds the fiddler toolbutton
        self._fiddler_menu = FiddlerMenu(ToolButton)
        self.insert(self._fiddler_menu, -1)
        self._fiddler_menu.show()

    def __tray_toggled_cb(self, button):
        if button.props.active:
            self._activity.tray.show()
        else:
            self._activity.tray.hide()
        self.update_traybutton_tooltip()

