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
import pandas as pd

from constants import LABELS

class ResultsManager():
    def __init__(self, window):
        container_outer_output = ttk.Frame(master=window, border=2, relief='solid')
        container_outer_output.pack(side=tk.LEFT, fill=tk.BOTH, pady=5, padx=5, expand=True)

        self.container_output = ttk.Frame(master=container_outer_output)
        self.container_output.pack(anchor='center', expand=True)

        self.window = window

        self.results_title_font = font.nametofont("TkDefaultFont").copy()
        self.results_title_font.configure(size=14)

        self.results_string_for_clipboard = ""
        self.copy_icon = tk.PhotoImage(file="Images/content_copy_FILL0_wght200_GRAD0_opsz24.png")

        self.create_results_widgets()


    # Create widgets to display results
    def create_results_widgets(self):
        label_results_title = ttk.Label(master=self.container_output, text=LABELS.string_results_title, font=self.results_title_font)
        label_results_title.pack(anchor='center', pady=15)

        # Create space for objective values (delta, s, d)
        frame_objectives = ttk.Frame(master=self.container_output)
        frame_objectives.pack(padx=5, pady=10, anchor='nw')

        self.label_objectives = ttk.Label(master=frame_objectives, width=len(LABELS.string_objectives))
        self.label_objectives.pack(side=tk.TOP, anchor='w')

        self.label_delta = ttk.Label(master=frame_objectives)
        self.label_delta.pack(side=tk.TOP, padx=15, anchor='w')
        self.label_s = ttk.Label(master=frame_objectives)
        self.label_s.pack(side=tk.TOP, padx=15, anchor='w')
        self.label_d = ttk.Label(master=frame_objectives)
        self.label_d.pack(side=tk.TOP, padx=15, anchor='w')

        # Create space for result's formulas and solutions
        self.frame_tables = ttk.Frame(master=self.container_output)
        self.frame_tables.pack(pady=1)

        # Table of formulas
        self.table_formulas = ttk.Treeview(master=self.frame_tables, show='headings')
        self.table_formulas['columns'] = ('quantity', 'formula', 'bottles')

        self.table_formulas.column('quantity', anchor='center', width=100)
        self.table_formulas.column('formula', anchor='center', width=150)
        self.table_formulas.column('bottles', anchor='center', width=120)

        self.table_formulas.heading('quantity', text=LABELS.strings_formula_table[0], anchor='center')
        self.table_formulas.heading('formula', text=LABELS.strings_formula_table[1], anchor='center')
        self.table_formulas.heading('bottles', text=LABELS.strings_formula_table[2], anchor='center')

        # Table of solutions
        self.table_solutions = ttk.Treeview(master=self.frame_tables, show='headings')
        self.table_solutions['columns'] = ('quantity', 'solution', 'bottles')

        self.table_solutions.column('quantity', anchor='center', width=100)
        self.table_solutions.column('solution', anchor='center', width=150)
        self.table_solutions.column('bottles', anchor='center', width=120)

        self.table_solutions.heading('quantity', text=LABELS.strings_solution_table[0], anchor='center')
        self.table_solutions.heading('solution', text=LABELS.strings_solution_table[1], anchor='center')
        self.table_solutions.heading('bottles', text=LABELS.strings_solution_table[2], anchor='center')

        # Create space to write mix volume
        self.frame_volume = ttk.Frame(master=self.container_output)
        self.frame_volume.pack(padx=5, pady=10)

        self.label_volume = ttk.Label(master=self.frame_volume, anchor='center')
        self.label_volume.pack(side=tk.TOP)

        # Create space to write nutrients obtained with mix
        self.frame_nutrient_results = ttk.Frame(master=self.container_output)
        self.frame_nutrient_results.pack(padx=5)

        # Create copy to clipboard button
        self.button_copy = ttk.Button(master=self.container_output, image=self.copy_icon, width=10, command=self.copy_to_clipboard)
    

    # Copy formatted results to clipboard
    def copy_to_clipboard(self):
        pd.DataFrame([self.results_string_for_clipboard]).to_clipboard(excel=False, index=False, header=False)
        # clipboards.to_clipboard(self.results_string_for_clipboard, excel=False)


    # Write results in widgets and save them in a formatted string
    def write(self, objectives, M_used, C_used, formulas, solutions, nutrients, volume):
        self.label_objectives['text'] = LABELS.string_objectives

        self.label_delta['text'] = LABELS.string_delta + " = " + str(round(objectives[0] * 100, 2)) + "%"
        self.label_s['text'] = LABELS.string_s + " = " + str(round(objectives[1])) + " " + LABELS.string_s_unit
        self.label_d['text'] = LABELS.string_d + " = " + str(round(objectives[2], 1))

        self.results_string_for_clipboard = "delta = " + str(round(objectives[0] * 100, 2)) + "%, s = " + str(round(objectives[1] * 100)) + "%, d = " + str(round(objectives[2], 1))

        # Formulas table
        self.table_formulas.pack_forget()
        if( M_used > 0):
            for item in self.table_formulas.get_children():
                self.table_formulas.delete(item)

            for f in formulas:
                values = [round(f[0]), f[1], int(f[2])]
                # number_of_bottles = round(f[0]) / float(f[3])
                # values.append(ceil(number_of_bottles))
                self.table_formulas.insert(parent="", index=tk.END, values=values)

                self.results_string_for_clipboard += ", " + str(values[0]) + "mL " + f[1]

            self.table_formulas.pack(side=tk.TOP, padx=5, pady=5)
            self.table_formulas.configure(height=len(formulas))
        
        # Solutions table
        self.table_solutions.pack_forget()
        if( C_used > 0):
            for item in self.table_solutions.get_children():
                self.table_solutions.delete(item)

            for sol in solutions:
                values = [round(sol[0]), sol[1], int(sol[2])]
                self.table_solutions.insert(parent="", index=tk.END, values=values)

                self.results_string_for_clipboard += ", " + str(values[0]) + "mL " + sol[1]

            self.table_solutions.pack(side=tk.TOP, padx=5, pady=5)
            self.table_solutions.configure(height=len(solutions))
        
        # Total mix volume        
        self.label_volume['text'] = LABELS.string_volume + " = " + str(round(volume)) + " " + LABELS.string_Vmin_unit
        self.results_string_for_clipboard += ", V = " + str(round(volume)) + " " + LABELS.string_Vmin_unit
        
        # Nutrients obtained
        # nutrients = [kcal, prot, fat, carbo, na, k, ca, mg, p, fe]
        for widget in self.frame_nutrient_results.grid_slaves():
            widget.destroy()

        self.label_obtained = ttk.Label(master=self.frame_nutrient_results, text=LABELS.string_nutrient_results, anchor='center')
        self.label_obtained.grid(row=0, column=0, columnspan=2, sticky='n')
        
        for i,n in enumerate(nutrients[1:4]):
            string_label = LABELS.string_nutrients[i] + " = " + "{:.1f}".format(n) + " " + LABELS.string_nutrients_unit[i]
            label = ttk.Label(master=self.frame_nutrient_results, text=string_label)
            label.grid(row=i+1, column=0, padx=10, sticky='w')

            self.results_string_for_clipboard += ", " + string_label

        string_label = LABELS.string_nutrients_energy + " = " + "{:.1f}".format(nutrients[0]) + " " + LABELS.string_nutrients_energy_unit
        label = ttk.Label(master=self.frame_nutrient_results, text=string_label)
        label.grid(row=4, column=0, padx=10, sticky='w')

        self.results_string_for_clipboard += ", " + string_label

        for i,n in enumerate(nutrients[4:]):
            string_label = LABELS.string_nutrients[i+3] + " = " + "{:.0f}".format(n) + " " + LABELS.string_nutrients_unit[i+3]
            label = ttk.Label(master=self.frame_nutrient_results, text=string_label)
            label.grid(row=i+1, column=1, padx=10, sticky='w')

            self.results_string_for_clipboard += ", " + string_label
        
        if self.button_copy not in self.container_output.pack_slaves():
            self.button_copy.pack(padx=5, pady=5, ipadx=5, side=tk.BOTTOM, anchor='sw')
        
            
                


            

            
    
