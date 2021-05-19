#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  protonup-gtk.py
#
#  Copyright 2020 Thomas Castleman <contact@draugeros.org>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
"""ProtonUp GTK GUI"""
import protonup
import threading
import os
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Main(Gtk.Window):
    """Main UI Window"""
    def __init__(self):
        """Initialize the Window"""
        Gtk.Window.__init__(self, title="ProtonUp GTK+")
        self.grid = Gtk.Grid(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.grid)
        self.set_icon_name("steam")

        # a couple Class-wide vars to work around the limitations of passing
        # data in GTK+
        self.selected_tag = None

        self.main_menu("clicked")

    def _set_default_margins(self, widget):
        """Set default margin size"""
        widget.set_margin_start(10)
        widget.set_margin_end(10)
        widget.set_margin_top(10)
        widget.set_margin_bottom(10)
        return widget

    def main_menu(self, button):
        """Main initial window for ProtonUp"""
        # Get data to make the window
                
        # Make UI elements
        label = Gtk.Label()
        label.set_markup("<b>Installed Proton Versions</b>")
        label.set_justify(Gtk.Justification.LEFT)
        label = self._set_default_margins(label)
        
        sep = Gtk.Separator.new(Gtk.Orientation.HORIZONTAL)
        sep.set_margin_top(20)
        sep.set_margin_bottom(20)
        sep.set_margin_start(10)
        sep.set_margin_end(10)
        
        label2 = Gtk.Label()
        label2.set_markup("Uninstall: ")
        label2.set_justify(Gtk.Justification.LEFT)
        label2 = self._set_default_margins(label2)
        
        label3 = Gtk.Label()
        label3.set_markup("Install: ")
        label3.set_justify(Gtk.Justification.LEFT)
        label3 = self._set_default_margins(label3)
        
        uninst_button = Gtk.Button.new_with_label("Uninstall")
        uninst_button.connect("clicked", self.uninst_confirm)
        uninst_button = self._set_default_margins(uninst_button)
        
        inst_button = Gtk.Button.new_with_label("Install")
        inst_button.connect("clicked", self.inst_confirm)
        inst_button = self._set_default_margins(inst_button)
        
        up_button = Gtk.Button.new_with_label("Update")
        up_button.connect("clicked", self.up_conf)
        up_button = self._set_default_margins(up_button)
        
        refresh_button = Gtk.Button.new_with_label("Refresh")
        refresh_button.connect("clicked", self.main_menu)
        refresh_button = self._set_default_margins(refresh_button)
        
        # Make sure nothing is happening in the background before we proceed
        while True:
            if not os.path.exists("/tmp/protonup"):
                time.sleep(0.01)
                break
            time.sleep(2)
            
        # Do this after the pause so that we get up-to-date info
        # Installed Proton Versions
        pro_inst = protonup.installed_versions()
        new_pro_inst = pro_inst[0]
        count = 1
        if len(pro_inst) > 1:
            for each in pro_inst[1:]:
                if count < 4:
                    count += 1
                    new_pro_inst = new_pro_inst + "\t\t" + each
                else:
                    count = 1
                    new_pro_inst = new_pro_inst + "\n" + each
        
        # Proton Versions available for install
        tags = protonup.fetch_releases()
        for each in pro_inst:
            if each[7:] in tags:
                del tags[tags.index(each[7:])]

        # make window
        self.clear_window()
        
        label1 = Gtk.Label()
        label1.set_markup(new_pro_inst)
        label1.set_justify(Gtk.Justification.LEFT)
        label1 = self._set_default_margins(label1)
        
        uninst_select = Gtk.ComboBoxText()
        for each in pro_inst:
            uninst_select.append(each, each)
        uninst_select.connect("changed", self.select_tag)
        uninst_select = self._set_default_margins(uninst_select)
        
        inst_select = Gtk.ComboBoxText()
        for each in tags:
            inst_select.append(each, each)
        inst_select.connect("changed", self.select_tag)
        inst_select = self._set_default_margins(inst_select)
        
        self.grid.attach(label, 0, 0, 10, 1)
        self.grid.attach(label1, 0, 1, 10, 1)
        self.grid.attach(uninst_select, 2, 3, 3, 1)
        self.grid.attach(inst_select, 2, 4, 3, 1)
        self.grid.attach(sep, 0, 2, 10, 1)
        self.grid.attach(label2, 0, 3, 2, 1)
        self.grid.attach(label3, 0, 4, 2, 1)
        self.grid.attach(uninst_button, 5, 3, 1, 1)
        self.grid.attach(inst_button, 5, 4, 1, 1)
        self.grid.attach(up_button, 0, 5, 4, 1)
        self.grid.attach(refresh_button, 5, 5, 5, 1)

        # display window changes
        self.show_all()

    def up_conf(self, button):
        """Confirm Update"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("Are you sure you want to update Proton to the latest release?")
        label.set_justify(Gtk.Justification.CENTER)
        label = self._set_default_margins(label)
        self.grid.attach(label, 0, 0, 3, 1)

        yes = Gtk.Button.new_with_label("Update")
        yes.connect("clicked", self.update)
        yes = self._set_default_margins(yes)
        self.grid.attach(yes, 0, 2, 1, 1)

        no = Gtk.Button.new_with_label("Cancel")
        no.connect("clicked", self.main_menu)
        no = self._set_default_margins(no)
        self.grid.attach(no, 2, 2, 1, 1)

        self.show_all()

    def update(self, button):
        """Update Proton to the latest release"""
        self.selected_tag = "latest"
        self.install("clicked")

    def select_tag(self, widget):
        """select a tag to uninstall/install"""
        text = widget.get_active_text()
        if text[:7] == "Proton-":
            text = text[7:]
        self.selected_tag = text

    def inst_confirm(self, button):
        """confirm installation"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("Are you sure you want to Install Proton %s?" % (self.selected_tag))
        label.set_justify(Gtk.Justification.CENTER)
        label = self._set_default_margins(label)
        self.grid.attach(label, 0, 0, 3, 1)

        yes = Gtk.Button.new_with_label("Install")
        yes.connect("clicked", self.install)
        yes = self._set_default_margins(yes)
        self.grid.attach(yes, 0, 2, 1, 1)

        no = Gtk.Button.new_with_label("Cancel")
        no.connect("clicked", self.main_menu)
        no = self._set_default_margins(no)
        self.grid.attach(no, 2, 2, 1, 1)

        self.show_all()

    def uninst_confirm(self, button):
        """confirm removal"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    Are you sure you want to uninstall Proton %s?\t
""" % (self.selected_tag))
        label.set_justify(Gtk.Justification.CENTER)
        label = self._set_default_margins(label)
        self.grid.attach(label, 0, 0, 3, 1)

        yes = Gtk.Button.new_with_label("Uninstall")
        yes.connect("clicked", self.uninstall)
        yes = self._set_default_margins(yes)
        self.grid.attach(yes, 0, 2, 1, 1)

        no = Gtk.Button.new_with_label("Cancel")
        no.connect("clicked", self.main_menu)
        no = self._set_default_margins(no)
        self.grid.attach(no, 2, 2, 1, 1)

        self.show_all()

    def install(self, button):
        """Uninstall Proton version in self.selected_tag"""
        self.clear_window()

        label = Gtk.Label()
        label.set_markup("""
    Installing Proton %s, this may take some time...
""" % (self.selected_tag))
        label.set_justify(Gtk.Justification.CENTER)
        label = self._set_default_margins(label)
        self.grid.attach(label, 1, 1, 1, 1)
        
        self.show_all()
        time.sleep(0.1)

        timer = threading.Timer(0.1, self.main_menu, args=".")
        timer.start()

        protonup.get_proton(version=self.selected_tag)

    def uninstall(self, button):
        """Install Proton version in self.selected_tag"""
        protonup.remove_proton(self.selected_tag)
        self.main_menu("clicked")

    def clear_window(self):
        """Clear Window"""
        children = self.grid.get_children()
        for each0 in children:
            self.grid.remove(each0)

    def exit(self, button):
        """Exit"""
        Gtk.main_quit("delete-event")
        self.destroy()


def show_main():
    """Show Main UI"""
    window = Main()
    window.set_decorated(True)
    window.set_resizable(False)
    window.set_position(Gtk.WindowPosition.CENTER)
    window.connect("delete-event", Main.exit)
    window.show_all()
    Gtk.main()
    window.exit("clicked")

if __name__ == "__main__":
    show_main()
