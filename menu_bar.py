# Copyright: (c) 2024, Anita Papetti <anitapapetti.dev@gmail.com>
#
# This file is part of NutriOptiMix
#
# NutriOptiMix is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NutriOptiMix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NutriOptiMix.  If not, see <http://www.gnu.org/licenses/>.

import tkinter as tk
from tkinter import messagebox

from constants import LABELS

class MenuBar(tk.Menu):
    def __init__(self, window):
        tk.Menu.__init__(self, window)
        
        preferences = tk.Menu(self, tearoff=0)
        preferences.add_command(label="Change settings")
        # TODO: create a popup window to change settings (font preferences, language, default values, protein per kg, harris-benedict version?)
        self.add_cascade(label="Preferences", menu=preferences)

        help = tk.Menu(self, tearoff=0)  
        help.add_command(label="View license", command=self.view_license)
        help.add_command(label="About", command=self.about)
        self.add_cascade(label="Help", menu=help)

    # Show project info
    def about(self):
            messagebox.showinfo('NutriOptiMix', LABELS.string_about)
    
    # Direct user to license file in GitHub repo
    def view_license(self):
         return