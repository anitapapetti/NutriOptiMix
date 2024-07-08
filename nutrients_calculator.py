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


# Calculate patient's nutrient requirements per day

# Define Harris-Benedict equations revised by Roza and Shizgal in 1984
# source: https://en.wikipedia.org/wiki/Harris%E2%80%93Benedict_equation
# does not necessarily apply to underweight or obese patients
def harris_benedict_1984(weight, height, age, gender):
    bmr = 0
    if gender == "M":
        bmr = (13.397 * weight) + (4.799 * height) - (5.677 * age) + 88.362
    elif gender == "F":
        bmr = (9.247 * weight) + (3.098 * height) - (4.330 * age) + 447.593
    else:
        "Gender for Harris-Benedict equations must be either M or F"
        exit(1)
    return bmr


# Define Harris-Benedict equations revised by Pavlidou in 2023
# source: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9967803/
# more accurate for modern Western Caucasian people (more overweight than 1984 people)
# weight between 43 and 157 kg
# height between 148 and 203 cm
# age between 18 and 78 years
# BMI between 17 and 48 kg/m^2
def harris_benedict_2023(weight, height, age, gender):
    bmr = 0
    if gender == "M":
        bmr = (9.65 * weight) + (5.73 * height) - (5.08 * age) + 260
    elif gender == "F":
        bmr = (7.38 * weight) + (6.07 * height) - (2.31 * age) + 43
    else:
        "Gender for Harris-Benedict equations must be either M or F"
        exit(1)
    return bmr


# Calculate nutrients from patient's data with Harris-Benedict equations
def calculate_nutrients(weight, height, age, gender):
    # cast numbers to float type
    weight = float(weight)
    height = float(height)
    age = float(age)

    # calculate non protein-based energy in kcal
    # using Harris–Benedict equations
    bmr = harris_benedict_2023(weight, height, age, gender)
    # bmr = harris_benedict_1984(weight, height, age, gender)
    non_protein_energy = bmr * 1.2      # patient recuperating in bed all day (source: https://www.omnicalculator.com/it/salute/bmr-equazione-harris-benedict#:~:text=Utilizzare%20l'equazione%20di%20Harris,dispendio%20energetico%20totale%20giornaliero%20%E2%80%94%20DET)

    # calculate carbohydrates and lipids
    carbo = 0.65 * non_protein_energy / 4.0         # carbohydrates in g
    fat = 0.35 * non_protein_energy / 9.0           # fat in g

    # calculate protein and total energy
    protein = weight * 1.3                          # protein in g
                                                    # source: https://www.espen.org/files/ESPEN-Guidelines/ESPEN_practical_and_partially_revised_guideline_Clinical_nutrition_in_the_intensive_care_unit.pdf (2023,recommendation 25)
    energy = non_protein_energy + protein * 4.0     # energy in kcal

    # set electrolytes 
    # values are not strictly equal to a healthy person's required amount per day, as in intensive care pt's electrolytes are measured 2-3 times a day and integrated as needed
    na = 2000.0       # sodium in mg        # between 500 and 2400 mg, source: https://www.ncbi.nlm.nih.gov/books/NBK234935/
    k = 3500.0        # potassium in mg     # source: https://www.ncbi.nlm.nih.gov/books/NBK234935/
    ca = 800.0        # calcium in mg
    mg = 3750.0       # magnesium in mg
    p = 800.0         # phosphorus in mg
    fe = 14.0         # iron in mg          # should be between 18 and 30 mg, source: https://www.espen.org/files/ESPEN-Guidelines/ESPEN_micronutrient_guideline.pdf  # (before: 14 mg)

    return [energy, protein, fat, carbo, na, k, ca, mg, p, fe]