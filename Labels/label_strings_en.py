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

# Label strings in English

class EnglishLabels:
    # make all fields of this class read-only
    __slots__ = ()
    
    # Main window's strings
    string_params_directions = "Insert solving parameters:"
    string_Mmax = "Max number of formulas"
    string_Cmax = "Max number of solutions"
    string_Vmin = "Min volume of each formula/solution"
    string_Vmin_unit = "mL"
    string_Smax = "Max total formula waste tolerated"
    string_Smax_unit = "mL"
    string_Dmax = "Max penalty for use of lower priority formulas"

    string_directions = "Insert target values for nutrients:*"

    string_nutrients_energy = "Energy"
    string_nutrients_energy_unit = "kcal"
    string_nutrients = [
        "Protein", "Fat", "Carbohydrates",
        "Na", "K", "Ca",
        "Mg", "P", "Fe"
    ]
    string_nutrients_unit = [
        "g", "g", "g",
        "mg", "mg", "mg",
        "mg", "mg", "mg"
    ]
    string_nutrients_weight = "Weight"

    string_submit_button = "Calculate mix"
    string_reset_nutrients = "Erase all nutrients"
    string_reset_weights = "Reset all weights"

    string_notes = "* target values <= 0 or undefined will be ignored. Energy is calculated automatically and depends on carbohydrates, fat and protein."

    string_precompile = "[Optional] Pre-fill fields with nutritional values for a sedentary lifestyle:"
    string_precompile_button = "Insert patient's data"

    # Precompile popup window's strings
    string_precompile_window_title = "Patient's data"
    string_precompile_window_info =  "Insert patient's data:"
    string_precompile_window_fields = [
        "Weight", "Height", "Age"
    ]
    string_precompile_window_fields_unit = [
        "kg", "cm", "years"
    ]
    string_precompile_window_gender = "Gender"
    string_precompile_window_button = "Calculate nutritional values*"

    string_precompile_footnote = "* weight must be between {w_min} and {w_max} {w_unit}\nheight must be between {h_min} and {h_max} {h_unit}\nage must be between {a_min} and {a_max_actual} {a_unit}\n(Less accurate for ages beyond {a_max} {a_unit})"

    # After precompile
    string_patient_button = string_precompile_window_button

    # After solve
    string_results_title = "RESULTS"

    string_objectives = "Objective values:"
    # string_delta = chr(948)   # greek letter delta
    string_delta = "Max deviation from target"
    string_s = "Total formula waste"
    string_s_unit = "mL"
    string_d = "Formula priority penalty"

    strings_formula_table = ('Quantity [mL]', 'Formula', 'Bottles needed')
    strings_solution_table = ('Quantity [mL]', 'Solution', 'Bottles needed')

    string_volume = "Total volume"
    string_nutrient_results = "Nutritional values obtained:"

    # Menu bar related strings
    string_about = "NutriOptiMix project is licensed with GNU GPL v3.0.\nSource code can be found on GitHub."