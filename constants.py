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


# Constants
# Define constants for model input
DEFAULT_MMAX = 5
DEFAULT_CMAX = 5
DEFAULT_VMIN = 10        # mL
DEFAULT_WEIGHTS = ["1.0", "1.0", "1.0", "1.0", "0.1", "0.1", "0.1", "0.1", "0.1", "0.1"]

# Define constants for model input's validation
VALID_WEIGHTS = ["0.0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0"]

# Define constants for patients data ranges to calculate nutrients
WEIGHT_MIN = 43         # kg
WEIGHT_MAX = 157        # kg
HEIGHT_MIN = 148        # cm
HEIGHT_MAX = 203        # cm
AGE_MIN = 18            # years
AGE_MAX = 78            # years
AGE_MAX_ACTUAL = 110    # years


# User's settings
LANG = "en"     # app's languange expressed in format ISO 639 set 1 (two letters) source: https://www.loc.gov/standards/iso639-2/php/English_list.php


# Define labels
match LANG:
    case "en":
        from Labels.label_strings_en import EnglishLabels as Labels
    case "it":
        from Labels.label_strings_it import ItalianLabels as Labels
    case _:
        from Labels.label_strings_en import EnglishLabels as Labels
LABELS = Labels()       # define labels namespace