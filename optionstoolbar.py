# Copyright (C) 2007, One Laptop Per Child
# Copyright (C) 2009, Tomeu Vizoso
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

from gettext import gettext as _

from gi.repository import Gtk
from gi.repository import GObject

from sugar3.graphics import style
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.toolbarbox import ToolbarButton
from sugar3.graphics.toggletoolbutton import ToggleToolButton

from browser import Browser
from browser import ZOOM_ORIGINAL


class OptionsToolbar(Gtk.Toolbar):
    def __init__(self, activity):
        GObject.GObject.__init__(self)

        self._browser = None

        self._activity = activity

        '''
        self.zoomout = ToolButton('zoom-out')
        self.zoomout.set_tooltip(_('Zoom out'))
        self.zoomout.connect('clicked', self.__zoomout_clicked_cb)
        self.insert(self.zoomout, -1)
        self.zoomout.show()
        '''
        #adding a button for Web Console
        #self._go_webconsole = ToolBarButton('js-fiddler')
        #self._go_webconsole.set_tooltip(_('Open/Run Web Console'))
        # self._go_webconsole.connect('clicked', self._go_webconsole_cb)
        #self.insert(self._go_webconsole, -1)
        #self._go_webconsole.show()

        #self._fiddler_options_toolbar = FiddleToolbar(self._activity)

        #self._options_toolbar_button = ToolbarButton(
        self._fiddler_menu = FiddlerMenu(ToolButton)

        self.insert(self._fiddler_menu, -1)

        self._fiddler_menu.show()



        '''
        self.traybutton = ToggleToolButton('tray-show')
        self.traybutton.set_icon_name('tray-favourite')
        self.traybutton.connect('toggled', self.__tray_toggled_cb)
        self.traybutton.props.sensitive = False
        self.traybutton.props.active = False
        self.insert(self.traybutton, -1)
        self.traybutton.show()
        '''

        #tabbed_view = self._activity.get_canvas()

        #if tabbed_view.get_n_pages():
        #    self._connect_to_browser(tabbed_view.props.current_browser)

        #tabbed_view.connect_after('switch-page', self.__switch_page_cb)

    '''    

    def __switch_page_cb(self, tabbed_view, page, page_num):
        self._connect_to_browser(tabbed_view.props.current_browser)

    def _connect_to_browser(self, browser):
        self._browser = browser
        self._update_zoom_buttons()

    def _update_zoom_buttons(self):
        is_webkit_browser = isinstance(self._browser, Browser)
        self.zoomin.set_sensitive(is_webkit_browser)
        self.zoomout.set_sensitive(is_webkit_browser)
        self.zoom_original.set_sensitive(is_webkit_browser)

    def __zoom_original_clicked_cb(self, button):
        tabbed_view = self._activity.get_canvas()
        tabbed_view.props.current_browser.set_zoom_level(ZOOM_ORIGINAL)

    def __zoomin_clicked_cb(self, button):
        tabbed_view = self._activity.get_canvas()
        tabbed_view.props.current_browser.zoom_in()

    def __zoomout_clicked_cb(self, button):
        tabbed_view = self._activity.get_canvas()
        tabbed_view.props.current_browser.zoom_out()

    def __fullscreen_clicked_cb(self, button):
        self._activity.fullscreen()
    '''    

    def __tray_toggled_cb(self, button):
        if button.props.active:
            self._activity.tray.show()
        else:
            self._activity.tray.hide()
        self.update_traybutton_tooltip()
    '''    

    def update_traybutton_tooltip(self):
        if not self.traybutton.props.active:
            self.traybutton.set_tooltip(_('Show Tray'))
        else:
            self.traybutton.set_tooltip(_('Hide Tray'))
    '''


class FiddlerMenu(ToolButton):

    def __init__(self, activity, **kwargs):
        ToolButton.__init__(self, 'js-fiddler', **kwargs)
        self.set_tooltip(_('JS-Fiddler'))
        self.palette_invoker.props.toggle_palette = True
        self.palette_invoker.props.lock_palette = True
        self.props.hide_tooltip_on_click = False
        self._palette = self.get_palette()

        menu_box = PaletteMenuBox()
        #sw = Gtk.ScrolledWindow()
        #sw.set_size_request(int(Gdk.Screen.width() / 2),
        #                    2 * style.GRID_CELL_SIZE)
        #sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        #self._text_view = Gtk.TextView()
        #self._text_view.set_left_margin(style.DEFAULT_PADDING)
        #self._text_view.set_right_margin(style.DEFAULT_PADDING)
        #self._text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        #text_buffer = Gtk.TextBuffer()
        #if 'description' in activity.metadata:
        #    text_buffer.set_text(activity.metadata['description'])
        #self._text_view.set_buffer(text_buffer)
        #self._text_view.connect('focus-out-event',
        #                        self.__description_changed_cb, activity)
        #sw.add(self._text_view)
        run_button = ToolButton('run')
        #run_button.set_tooltip(_('Run'))
        menu_box.append_item(run_button, item_name='Run', vertical_padding=0)
        run_button.show()

        save_button = ToolButton('save-as')
        #save_button.set_tooltip(_('Save As'))
        menu_box.append_item(save_button, item_name='Save As', vertical_padding=0)
        save_button.show()

        add_image = ToolButton('add-image')
        #add_image.set_tooltip(_('Add image'))
        menu_box.append_item(add_image, item_name='Add Image', vertical_padding=0)
        add_image.show()

        open_button = ToolButton('open')
        #open_button.set_tooltip(_('Open'))
        menu_box.append_item(open_button, item_name='Open', vertical_padding=0)
        open_button.show()


        self._palette.set_content(menu_box)
        menu_box.show_all()
        
    

class PaletteMenuBox(Gtk.HBox):
    def __init__(self):
        Gtk.HBox.__init__(self)

    def append_item(self, item_or_widget, item_name, horizontal_padding=None,
                    vertical_padding=None):

        #if (isinstance(item_or_widget) or
        #        isinstance(item_or_widget, PaletteMenuItemSeparator)):
        item = item_or_widget
        item_name = item_name
        #else:
        #    item = self._wrap_widget(item_or_widget, horizontal_padding,
        #                             vertical_padding)

        self.vbox = Gtk.VBox()
        self.vbox.pack_start(item, False, False, 0)

        self._item_label = Gtk.Label()
        self._item_label.set_text(_(item_name))
        self.vbox.pack_start(self._item_label, False, False, 0)
        self._item_label.show()

        self.pack_start(self.vbox, False, False, style.DEFAULT_SPACING)

    def _wrap_widget(self, widget, horizontal_padding, vertical_padding):
        vbox = Gtk.HBox()
        vbox.show()

        if horizontal_padding is None:
            horizontal_padding = style.DEFAULT_SPACING

        if vertical_padding is None:
            vertical_padding = style.DEFAULT_SPACING

        hbox = Gtk.HBox()
        vbox.pack_start(hbox, True, True, vertical_padding)
        hbox.show()

        hbox.pack_start(widget, True, True, horizontal_padding)
        return vbox


class PaletteMenuItemSeparator(Gtk.EventBox):
    """Contains a HSeparator and has the proper height for the menu."""

    __gtype_name__ = 'FiddlerPaletteMenuItemSeparator'

    def __init__(self):
        Gtk.EventBox.__init__(self)
        separator = Gtk.VSeparator()
        self.add(separator)
        separator.show()
        self.set_size_request(-1, style.DEFAULT_SPACING * 2)
