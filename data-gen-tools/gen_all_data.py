##############################################################################
################################### Import ###################################
##############################################################################
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import linregress
import copy
import json
import prompt_gen_tools as pg

np.random.seed(19960806)

##############################################################################
#################################### Vars ####################################
##############################################################################
all_nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

### Upper an lower bounds for integration ###
lbs = [-np.inf, -10, -1, 0]
ubs = [np.inf, 0, 1, 10]
specific_bounds = lbs + ubs

### Basic expressions with no variables ###
basic_bodies    = pg.gen_ops(100, bodies=all_nums, ops=['+','-'], op_num=[0,2], add_constant=False)
basic_exps      = pg.gen_exp(100, bodies=all_nums, muls=[1,9], exps=[0,4])
basic_fracs     = pg.gen_div(100, bodies=all_nums)
basic_fracs_v2  = pg.gen_div(100, bodies=basic_bodies)
basic_trig      = pg.gen_trig(100, bodies=basic_fracs, funcs=['sin', 'cos', 'tan'], include_pi=True)
basic_trig_v2   = pg.gen_trig(100, bodies=basic_fracs, funcs=['sin', 'cos', 'tan', 'cot', 'sec', 'csc'], include_pi=True)
basic_log       = pg.gen_log(100, bodies=all_nums, bases=['10', '2', 'e'], include_con=False)
basic_log_v2    = pg.gen_log(100, bodies=basic_fracs, bases=['10', '2', 'e'], include_con=False)

### Simple expressions of one variable ###
simple_bodies_var1 = pg.gen_exp(n=1000, bodies=['x'], muls=[1,9], exps=[1,2])
simple_bodies_var1 = pg.gen_ops(100, bodies=simple_bodies_var1, ops=['+','-'], op_num=[1,2])

### Simple expressions of two variable ###
b1 = pg.gen_exp(n=1000, bodies=['x'], muls=[1,9], exps=[1,2])
b2 = pg.gen_exp(n=1000, bodies=['y'], muls=[1,9], exps=[1,2])
simple_bodies_var2 = pg.combine_bodies(b1, b2, ops=['+','-'])
simple_bodies_var2 = pg.gen_ops(100, bodies=simple_bodies_var2, ops=['+','-'], op_num=[0,0])

### Simple expressions of three variable ###
b1 = pg.gen_exp(n=1000, bodies=['x'], muls=[1,9], exps=[1,2])
b2 = pg.gen_exp(n=1000, bodies=['y'], muls=[1,9], exps=[1,2])
b3 = pg.gen_exp(n=1000, bodies=['z'], muls=[1,9], exps=[1,2])
simple_bodies_var3 = pg.combine_bodies(b1, b2, ops=['+','-'])
simple_bodies_var3 = pg.combine_bodies(simple_bodies_var3, b3, ops=['+','-'])
simple_bodies_var3 = pg.gen_ops(100, bodies=simple_bodies_var3, ops=['+','-'], op_num=[0,0])

### More complex expressions of one variable ###
bodies = pg.gen_exp(100, exps=[1,5])
bodies = pg.gen_ops(100, bodies=bodies, ops=['+','-'], op_num=[1,1], add_constant=True)
bodies = pg.gen_div(100, bodies=bodies, p=0.1)
bodies = pg.gen_ops(100, bodies=bodies, ops=['+','-'], op_num=[1,1], add_constant=True)
print(bodies)

### More complex expressions of one variable mixed to create expressions of two and three vars ###
bodies_y = copy.deepcopy(bodies)
for i in range(len(bodies_y)):
    bodies_y[i] = bodies_y[i].replace('x', 'y')
np.random.shuffle( bodies_y )
bodies_z = copy.deepcopy(bodies)
for i in range(len(bodies_z)):
    bodies_z[i] = bodies_z[i].replace('x', 'z')
np.random.shuffle( bodies_z )
    
bodies_var2 = pg.combine_bodies(bodies, bodies_y, ops=['+','-'])
bodies_var3 = pg.combine_bodies(bodies_var2, bodies_z, ops=['+','-'])

##############################################################################
################################## Prompts ###################################
##############################################################################
### Single integral prompts ###
ints = pg.gen_integral(10, bodies=bodies, bound_range=[-100,100], specific_bounds=[-np.inf, 0, np.inf, 1], p=0.2)
for i in ints:
    print(i)

### Derivative prompts ###
devs  = pg.gen_derivative(10, bodies=bodies)
devs2 = pg.gen_2nd_derivative(10, bodies=bodies)
devs3 = pg.gen_3rd_derivative(10, bodies=bodies)
for d in devs:
    print(d)
for d in devs2:
    print(d)
for d in devs3:
    print(d)
    
devs_var2  = pg.gen_derivative(10, bodies=simple_bodies_var2)
devs2_var2 = pg.gen_2nd_derivative(10, bodies=simple_bodies_var2)
devs3_var2 = pg.gen_3rd_derivative(10, bodies=simple_bodies_var2)

devs_var3  = pg.gen_derivative(10, bodies=simple_bodies_var3)
devs2_var3 = pg.gen_2nd_derivative(10, bodies=simple_bodies_var3)
devs3_var3 = pg.gen_3rd_derivative(10, bodies=simple_bodies_var3)

### System of equation prompts ###
eq1 = pg.eq_solve(10, bodies=simple_bodies_var1, num_vars=1)
for d in eq1:
    print(d)
    
eq2 = pg.eq_solve(10, bodies=simple_bodies_var2, num_vars=2)
for d in eq2:
    print(d)
    
eq3 = pg.eq_solve(10, bodies=simple_bodies_var3, num_vars=3)
for d in eq3:
    print(d)



##############################################################################
#################################### Main ####################################
##############################################################################
### Save Vars ###
dir_save = './annotations/'
elem_fn    = 'elementary_math.json'
algebra_fn = 'algebra.json'
calc_12_fn = 'calc_basic.json'


### Save Calc 1&2 ###
calc_12 = {'annotations':[]}
for p in devs:
    calc_12['annotations'].append({'prompt':p, 'type':'derivative'})
for p in ints:
    calc_12['annotations'].append({'prompt':p, 'type':'integral'})
calc_12_obj = json.dumps(calc_12, indent=4)
with open(dir_save+calc_12_fn, "w") as outfile:
    outfile.write(calc_12_obj)