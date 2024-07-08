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


import pandas as pd
from mip import *

class MixCalculator():
    def __init__(self, Mmax=5, Cmax=5, Vmin=1, Smax=3000, Dmax=3000):
        self.create_data(Mmax, Cmax, Vmin, Smax, Dmax)
        self.create_model()
    

    # Set target and solve
    def solve(self, user_nutrients, user_weights):
        self.set_target(user_nutrients, user_weights)
        self.model.optimize()
        self.get_results()
        
        return self.objectives, self.M_used, self.C_used, self.formulas, self.solutions, self.nutrients, self.total_volume


    # Declare data that will be used by the model
    def create_data(self, Mmax, Cmax, Vmin, Smax, Dmax):

        ## Constants

        self.Mmax = Mmax                # Max number of formulas to use
        self.Cmax = Cmax                # Max number of solutions to use
        self.Vmin = Vmin                # Min formula volume to use [ml]
        self.Smax = Smax                # Max total waste tolerated
        self.Dmax = Dmax                # Max penalty for use of lower priority formulas
        self.b_default = 500         # Default bottle volume [ml]
        self.fmax_default = 10       # Default number of available bottles
        self.p_default = 1           # Default priority level for formulas
        # self.okLactose = True        # True if there are no concerns about lactose in mix

        # TODO: insert f_max values in db instead of using arbitrary constant

        # Checks
        assert self.Mmax >= 0, "Mmax should be non-negative"
        assert self.Cmax >= 0, "Cmax should be non-negative"
        assert self.Vmin >= 0, "Vmin should be non-negative"
        assert self.b_default > 0, "Bottle volume default value should be positive"
        assert self.fmax_default >= 0, "Default number of available bottles should be non-negative"
        assert self.p_default > 0, "Default formula priority level should be positive"


        ## Formulas

        # import formulas data from csv (nutrient values per 100ml)
        df = pd.read_csv('Database/prodotti_new_pesati.csv',
                        encoding='utf-8',
                        usecols=['Nome Prodotto',
        #                          'Note',
        #                          'Prezzo',
                                'Volume',
                                'Peso',
                                'Kcal',
        #                          'mOsm/L',
        #                          'Acqua (ml)',
        #                          'P/L/C (%)',
                                'Prot. gr.',
                                'Lipidi gr.',
        #                          'MCT',
        #                          'LCT',
                                'Carbo gr. ',
        #                          'EPA DHA (g)',
        #                          'Latt.',
        #                          'Fibra PHGG',
                                'Na (mg)',
                                'K (mg)',
                                'Ca (mg)',
                                'Mg (mg)',
                                'P (mg)',
                                'Fe (mg)'
                                ]
                        )

        # column names cleaning
        df.columns = [c.lower().split(' ', 1)[0] for c in df.columns]
        df.rename(columns={'latt.': 'lactose'}, inplace=True)

        # manage lactose
        # if not okLactose:
        #     if 'lactose' in df.columns:
        #         df.lactose = df.lactose.str.lower()
        #         df.lactose = df.lactose.fillna(True)  # with no data, assume formula may contain lactose
        #         df.loc[df['lactose'] == 'no', 'lactose'] = False
        #         df.loc[df['lactose'] == 'sì', 'lactose'] = True
        #         df.loc[(df['lactose'] != False) & (df['lactose'] != True), 'lactose'] = True
        #         df = df[(df.lactose == False)]        # keep lactose-free formulas only
        #     else:
        #         print("Warning: Missing data about lactose in formulas. Continued solving with all formulas\n")


        # save formula names and number of formulas
        self.formula_names = [str(n) for n in df.nome]
        self.nFormulas = len(self.formula_names)

        # filter data and manage na
        df = df.select_dtypes(include='number')
        df.volume = df.volume.fillna(self.b_default)
        df.peso = df.peso.fillna(self.p_default)
        df = df.fillna(0)

        # extract bottle volumes into parameter b (only formulas' for now)
        self.b = [float(v) for v in df.volume]
        df.drop('volume', axis=1, inplace=True)

        # extract formula priority levels into parameter p
        self.p = [float(r) for r in df.peso]
        df.drop('peso', axis=1, inplace=True)

        ########## TO FORCE A PRIORITIZATION FOR TESTING: #################
        self.p[13] = 0.5
        self.p[9] = 0.8
        self.p[15] = 0.9
        ###################################################################

        # put max number of bottles available in parameter fmax (only formulas' for now)
        self.fmax = [int(self.fmax_default) for i in range(self.nFormulas)]

        # save nutrient values per 100ml (df data) in parameter a (only formulas' for now)
        self.a = []
        for i in range(self.nFormulas):   
            row = df.iloc[[i]].values[0][0:]                                # row = list of values in row i (pandas type)
            row_string = str(row)[1:-1]                                     # row_string = str row without external []
            row_string = row_string.replace("\n", "")                       # cleaning row_string
            nutrient_values_strings = row_string.strip().split()             
            nutrient_values = [float(x) for x in nutrient_values_strings]
            self.a.append(nutrient_values)

        # save the number of nutrients found in db
        self.nNutrients = len(df.columns)


        ## Solutions

        # import solutions data from csv (nutrient values per 100ml)
        # IMPORTANT: COLUMNS USED FOR PARAMETER A AND THE ORDER IN WHICH THEY ARE IMPORTED MUST BE THE SAME AS FORMULAS'
        df_s = pd.read_csv('Database/miscele_povere.csv',
                        encoding='utf-8',
                        usecols=['Nome',
                                'Volume flacone',
                                'Kcal',
        #                          'mOsm/L',
        #                          'Acqua (ml)',
                                'Prot. gr.',
                                'Lipidi gr.',
                                'Carbo gr. ',
                                'Na (mg)',
                                'K (mg)',
                                'Ca (mg)',
                                'Mg (mg)',
                                'P (mg)',
                                'Fe (mg)'
                                ]
                        )
        # column names cleaning
        df_s.columns = [c.lower().split(' ', 1)[0] for c in df_s.columns]

        # save solutions names and number of solutions
        self.solution_names = [str(n) for n in df_s.nome]
        self.nSolutions = len(self.solution_names)

        # filter data and manage na
        df_s = df_s.select_dtypes(include='number')
        df_s.volume = df_s.volume.fillna(self.b_default)
        df_s = df_s.fillna(0)

        # extract bottle volumes column and append to parameter b
        for v in df_s.volume:
            self.b.append(float(v))
        df_s.drop('volume', axis=1, inplace=True)

        # append solutions' max number of bottles available to parameter fmax
        for i in range(self.nSolutions):
            self.fmax.append(int(self.fmax_default))

        # check that the number of nutrients in df_s is the same as in df
        assert len(df_s.columns) == self.nNutrients, "Number of nutrients in formulas' db must be the same as in solutions' db"

        # append solutions' nutrient values per 100ml to parameter a
        for i in range(self.nSolutions):   
            row = df_s.iloc[[i]].values[0][0:]                              # row = list of values in row i (pandas type)
            row_string = str(row)[1:-1]                                     # row_string = str row without external []
            row_string = row_string.replace("\n", "")                       # cleaning row_string
            nutrient_values_strings = row_string.strip().split()             
            nutrient_values = [float(x) for x in nutrient_values_strings]
            self.a.append(nutrient_values)

        ## Sets
        self.M = set(range(self.nFormulas))
        self.C = set(range(self.nFormulas, self.nFormulas + self.nSolutions))
        self.N = set(range(self.nNutrients))

        # Vmin values for each formula/solution (the lowest between parameter Vmin and bottle's volume)
        self.Vmin_list = []
        for i in self.M.union(self.C):
            if Vmin < self.b[i]:
                self.Vmin_list.append(Vmin)
            else:
                self.Vmin_list.append(self.b[i])

        ## Prints to check data
        # print("DATA checks")
        # print("nFormulas = " + str(nFormulas) + ", set of " + str(M))
        # print("nSolutions = " + str(nSolutions) + ", set of " + str(C))
        # print("nFormulas + nSolutions = " + str(nFormulas + nSolutions) + ", set of " + str(M.union(C)))
        # print("nNutrients = " + str(nNutrients) + ", set of " + str(N))
        # print("b = " + str(b))
        # print("b len = " + str(len(b)))
        # print("fmax = " + str(fmax))
        # print("fmax len = " + str(len(fmax)))
        # print("p = " + str(p))
        # print("p len = " + str(len(p)))
        # print("a = ")
        # for i in M.union(C):
        #     print(str(a[i]))
        # print("a = matrix " + str(len(a)) + " x " + str(len(a[0])))
        # print("o = " + str(o))
        # print("o len = " + str(len(o)))
        # print("w = " + str(w))
        # print("w len = " + str(len(w)))
        # print("Target indexes = " + str(target_indexes))
        # print("target indexes len = " + str(len(target_indexes)))


    # Declare MIP model
    def create_model(self):

        self.model = Model(sense=MINIMIZE, solver_name=CBC)

        ##### VARIABLES #####

        # var x = used volume of formula or solution [ml]
        x = [self.model.add_var(name='x({})'.format(i), lb=0.0) for i in self.M.union(self.C)]

        # var y = 1 if and only if the formula or solution is used
        y = [self.model.add_var(var_type=BINARY) for i in self.M.union(self.C)]

        # var f = number of bottles opened for the mix
        f = [self.model.add_var(name='f({})'.format(i), var_type=INTEGER, lb=0) for i in self.M.union(self.C)]

        # var delta = max of % deviations between target and obtained nutrient value
        delta = self.model.add_var(name="delta", lb=0.0)

        # var s = total waste of formula
        s = self.model.add_var(name="s", lb=0.0)

        # var d = penalty due to used formulas' priority levels
        d = self.model.add_var(name="d", lb=0.0)

        # var n = obtained nutrient values
        n = [self.model.add_var(name='n({})'.format(j), lb=0.0) for j in self.N]

        # var V = total mix volume [ml]
        V = self.model.add_var(name="V", lb=0.0)


        ##### OBJECTIVE #####

        self.model.objective = minimize(delta)
        # model.objective = minimize(delta + 0.1*s + 0.0001*d)


        ##### CONSTRAINTS #####

        # For each formula or solution, the number of bottles opened must be between one and the maximum number of bottles available if the formula or solution is used in the mix, zero otherwise.
        for i in self.M.union(self.C):
            self.model += f[i] >= y[i]
            self.model += f[i] <= y[i] * self.fmax[i]

        # For each formula or solution, the number of bottles opened for the mix must be the minimum necessary to provide the requested quantity
        for i in self.M.union(self.C):
            self.model += x[i] <= self.b[i] * f[i]
            # self.model += x[i] >= self.b[i] * (f[i]-1)    # redundant because of Vmin constraint

        # The maximum number of formulas to use in the mix is limited by the given constant Mmax
        self.model += xsum(y[t] for t in self.M) <= self.Mmax

        # The maximum number of solutions to use in the mix is limited by the given constant Cmax
        self.model += xsum(y[c] for c in self.C) <= self.Cmax

        # To avoid costly waste, a bottle of formula or solution is used only if the requested quantity is greater or equal than the given minimum volume Vmin
        for i in self.M.union(self.C):
            self.model += x[i] >= self.Vmin_list[i] + (f[i]-1) * self.b[i]

        # The nutrient values of the mix are calculated and stored in variables n_j
        for j in self.N:
            self.model += n[j] == xsum(self.a[i][j] * 0.01 * x[i] for i in self.M.union(self.C))
        
        # Mix volume is calculated and stored in variable V
        self.model += V == xsum(x[i] for i in self.M.union(self.C))


        # Define s as the total waste of formula, calculating it as the sum of the remainders of each used formula
        self.model += s == xsum(self.b[t] * f[t] - x[t] for t in self.M)

        # Define d as a penalty, dependent on the priority of formulas used in the mix
        self.model += d == xsum((1 - self.p[t]) * x[t] for t in self.M)
        # self.model += d == xsum(x[t]/self.p[t] for t in self.M)

        
        # Secondary objective: minimize formula waste
        # Limit total waste of formula by parameter Smax (set by the user)
        self.model += s <= self.Smax

        # Secondary objective: follow formula priorirty (minimize formula priority penalty)
        # Limit penalty by parameter Dmax (set by the user)
        self.model += d <= self.Dmax


    # Set model's target nutrients values and weights
    # Define delta in model
    def set_target(self, user_o, user_w):
        # user_o : target nutrients' values received from user input
        # if user_o[i] <= 0 then nutrient i is not a target
        # 0 -> kcal    1 -> prot.    2 -> lipidi    3 -> carbo    4 -> na    
        # 5 -> k    6 -> ca    7 -> mg    8 -> p    9 -> fe

        # user_w : nutrients' nutritional importance received from user input
        # must be between 0.0 and 1.0 included

        # check number of nutrients and weights received is ok and consistent with db data
        for w in user_w:
            assert float(w) >= 0.0 and float(w) <= 1.0, "Target weight must be between 0 and 1 (included)" 
        assert len(user_o) == self.nNutrients, "Possible target nutrients must number the same as nutrients in db"
        assert len(user_w) == self.nNutrients, "Possible target nutrients' weights must number the same as nutrients in db"

        # put target nutrients' values or zero into parameter o
        # put target nutrients' indexes in parameter target_indexes
        o = []
        target_indexes = []
        for i, value in enumerate(user_o):
            if float(value) > 0.0:
                o.append(float(value))
                target_indexes.append(i)
            else:
                o.append(float(0))

        # check user_w's values and put target nutrients' weights into parameter w
        w = []
        for weight in user_w:
            if float(weight) < 0.0:
                w.append(float(0.0))
            elif float(weight) > 1.0:
                w.append(float(1.0))
            else: 
                w.append(float(weight))
        
        # add target indexes set to model 
        self.O = set(target_indexes)

        # Define delta as the maximum percentage deviation between each nutrient’s target and obtained value, weighted by that nutrient’s nutritional importance
        for k in self.O:
            self.model += self.model.var_by_name("delta") >= w[k] * (self.model.var_by_name("n({})".format(k))/o[k] - 1)
            self.model += self.model.var_by_name("delta") >= w[k] * (- self.model.var_by_name("n({})".format(k))/o[k] + 1)


    # Print results on stdout
    def print_results(self):
        if(self.M_used == None):
            self.get_results()
        # print(f"Valore obiettivo = {self.model.objective_value:.{6}}")
        print(f"delta = {self.model.var_by_name('delta').x:.6f}")
        print(f"s = {round(self.model.var_by_name('s').x)} mL")
        print(f"d = {round(self.model.var_by_name('d').x)}")

        print("Formulas used: ", self.M_used)
        print("Solutions used: ", self.C_used)

        for component in self.formulas:
            print(f"Used {component[0]:.0f} mL of formula {component[1]} ({component[2]:.0f} bottles x {component[3]:.0f} mL)")
        
        for component in self.solutions:
            print(f"Used {component[0]:.0f} mL of solution {component[1]} ({component[2]:.0f} bottles x {component[3]:.0f} mL)")

        print("Nutrients obtained: ", self.nutrients)
        print(f"Nutrients obtained: energy = {round(self.nutrients[0],1)} kcal, protein = {round(self.nutrients[1], 1)} g, fat = {round(self.nutrients[2], 1)} g, carbs = {round(self.nutrients[3], 1)}, Na = {round(self.nutrients[4])} mg, K = {round(self.nutrients[5])} mg, Ca = {round(self.nutrients[6])} mg, Mg = {round(self.nutrients[7])} mg, P = {round(self.nutrients[8])} mg, Fe = {round(self.nutrients[9])} mg\n")

        

    # Extract results from after-solve model's variables
    def get_results(self):
        self.objectives = [self.model.var_by_name('delta').x, self.model.var_by_name('s').x, self.model.var_by_name('d').x]
        
        self.M_used = 0
        self.C_used = 0
        self.formulas = []
        self.solutions = []
        for i in range(self.nFormulas + self.nSolutions):
            quantity = self.model.var_by_name("x({})".format(i)).x
            name = ""
            number = self.model.var_by_name("f({})".format(i)).x
            # print(i, f[i].x, y[i].x, x[i].x)
            if quantity > 0:
                if i < self.nFormulas:
                    name = self.formula_names[i]
                    self.M_used += 1
                    component = (quantity, name, number, self.b[i])
                    self.formulas.append(component)
                else:
                    name = self.solution_names[i-self.nFormulas]
                    self.C_used += 1
                    component = (quantity, name, number, self.b[i])
                    self.solutions.append(component) 
        
        self.nutrients = [self.model.var_by_name('n({})'.format(i)).x for i in self.N]
        self.total_volume = self.model.var_by_name('V').x