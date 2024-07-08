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
from tkinter import ttk

import constants
from constants import LABELS

# Pre-compile nutrient fields
class PrecompileDialog(tk.Toplevel):
    def __init__(self, parent):
        # Create precompile window
        tk.Toplevel.__init__(self, parent, padx=5, pady=5)
        self.wm_title(LABELS.string_precompile_window_title)
        self.wm_attributes('-topmost', True)
        self.resizable(False, False)
        self.grab_set()

        # center precompile window
        width = 271
        height = 295
        x = parent.winfo_width()//2 - width//2 + parent.winfo_x()
        y = parent.winfo_height()//2 - height//2 + parent.winfo_y()
        # self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.geometry('+%d+%d' % (x, y))


        # Create widgets for user input of patient's info
        frame_info = ttk.Frame(master=self)
        frame_info.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        label_info = ttk.Label(master=frame_info, text=LABELS.string_precompile_window_info, width=len(LABELS.string_precompile_window_info))
        label_info.pack()

        self.frame_form = ttk.Frame(master=self)
        self.frame_form.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.frame_form.columnconfigure(0, weight=1, minsize=100, pad=5)
        self.frame_form.columnconfigure(1, weight=1, minsize=15, uniform="form")
        self.frame_form.columnconfigure(2, weight=1, minsize=50, pad=50)

        self.var_fields = [tk.StringVar() for i in range(len(LABELS.string_precompile_window_fields))]
        self.var_gender = tk.StringVar()

        for index, field in enumerate(LABELS.string_precompile_window_fields):
            label_form = ttk.Label(master=self.frame_form, text=field, justify='right')
            entry_form = ttk.Entry(master=self.frame_form, width=6, justify='right', textvariable=self.var_fields[index], validate="focusout")
            entry_form.configure(validatecommand=(entry_form.register(self.validate_field), "%P"))
            entry_form.configure(invalidcommand=(entry_form.register(self.on_invalid_field), "%W"))
            if index == 0:    
                entry_form.focus_set()
            label_form_unit = ttk.Label(master=self.frame_form, text=LABELS.string_precompile_window_fields_unit[index])

            label_form.grid(row=index, column=0, sticky="e", padx=2, pady=3)
            entry_form.grid(row=index, column=1, ipadx=3, ipady=1)
            label_form_unit.grid(row=index, column=2, sticky="w", padx=2)

        label_form = ttk.Label(master=self.frame_form, text=LABELS.string_precompile_window_gender, justify='right')
        dropdown_gender = ttk.Combobox(master=self.frame_form, values=["M","F"], state='readonly', width=4, textvariable=self.var_gender)
        dropdown_gender.set("M")

        latest_row_index = len(LABELS.string_precompile_window_fields)
        label_form.grid(row=latest_row_index, column=0, sticky="e", pady=2)
        dropdown_gender.grid(row=latest_row_index, column=1, sticky="ew")
        latest_row_index += 1

        # Create submit form button
        button_form = ttk.Button(master=self.frame_form, text=LABELS.string_precompile_window_button, command=self.on_submit)
        button_form.grid(row=latest_row_index, column=0, columnspan=3, pady=8, ipadx=5)

        # Write footnote with values accepted by the form
        frame_footnote = ttk.Frame(master=self)
        frame_footnote.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        string_local_footnote = LABELS.string_precompile_footnote.format(
            w_min=constants.WEIGHT_MIN, w_max=constants.WEIGHT_MAX, w_unit=LABELS.string_precompile_window_fields_unit[0], 
            h_min=constants.HEIGHT_MIN, h_max=constants.HEIGHT_MAX, h_unit=LABELS.string_precompile_window_fields_unit[1], 
            a_min=constants.AGE_MIN, a_max=constants.AGE_MAX, a_max_actual=constants.AGE_MAX_ACTUAL, a_unit=LABELS.string_precompile_window_fields_unit[2])
        label_footnote = ttk.Label(master=frame_footnote, text=string_local_footnote, anchor='n', justify='center')
        label_footnote.pack()

        # Submit form when you press Enter
        self.bind('<Return>', self.on_enter)

        self.pt_info = [""]

        # Print precompile window's dimensions
        # self.update_idletasks()
        # print(self.winfo_width(), self.winfo_height())


    # Check if input value is valid
    # Valid if value is empty or is a non negative float
    def validate_field(self, new_value):
        return new_value == "" or new_value.replace('.','',1).isdigit()


    # On input of an invalid field's value
    # Erase new value
    def on_invalid_field(self, widget_name):
        print("Invalid input in ", widget_name)
        # widget = self.frame_form.nametowidget(widget_name)
        entry_number = widget_name.split(".!entry")[-1]
        index = 0
        if entry_number != "":    # first entry is called "!entry", second is "!entry2", etc
            index = int(entry_number) -1
        self.var_fields[index].set("")
    

    # Handle Enter key press
    def on_enter(self, event):
        self.on_submit()
    

    # Check form input and if ok close precompile window
    def on_submit(self):
        self.pt_info = [var.get() for var in self.var_fields]
        self.pt_info.append(self.var_gender.get())
        self.check_input(self.pt_info)

        if "" not in self.pt_info:
            self.destroy()


    # Check if user input is valid: if a value is invalid, erase that value
    # Weight must be between 0 and 150 kg
    # Height must be between 120 and 220 cm
    # Age must be between 1 and 123 years
    def check_input(self, pt_info):
        try:
            weight = float(pt_info[0])
            if weight < constants.WEIGHT_MIN or weight > constants.WEIGHT_MAX:
                pt_info[0] = ""
        except:
            pt_info[0] = ""
        
        try:
            height = float(pt_info[1])
            if height < constants.HEIGHT_MIN or height > constants.HEIGHT_MAX:
                pt_info[1] = ""
        except:
            pt_info[1] = ""
        
        try:
            age = float(pt_info[2])
            if age < constants.AGE_MIN or age > constants.AGE_MAX_ACTUAL:
                pt_info[2] = ""
        except:
            pt_info[2] = ""


    # Show precompile window and pass patient's info to main window
    def show(self):
        self.wm_deiconify()
        self.wait_window()

        return self.pt_info