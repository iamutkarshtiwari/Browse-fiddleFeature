# Copyright (C) 2015, Richa Sehgal
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

from filepicker import FilePicker
from gettext import gettext as _
import os
import re
import tempfile
import shutil
import zipfile

from gi.repository import Gtk
from gi.repository import WebKit
from gi.repository import GObject
from gi.repository import GLib

from sugar3.graphics import style
from sugar3.graphics.alert import ErrorAlert, Alert
from sugar3.graphics.icon import Icon
from sugar3.activity import activity
from sugar3.datastore import datastore


class WebConsole():
    def __init__(self, act):
        self._activity = act

        src_path = os.path.join(activity.get_bundle_path(),
                                "data/web-console.html")
        self._src_uri = "file://" + src_path

        self.parent_dir = os.path.join(act.get_activity_root(),
                                  "Web_Console_Files")
        if not os.path.exists(self.parent_dir):
            os.makedirs(self.parent_dir)

        self._storage_dir = os.path.join(self.parent_dir, "default")
        try:
            os.makedirs(self._storage_dir)
        except OSError as e:
            pass
        self._index_html_path = os.path.join(self._storage_dir, "index.html")

        self._load_status_changed_hid = None
        self._file_path = None



    def __del__(self):
        shutil.rmtree(self._storage_dir)

    def _get_file_text(self, pattern):
        browser = self._activity._tabbed_view.props.current_browser
        frame = browser.get_main_frame()

        original_title = frame.get_title()
        if original_title is None:
            original_title = ""
        text_script = \
            "var saveTextBtn = document.getElementById('internal-use-trigger-" + pattern + "-text');" \
            "saveTextBtn.click();" \
            "var savedTextDiv = document.querySelector('#internal-use-" + pattern + "-text');" \
            "var text = savedTextDiv.value; " \
            "document.title = text;"
        browser.execute_script(text_script)
        file_text = frame.get_title()

        reset_title_script = "document.title = '" + original_title + "';"
        browser.execute_script(reset_title_script)

        return file_text

    def _add_to_journal(self, title, file_path):
        jobject = datastore.create()

        jobject.metadata['title'] = title + '.html'
        jobject.metadata['description'] = "Saved from web console"

        jobject.metadata['mime_type'] = "application/zip"
        jobject.file_path = file_path
        datastore.write(jobject)

    def _load_status_changed_cb(self, widget, param):
        status = widget.get_load_status()
        if status == WebKit.LoadStatus.FINISHED:
            self._open_file_path(self._file_path)
            browser = self._activity._tabbed_view.props.current_browser
            browser.disconnect(self._load_status_changed_hid)
            self._file_path = None

    def _open_with_source(self, file_path):
        browser = self._activity._tabbed_view.props.current_browser
        browser.load_uri(self._src_uri);
        browser.grab_focus();
        self._file_path = file_path

        self._load_status_changed_hid = browser.connect(
            'notify::load-status', self._load_status_changed_cb)

    def _open_empty(self):
        browser = self._activity._tabbed_view.props.current_browser
        browser.load_uri(self._src_uri);
        browser.grab_focus();

    def open_new_tab(self):
        browser = self._activity._tabbed_view.props.current_browser
        browser.get_source(self._open_with_source, self._open_empty)

    def run(self):
        browser = self._activity._tabbed_view.props.current_browser
        if browser.get_uri() != self._src_uri:
            self.open_new_tab()
            return
        file_text = self._get_file_text('run')
        with open(self._index_html_path, 'w') as f:
            f.write(file_text + '\n')

        text_script = \
            "var iframe = document.getElementById('iframe');" \
            "iframe.src = '" + self._index_html_path + "';"
        browser.execute_script(text_script)

    def save_file(self):
        browser = self._activity._tabbed_view.props.current_browser
        if browser.get_uri() != self._src_uri:
            self._activity._alert("It looks like the Web Console is not open." +
                                  "You can only Save a file from Web Console")
            return
        file_text = self._get_file_text('save')
        # Grabs the name between <title> tags
        output  = re.compile('<title>(.*?)</title>', re.DOTALL |  re.IGNORECASE).findall(file_text)
        if len(output) != 0:
            # Assigns the path to the directories
            folder_name = output[0].strip().replace (" ", "_")
            self._get_path(folder_name)
            # Creates the directory to save the files
            os.makedirs(self._storage_dir)
            self._do_save()

        else:
            self._save_alert = SaveAlert()
            self._save_alert.props.title = _('Save As')
            self._save_alert.props.msg = _('Provide the name for the project')
            ok_icon = Icon(icon_name='dialog-ok')
            self._save_alert.add_button(Gtk.ResponseType.OK,
                                                _('Ok'), ok_icon)
            cancel_icon = Icon(icon_name='dialog-cancel')
            self._save_alert.add_button(Gtk.ResponseType.CANCEL,
                                                _('Cancel'), cancel_icon)
            self._save_alert.connect('response',
                                             self.__save_response_cb)
            self._save_alert._name_entry.grab_focus()
            self._activity.add_alert(self._save_alert)
            self._save_alert.show()



    def __save_response_cb(self, alert, response_id):


        if response_id == Gtk.ResponseType.OK:
            folder_name = alert._name_entry.get_text()
            folder_name = folder_name.strip().replace (" ", "_")
            self._get_path(folder_name)
            self._activity.remove_alert(alert)

            try:
                # Tries to create a directory
                os.makedirs(self._storage_dir)
                self._do_save()
            except OSError as e:
                # If the directory with the same name already
                # exists, ask the user to save with another name
                self._activity.remove_alert(alert)
                self._error_alert = ErrorAlert()
                self._error_alert.props.msg = _('The project name already exists, choose another name')
                self._activity.add_alert(self._error_alert)
                self._error_alert.show()
                self._error_alert.connect('response',
                                             self.__error_response_cb)
                return

        if response_id == Gtk.ResponseType.CANCEL:
            self._activity.remove_alert(alert)

    def __error_response_cb(self, alert, response_id):
        if response_id == Gtk.ResponseType.OK:
            self._activity.remove_alert(self._error_alert)
            self.save_file()


    def _get_path(self, folder_name):
        # Creates the files directory by the specified 'folder_name'
        self._storage_dir = os.path.join(self.parent_dir, folder_name)
        self._index_html_path = os.path.join(self._storage_dir, "index.html")

    def _do_save(self):
        file_text = self._get_file_text('save')
        # Write to file
        with open(self._index_html_path, 'w') as f:
            f.write(file_text + '\n')

        save_name = os.path.basename(os.path.normpath(self._storage_dir))
        zip_name = shutil.make_archive(save_name, 'zip', self._storage_dir)
        self._add_to_journal(save_name, zip_name)


    def open_file(self):
        browser = self._activity._tabbed_view.props.current_browser
        if browser.get_uri() != self._src_uri:
            self._activity._alert("It looks like the Web Console is not open." +
                                  "You can only Open a file from Web Console")
            return
        picker = FilePicker(self._activity)
        chosen = picker.run()
        picker.destroy()
        if zipfile.is_zipfile(chosen):
            zip_object = zipfile.ZipFile(chosen, 'r')
            valid = False
            for name in zip_object.namelist():
                if name == 'index.html':
                    valid = True
                    break;
            if not valid:
                self._activity._alert("No index.html file in the zip folder.")
                return

            chosen = os.path.splitext(os.path.basename(os.path.normpath(chosen)))[0]
            self._get_path(chosen)
            zip_object.extractall(self._storage_dir)
            chosen = self._index_html_path
        self._open_file_path(chosen)

    def add_image(self):
        browser = self._activity._tabbed_view.props.current_browser
        if browser.get_uri() != self._src_uri:
            self._activity._alert("It looks like the Web Console is not open." +
                                  "You can only Open a file from Web Console")
            return
        picker = FilePicker(self._activity)
        chosen = picker.run()
        picker.destroy()
        extensions = {".jpg", ".png", ".gif", ".jpe"}
        valid = False
        self._activity._alert(chosen)
        for ext in extensions:
            if chosen.endswith(ext):
                valid = True
                break
        if not valid:
            self._activity._alert("Only jpg, png and gif files accepted")
            return
        image_name = os.path.basename(os.path.normpath(chosen))
        image_path = os.path.join(self._storage_dir, image_name)
        shutil.copyfile(chosen, image_path)



    def _get_javascript_input(self, data):
        start_head = data.find("<head>")
        end_head = data.find("</head>")
        start_script_tag = data.find("<script")
        if start_script_tag < 0 or start_head < 0 or start_head > end_head:
            return ""
        if len(data) == start_script_tag + 7:
            return ""
        end_script_tag = data.find(">", start_script_tag)
        end_script = data.find("</script>")
        if (start_head > start_script_tag or end_head < end_script or
                end_script_tag > end_script):
            return ""
        if (data.find("src=", start_script_tag, end_script_tag) > 0 or
                data.find("src =", start_script_tag, end_script_tag) > 0):
            return ""
        return data[end_script_tag + 1 : end_script]

    def _get_css_input(self, data):
        start_head = data.find("<head>")
        end_head = data.find("</head>")
        start_style_tag = data.find("<style")
        if start_style_tag < 0 or start_head < 0 or start_head > end_head:
            return ""
        if len(data) == start_style_tag + 6:
            return ""
        end_style_tag = data.find(">", start_style_tag)
        end_style = data.find("</style>")
        if (start_head > start_style_tag or end_head < end_style or
                end_style_tag > end_style):
            return ""
        return data[end_style_tag + 1 : end_style]

    def _get_html_input(self, data):
        start = data.find("<body>")
        end = data.find("</body>")
        if start > -1 and end > -1 and start < end:
            return data[start + 6 : end]
        return ""

    def _get_title(self, data):
        start = data.find("<title>")
        end = data.find("</title>")
        if start > -1 and end > -1 and start < end:
            return data[start + 7 : end]
        return ""

    def _escape_string(self, string):
        return string.replace("'", "\\\'").replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r")

    # TODO(richa): Change comments like <!-- to /* for JS.
    def _open_file_path(self, file_path):
        browser = self._activity._tabbed_view.props.current_browser
        f = open(file_path, 'r')
        data = f.read()

        js = self._escape_string(self._get_javascript_input(data))
        css = self._escape_string(self._get_css_input(data))
        html = self._escape_string(self._get_html_input(data))
        title = self._escape_string(self._get_title(data))

        fill_js_script = \
            "var div = document.getElementById('js');" \
            "div.value = '" + js + "';"
        browser.execute_script(fill_js_script)

        fill_css_script = \
            "var div = document.getElementById('css');" \
            "div.value = '" + css + "';"
        browser.execute_script(fill_css_script)

        fill_html_script = \
            "var div = document.getElementById('html');" \
            "div.value = '" + html + "';"
        browser.execute_script(fill_html_script)

        fill_title_script = "document.title = '" + title + "';"
        browser.execute_script(fill_title_script)


class SaveAlert(Alert):
    """
    Creates a alert popup to prompt the user to specify
    a name for the project to be saved.
    """
    __gtype_name__ = 'ProjectSaveAsAlert'

    def __init__(self, **kwargs):
        Alert.__init__(self, **kwargs)
        # Name entry box
        self._name_view = Gtk.EventBox()
        self._name_view.show()

        # Entry box
        self._name_entry = Gtk.Entry()
        halign = Gtk.Alignment.new(0, 0, 0, 0)
        self._hbox.pack_start(halign, False, False, 0)
        halign.add(self._name_view)
        halign.show()

        self._name_view.add(self._name_entry)
        self._name_entry.show()

        halign = Gtk.Alignment.new(0, 0, 0, 0)
        self._buttons_box = Gtk.HButtonBox()
        self._buttons_box.set_layout(Gtk.ButtonBoxStyle.END)
        self._buttons_box.set_spacing(style.DEFAULT_SPACING)
        halign.add(self._buttons_box)
        self._hbox.pack_start(halign, False, False, 0)
        halign.show()
        self.show_all()