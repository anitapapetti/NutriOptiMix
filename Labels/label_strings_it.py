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

# Label strings in Italian

class ItalianLabels:
    # make all fields of this class read-only
    __slots__ = ()

    # Main window's strings
    string_params_directions = "Inserire i parametri di calcolo:"
    string_Mmax = "N° max di miscele"
    string_Cmax = "N° max di soluzioni"
    string_Vmin = "Volume minimo di ogni miscela/soluzione"
    string_Vmin_unit = "mL"
    string_Smax = "Massimo spreco totale di miscela tollerato"
    string_Smax_unit = "mL"
    string_Dmax = "Max penalità per uso di miscele meno prioritarie"

    string_directions = "Inserire i valori obiettivo per i nutrienti:*"

    string_nutrients_energy = "Energia"
    string_nutrients_energy_unit = "kcal"
    string_nutrients = [
        "Proteine", "Lipidi", "Glucidi",
        "Na", "K", "Ca",
        "Mg", "P", "Fe"
    ]
    string_nutrients_unit = [
        "g", "g", "g",
        "mg", "mg", "mg",
        "mg", "mg", "mg"
    ]
    string_nutrients_weight = "Peso"

    string_submit_button = "Calcola mix"
    string_reset_nutrients = "Cancella valori nutrienti"
    string_reset_weights = "Resetta tutti i pesi"

    string_notes = "* valori obiettivo <= 0 o non definiti saranno ignorati. L'energia è calcolata in automatico e dipende da glucidi, lipidi e proteine."

    string_precompile = "[Opzionale] Precompila i campi con i valori nutrizionali per una vita sedentaria:"
    string_precompile_button = "Inserisci dati paziente"

    # Precompile popup window's strings
    string_precompile_window_title = "Inserisci dati paziente"
    string_precompile_window_info = "Inserisci i dati del paziente:"
    string_precompile_window_fields = [
        "Peso", "Altezza", "Età"
    ]
    string_precompile_window_fields_unit = [
        "kg", "cm", "anni"
    ]
    string_precompile_window_gender = "Sesso"
    string_precompile_window_button = "Calcola valori nutrizionali*"

    string_precompile_footnote = "* il peso dev'essere fra {w_min} e {w_max} {w_unit}\nl'altezza dev'essere fra {h_min} e {h_max} {h_unit}\nl'età dev'essere fra {a_min} e {a_max_actual} {a_unit}\n(L'accuratezza diminuisce per età superiori a {a_max} {a_unit})"

    # After precompile
    string_patient_button = string_precompile_window_button

    # After solve
    string_results_title = "RISULTATI"

    string_objectives = "Valori obiettivo:"
    # string_delta = chr(948)   # greek letter delta
    string_delta = "Max deviazione dall'obiettivo"
    string_s = "Spreco totale di miscela"
    string_s_unit = "mL"
    string_d = "Penalità per priorità miscele"

    strings_formula_table = ('Quantità [mL]', 'Miscela', 'Flaconi necessari')
    strings_solution_table = ('Quantità [mL]', 'Soluzione', 'Flaconi necessari')

    string_volume = "Volume totale"
    string_nutrient_results = "Valori nutritivi ottenuti:"

    # Menu bar related strings
    string_about = "Il progetto NutriOptiMix è distribuito sotto licenza GNU GPL v3.0.\nIl codice sorgente si può trovare su GitHub."