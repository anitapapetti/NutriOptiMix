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
from tkinter import font, ttk

import constants, menu_bar, mix_calculator, results_manager,window_precompile
from constants import LABELS
from nutrients_calculator import calculate_nutrients


class App(tk.Tk):    
    def __init__(self):
        # Create main window
        super().__init__()

        self.title("NutriOptiMix")
        self.config(padx=15, pady=5)
        self.minsize(1150, 650)
        self.geometry('+75+50')
        menubar = menu_bar.MenuBar(self)
        self.config(menu=menubar)

        # Font
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(size=10)
        # default_font.configure(family='Segoe UI', size=9, weight='normal', slant='roman', underline=0, overstrike=0)  # default

        font.nametofont("TkHeadingFont").configure(size=10)

        # Style
        style = ttk.Style()
        style.configure("Treeview.Heading", rowheight=int(self.default_font['size']*2.5))
        style.configure("Treeview", rowheight=int(self.default_font['size']*2.5))

        # Widgets
        self.create_input_widgets()

        # Internal manager class
        self.results_manager = results_manager.ResultsManager(self)
    
    # Create all widgets for user input
    def create_input_widgets(self):
        # TODO: give option of importing nutrients from csv ???

        self.container_input = ttk.Frame(border=2, relief='solid')
        self.container_input.pack(side=tk.LEFT, pady=5, padx=5, fill='y')

        self.create_params_widgets()
        self.create_nutrients_widgets()
        self.create_precompile_widgets()

    # Solve problem and write results in main window
    def solve(self, user_nutrients, user_weights):
        print("Submitted: ", user_nutrients)

        if self.var_Mmax == "":
            self.var_Mmax = constants.DEFAULT_MMAX
        if self.var_Cmax == "":
            self.var_Cmax = constants.DEFAULT_CMAX
        if self.var_Vmin == "":
            self.var_Vmin = constants.DEFAULT_VMIN
        if self.var_Smax == "":
            self.var_Smax = self.var_Mmax * 500 + 500     # max waste tolerated = 500mL for each formula + 500 mL to be safe
        if self.var_Dmax == "":
            self.var_Dmax = self.var_Mmax * 500 + 500 
        
        objectives, m, c, formulas, solutions, nutrients, volume = mix_calculator.MixCalculator(int(self.var_Mmax.get()), int(self.var_Cmax.get()), float(self.var_Vmin.get()), float(self.var_Smax.get()), float(self.var_Dmax.get())).solve(user_nutrients, user_weights)
        # if self.results_manager == None:
        #     self.results_manager = results_manager.ResultsManager(self)
        self.results_manager.write(objectives, m, c, formulas, solutions, nutrients, volume)


    ####################################################################
    # Create widgets to modify model parameters
    def create_params_widgets(self):
        self.container_params = ttk.Frame(master=self.container_input)
        self.container_params.pack(pady=5, anchor='nw')

        # Tell the user to insert model parameters
        frame_params_directions = ttk.Frame(master=self.container_params)
        frame_params_directions.pack(padx=15, pady=5, anchor='nw')

        label_params = ttk.Label(master=frame_params_directions, text=LABELS.string_params_directions, width=len(LABELS.string_params_directions))   
        label_params.pack(padx=3, pady=3, side=tk.LEFT)

        # Model parameters
        frame_params_fields = ttk.Frame(master=self.container_params)
        frame_params_fields.pack(padx=30, pady=5, anchor='nw')

        # Validate parameters entries
        # True if new_value is a non negative float
        def check_param(new_value):
            if new_value == "":
                return False
            try:
                param = float(new_value)
                if param >= 0.0:
                    return True
                else:
                    return False
            except:
                return False
        
        # Validate parameters entries
        # True if new_value is a non negative integer
        def check_param_integer(new_value):
            if new_value == "":
                return False
            try:
                param = float(new_value)
                param_integer = int(new_value)
                if param >= 0.0 & param == param_integer:
                    return True
                else:
                    return False
            except:
                return False

        # On input of an invalid Mmax value
        # Reset to default value
        def on_invalid_Mmax():
            print("Invalid input for Mmax. Value reset to default.")
            self.var_Mmax.set(constants.DEFAULT_MMAX)

        # On input of an invalid Cmax value
        # Reset to default value
        def on_invalid_Cmax():
            print("Invalid input for Cmax. Value reset to default.")
            self.var_Cmax.set(constants.DEFAULT_CMAX)

        # On input of an invalid Vmin value
        # Reset to default value
        def on_invalid_Vmin():
            print("Invalid input for Vmin. Value reset to default.")
            self.var_Vmin.set(constants.DEFAULT_VMIN)
            
        # On input of an invalid Smax value
        # Reset to default value
        def on_invalid_Smax():
            print("Invalid input for Smax. Value reset to default.")
            self.var_Smax.set(constants.DEFAULT_MMAX * 500 + 500)
        
        # On input of an invalid Dmax value
        # Reset to default value
        def on_invalid_Dmax():
            print("Invalid input for Dmax. Value reset to default.")
            self.var_Dmax.set(constants.DEFAULT_MMAX * 500 + 500)

        self.var_Mmax = tk.StringVar()
        label_Mmax = ttk.Label(master=frame_params_fields, text=LABELS.string_Mmax, justify='right')
        entry_Mmax = ttk.Entry(master=frame_params_fields, width=6, justify='right', textvariable=self.var_Mmax, validate='focusout')
        entry_Mmax.configure(validatecommand=(entry_Mmax.register(check_param_integer), "%P"))
        entry_Mmax.configure(invalidcommand=(entry_Mmax.register(on_invalid_Mmax)))
        entry_Mmax.insert(0, constants.DEFAULT_MMAX)
        label_Mmax.grid(row=0, column=0, padx=5, pady=5)
        entry_Mmax.grid(row=0, column=1)

        self.var_Cmax = tk.StringVar()
        label_Cmax = ttk.Label(master=frame_params_fields, text=LABELS.string_Cmax, justify='right')
        entry_Cmax = ttk.Entry(master=frame_params_fields, width=6, justify='right', textvariable=self.var_Cmax, validate='focusout')
        entry_Cmax.configure(validatecommand=(entry_Cmax.register(check_param_integer), "%P"))
        entry_Cmax.configure(invalidcommand=(entry_Cmax.register(on_invalid_Cmax)))
        entry_Cmax.insert(0, constants.DEFAULT_CMAX)
        label_Cmax.grid(row=1, column=0, padx=5)
        entry_Cmax.grid(row=1, column=1)

        self.var_Vmin = tk.StringVar()
        label_Vmin = ttk.Label(master=frame_params_fields, text=LABELS.string_Vmin, width=len(LABELS.string_Dmax)+5, anchor='e')
        entry_Vmin = ttk.Entry(master=frame_params_fields, width=6, justify='right', textvariable=self.var_Vmin, validate='focusout')
        entry_Vmin.configure(validatecommand=(entry_Vmin.register(check_param), "%P"))
        entry_Vmin.configure(invalidcommand=(entry_Vmin.register(on_invalid_Vmin)))
        entry_Vmin.insert(0, constants.DEFAULT_VMIN)
        label_Vmin_unit = ttk.Label(master=frame_params_fields, text=LABELS.string_Vmin_unit, justify='left')
        label_Vmin.grid(row=0, column=2, padx=5, pady=5)
        entry_Vmin.grid(row=0, column=3)
        label_Vmin_unit.grid(row=0, column=4, padx=3)

        self.var_Smax = tk.StringVar()
        label_Smax = ttk.Label(master=frame_params_fields, text=LABELS.string_Smax, width=len(LABELS.string_Dmax)+5, anchor='e')
        entry_Smax = ttk.Entry(master=frame_params_fields, width=6, justify='right', textvariable=self.var_Smax, validate='focusout')
        entry_Smax.configure(validatecommand=(entry_Smax.register(check_param), "%P"))
        entry_Smax.configure(invalidcommand=(entry_Smax.register(on_invalid_Smax)))
        starting_Smax = constants.DEFAULT_MMAX * 500 + 500   # usually, formula bottles are up to 500 mL each
        entry_Smax.insert(0, starting_Smax)
        label_Smax_unit = ttk.Label(master=frame_params_fields, text=LABELS.string_Smax_unit, justify='left')
        label_Smax.grid(row=1, column=2, padx=5, pady=5)
        entry_Smax.grid(row=1, column=3)
        label_Smax_unit.grid(row=1, column=4, padx=3)

        self.var_Dmax = tk.StringVar()
        label_Dmax = ttk.Label(master=frame_params_fields, text=LABELS.string_Dmax, width=len(LABELS.string_Dmax)+5, anchor='e')
        entry_Dmax = ttk.Entry(master=frame_params_fields, width=6, justify='right', textvariable=self.var_Dmax, validate='focusout')
        entry_Dmax.configure(validatecommand=(entry_Dmax.register(check_param), "%P"))
        entry_Dmax.configure(invalidcommand=(entry_Dmax.register(on_invalid_Dmax)))
        starting_Dmax = constants.DEFAULT_MMAX * 500 + 500   # usually, formula bottles are up to 500 mL each
        entry_Dmax.insert(0, starting_Dmax)
        label_Dmax.grid(row=2, column=2, padx=5, pady=5)
        entry_Dmax.grid(row=2, column=3)


    ####################################################################
    # Create widgets for nutrients values and formula mix calculation
    def create_nutrients_widgets(self):
        self.container_nutrients = ttk.Frame(master=self.container_input)
        self.container_nutrients.pack(pady=5, anchor='nw')

         # Tell the user to insert nutrient requirements
        frame_directions = ttk.Frame(master=self.container_nutrients)
        frame_directions.pack(padx=15, anchor='nw')

        label_directions = ttk.Label(master=frame_directions, text=LABELS.string_directions, width=len(LABELS.string_directions))
        label_directions.pack()

        # Nutrient requirements fields
        frame_nutrients = ttk.Frame(master=self.container_nutrients)
        frame_nutrients.pack(padx=15, anchor='center', fill=tk.BOTH)

        # Layout config
        frame_nutrients.rowconfigure([0,1,2,3,4,5,6], weight=1, minsize=50)
        frame_nutrients.columnconfigure([0,6], weight=1, minsize=100)           # nutrient's name
        frame_nutrients.columnconfigure([1,7], weight=1, minsize=15)            # nutrient's value
        frame_nutrients.columnconfigure([2,8], weight=1, minsize=50)            # nutrient's unit
        frame_nutrients.columnconfigure([3,9], weight=1, minsize=5)             # - button
        frame_nutrients.columnconfigure([4,10], weight=1, minsize=10)           # weight's value
        frame_nutrients.columnconfigure([5,11], weight=1, minsize=5)            # + button

        # Weight title
        label_weight1 = ttk.Label(master=frame_nutrients, text=LABELS.string_nutrients_weight, justify='center')
        label_weight1.grid(row=0, column=3, columnspan=3)
        label_weight2 = ttk.Label(master=frame_nutrients, text=LABELS.string_nutrients_weight, justify='center')
        label_weight2.grid(row=0, column=9, columnspan=3)

        # Validate nutrient's value
        # Ok if value is empty or is a float
        def check_nutrient(new_value):
            return new_value == "" or new_value.lstrip('-').replace('.','',1).replace('e-','',1).replace('e','',1).isdigit()
        
        # On input of an invalid nutrient's value
        # Erase new value
        def on_invalid_nutrient(widget_name):
            print("Invalid input in ", widget_name)
            # widget = self.container_nutrients.nametowidget(widget_name)
            entry_number = widget_name.split(".!entry")[-1]
            index = 0
            if entry_number != "":    # first entry is called "!entry", second is "!entry2", etc
                index = (int(entry_number) -1) // 2
            self.var_nutrients[index].set("")
            # self.var_nutrients[index].set(old_value)

        # Validate weight's value
        # Ok if value is float with one decimal value between 0.0 and 1.0
        def check_weight(new_value):
            if new_value in constants.VALID_WEIGHTS:
                return True
            else: 
                return False

        # On input of an invalid weight's value
        # Reset value to default weight
        def on_invalid_weight(widget_name):
            print("Invalid input in ", widget_name)
            # widget = self.container_nutrients.nametowidget(widget_name)
            index = int(widget_name[len(widget_name)-1]) // 2
            self.var_weights[index].set(constants.DEFAULT_WEIGHTS[index])
            # self.var_weights[index].set(old_value)
                
        # Decrease weight of one decimal point (must stay between 0.0 and 1.0)
        def decrease_weight(index):
            w = self.var_weights[index]
            if w.get() == "":
                w.set("0.0")
            else:
                try:
                    weight = float(w.get())
                    weight -= 0.1
                    if weight <= 0.0:
                        w.set("0.0")
                    elif weight >= 1.0:
                        w.set("1.0")
                    else:                        
                        w.set(str(round(weight,1)))
                except:
                    w.set(constants.DEFAULT_WEIGHTS[index])

        # Increase weight of one decimal point (must stay between 0.0 and 1.0)    
        def increase_weight(index):
            w = self.var_weights[index]
            if w.get() == "":
                w.set("0.0")
            else:
                try:
                    weight = float(w.get())
                    weight += 0.1
                    if weight <= 0.0:
                        w.set("0.0")
                    elif weight >= 1.0:
                        w.set("1.0")
                    else:                        
                        w.set(str(round(weight,1)))
                except:
                    w.set(constants.DEFAULT_WEIGHTS[index])
        
        # Erase all nutrients values
        def erase_nutrients():
            for var_nutrient in self.var_nutrients:
                var_nutrient.set("")
        
        # Reset all weights to default values
        def reset_weights():
            for i, var_weight in enumerate(self.var_weights):
                var_weight.set(constants.DEFAULT_WEIGHTS[i])

        # Create nutrients' and weights' widgets (except energy's)
        self.var_nutrients = [tk.StringVar() for i in range(len(LABELS.string_nutrients))]
        self.var_weights = [tk.StringVar() for i in range(len(LABELS.string_nutrients))]
        self.entry_nutrients = []
        for index, nutrient in enumerate(LABELS.string_nutrients):
            row = index + 1
            col = 0
            if index >= 3:
                row = (index + 3) % 6 + 1
                col = 6
            
            label_nutrient = ttk.Label(master=frame_nutrients, text=nutrient, justify='right')
            entry_nutrient = ttk.Entry(master=frame_nutrients, width=6, justify='right', textvariable=self.var_nutrients[index], validate='focusout')
            entry_nutrient.configure(validatecommand=(entry_nutrient.register(check_nutrient), "%P"))
            entry_nutrient.configure(invalidcommand=(entry_nutrient.register(on_invalid_nutrient), "%W"))
            self.entry_nutrients.append(entry_nutrient)
            if index == 0:
                entry_nutrient.focus_set()
            label_nutrient_unit = ttk.Label(master=frame_nutrients, text=LABELS.string_nutrients_unit[index], justify='left')

            button_minus = ttk.Button(master=frame_nutrients, text="-", width=len("-"), command=lambda index=index: decrease_weight(index+1))
            entry_weight = ttk.Entry(master=frame_nutrients, width=3, justify='center', textvariable=self.var_weights[index], validate='focusout')
            entry_weight.configure(validatecommand=(entry_weight.register(check_weight),"%P"))
            entry_weight.configure(invalidcommand=(entry_weight.register(on_invalid_weight),"%W"))
            entry_weight.insert(0, constants.DEFAULT_WEIGHTS[index+1])
            button_plus = ttk.Button(master=frame_nutrients, text="+", width=len("+"), command=lambda index=index: increase_weight(index+1))

            label_nutrient.grid(row=row, column=col, sticky="e")
            entry_nutrient.grid(row=row, column=col+1, ipadx=3, ipady=1)
            label_nutrient_unit.grid(row=row, column=col+2, sticky="w", padx=1)
            button_minus.grid(row=row, column=col+3, sticky="e")
            entry_weight.grid(row=row, column=col+4)
            button_plus.grid(row=row, column=col+5, sticky="w")


        # Create energy widgets
        self.var_weights.insert(0, tk.StringVar())
        var_energy = tk.StringVar()
        label_nutrients_energy = ttk.Label(master=frame_nutrients, text=LABELS.string_nutrients_energy)
        entry_nutrients_energy = ttk.Entry(master=frame_nutrients, width=7, state='readonly', textvariable=var_energy, justify='right')
        var_energy.set("0.0")
        label_nutrients_energy_unit = ttk.Label(master=frame_nutrients, text=LABELS.string_nutrients_energy_unit)
        button_minus = ttk.Button(master=frame_nutrients, text="-", width=len("-"), command=lambda: decrease_weight(0))
        entry_nutrients_energy_weight = ttk.Entry(master=frame_nutrients, width=3, textvariable=self.var_weights[0], justify='center')
        entry_nutrients_energy_weight.insert(0, constants.DEFAULT_WEIGHTS[0])
        button_plus = ttk.Button(master=frame_nutrients, text="+", width=len("+"), command=lambda: increase_weight(0))

        row_energy = 4
        label_nutrients_energy.grid(row=row_energy, column=0, sticky="e", padx=5)
        entry_nutrients_energy.grid(row=row_energy, column=1)
        label_nutrients_energy_unit.grid(row=row_energy, column=2, sticky="w", padx=1)
        button_minus.grid(row=row_energy, column=3, sticky="e")
        entry_nutrients_energy_weight.grid(row=row_energy, column=4)
        button_plus.grid(row=row_energy, column=5, sticky="w")


        # Set tab order to start moving from a nutrient to the next
        for entry in self.entry_nutrients:
            entry.lift()


        # Create reset buttons
        button_reset_nutrients = ttk.Button(master=frame_nutrients, text=LABELS.string_reset_nutrients, width=len(LABELS.string_reset_nutrients), command=erase_nutrients)
        button_reset_nutrients.grid(row=5, column=0, columnspan=3)

        button_reset_weights = ttk.Button(master=frame_nutrients, text=LABELS.string_reset_weights, width=len(LABELS.string_reset_weights), command=reset_weights)
        button_reset_weights.grid(row=5, column=3, columnspan=3)


        # Update energy value interactively
        # energy in kcal = carbohydrates in g * 4 + fat in g * 9 + protein in g * 4
        def update_energy_value(var, index, mode):
            protein = self.var_nutrients[0].get()
            if protein == "": protein = 0
            fat = self.var_nutrients[1].get()
            if fat == "": fat = 0
            carbs = self.var_nutrients[2].get()
            if carbs == "": carbs = 0
            
            try:
                protein = float(protein) 
                if protein < 0:  protein = 0
                fat = float(fat)
                if fat < 0:  fat = 0
                carbs = float(carbs)
                if carbs < 0:   carbs = 0

                energy = protein * 4.0 + fat * 9.0 + carbs * 4.0
                energy = round(energy, 1)
                var_energy.set(str(energy))
            except:
                var_energy.set("")

        self.var_nutrients[0].trace_add('write', update_energy_value)
        self.var_nutrients[1].trace_add('write', update_energy_value)
        self.var_nutrients[2].trace_add('write', update_energy_value)


        # Check if input is valid and reset invalid fields
        # nutrients must be float
        # weights must be float between 0.0 and 1.0
        # at least one nutrient must be > 0
        # at least one weight must be > 0
        def validate_input(nutrients, weights):
            all_ok = True

            no_target = True
            for i, nutrient in enumerate(nutrients[1:]):
                try:
                    n = float(nutrient)
                    if n > 0.0:
                        no_target = False
                    elif n < 0.0:
                        self.var_nutrients[i].set("0.0")
                    # TODO: remove red color from entry box outline
                except:
                    # TODO: color entry box outline red
                    self.var_nutrients[i].set("")
                    all_ok = False

            all_weights_zero = True
            for i, weight in enumerate(weights):
                try:
                    w = float(weight)
                    if w < 0.0 or w > 1.0:
                        self.var_weights[i].set(w_default)
                        all_ok = False
                    elif w > 0.0:
                        all_weights_zero = False
                except:
                    w_default = constants.DEFAULT_WEIGHTS[i]
                    self.var_weights[i].set(w_default)
                    all_ok = False
            return all_ok and not no_target and not all_weights_zero
        
        # Trigger formula mix calculation
        def handle_submit():
            user_nutrients = [var_energy.get()]
            for v in self.var_nutrients:
                value = v.get()
                if value == "": value = '0'
                user_nutrients.append(value)
            user_weights = []    
            for v in self.var_weights:
                value = v.get()
                if value == "": value = '0'
                user_weights.append(value)

            if validate_input(user_nutrients, user_weights):
                self.solve(user_nutrients, user_weights)



        # Create solve button
        frame_submit = ttk.Frame(master=self.container_nutrients)
        frame_submit.pack(padx=5, pady=5, anchor='center')

        button_submit = ttk.Button(master=frame_submit, text=LABELS.string_submit_button, command=handle_submit)
        button_submit.pack(padx=3, ipadx=5, side=tk.TOP)


        # Create widgets for footnotes (instructions for user)
        frame_notes = ttk.Frame(master=self.container_nutrients)
        frame_notes.pack(padx=20, pady=5, anchor='center')

        label_notes = ttk.Label(master=frame_notes, text=LABELS.string_notes, font=(self.default_font.actual('family'), self.default_font.actual('size')-1, self.default_font.actual('weight')))
        label_notes.pack(padx=3, pady=10, side=tk.BOTTOM, fill=tk.BOTH)


    ####################################################################
    # Create widgets to compile nutrients values automatically 
    def create_precompile_widgets(self):
        self.container_precompile = ttk.Frame(master=self.container_input)
        self.container_precompile.pack(pady=10, anchor='nw')

        # Write nutrients calculated from patient's info
        def write_nutrients():
            nutrients = calculate_nutrients(self.pt_info[0], self.pt_info[1], self.pt_info[2], self.pt_info[3])

            for i, nutrient in enumerate(nutrients[1:]):
                if i < 3:
                    n = "{:.1f}".format(nutrient)
                else:
                    n = "{:.0f}".format(nutrient)
                self.var_nutrients[i].set(n)

        # Open popup window and wait for user to input patient's info,
        # then write patient's info at the bottom of main window
        # and write nutrients calculated in main window's nutrients fields
        def on_precompile():
            results = window_precompile.PrecompileDialog(self).show()

            if "" in results:
                return
            
            self.pt_info = results

            self.geometry('')

            if (self.frame_patient in self.container_precompile.pack_slaves()):
                for widget in self.frame_patient.pack_slaves():
                    widget.destroy()
            else:
                # add patient's info at the bottom
                self.frame_patient.pack(padx=20, anchor='w')
                
            string_patient_data = []
            string_patient_data.append(LABELS.string_precompile_window_fields[0] + ": " + self.pt_info[0] + " " + LABELS.string_precompile_window_fields_unit[0])
            string_patient_data.append(LABELS.string_precompile_window_fields[1] + ": " + self.pt_info[1] + " " + LABELS.string_precompile_window_fields_unit[1])
            string_patient_data.append(LABELS.string_precompile_window_fields[2] + ": " + self.pt_info[2] + " " + LABELS.string_precompile_window_fields_unit[2])
            string_patient_data.append(LABELS.string_precompile_window_gender + ": " + self.pt_info[3])

            for i in range(len(self.pt_info)):
                label_patient = ttk.Label(master=self.frame_patient, text=string_patient_data[i], justify='left')
                label_patient.pack(padx=0, pady=3, side=tk.TOP)

            button_refill = ttk.Button(master=self.frame_patient, text=LABELS.string_patient_button, width=len(LABELS.string_patient_button), command=write_nutrients)
            button_refill.pack(padx=0, pady=3, fill=tk.BOTH, side=tk.RIGHT, expand=True)

            # write nutrients in main window's fields
            write_nutrients()
            

        # Create precompile widgets in main window
        frame_precompile = ttk.Frame(master=self.container_precompile)
        frame_precompile.pack(padx=20, ipadx=2, ipady=2, anchor='center')

        label_precompile = ttk.Label(master=frame_precompile, text=LABELS.string_precompile, width=len(LABELS.string_precompile)-10)
        label_precompile.pack(padx=0, pady=2, anchor='center', side=tk.LEFT, fill=tk.BOTH)

        button_precompile = ttk.Button(master=frame_precompile, text=LABELS.string_precompile_button, width=len(LABELS.string_precompile_button), command=on_precompile)
        button_precompile.pack(padx=2, ipadx=3, anchor='center', side=tk.LEFT, fill=tk.X, expand=True)

        self.frame_patient = ttk.Frame(master=self.container_precompile)


####################################################################
# Start the application
if __name__ == '__main__':
    app = App()
    app.mainloop()