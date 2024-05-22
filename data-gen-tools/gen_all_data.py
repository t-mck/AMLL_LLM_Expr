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
all_nums_20 = np.arange(1,21,1).astype(str)
all_nums_99 = np.arange(1,100,1).astype(str)
nb_vals = 1000
np_vals = 10
out_p   = 100 

### Upper an lower bounds for integration ###
lbs = [-np.inf, -10, -1, 0]
ubs = [np.inf, 0, 1, 10]
specific_bounds = lbs + ubs

### Basic expressions with no variables ###
basic_bodies        = pg.gen_ops(nb_vals, bodies=all_nums, ops=['+','-'], op_num=[0,2], add_constant=False)
basic_bodies_mul    = pg.gen_ops(nb_vals, bodies=all_nums, ops=['+','-','*'], op_num=[0,2], add_constant=False)
basic_bodies_mul_20 = pg.gen_ops(nb_vals, bodies=all_nums_20, ops=['+','-','*'], op_num=[0,2], add_constant=False)
basic_exps          = pg.gen_exp(nb_vals, bodies=all_nums, muls=[1,9], exps=[0,4])
basic_fracs         = pg.gen_div(nb_vals, bodies=all_nums)
basic_fracs_99      = pg.gen_div(nb_vals, bodies=all_nums_99)
basic_fracs_v2      = pg.gen_div(nb_vals, bodies=basic_bodies)
basic_trig          = pg.gen_trig(nb_vals, bodies=basic_fracs, funcs=['sin', 'cos', 'tan'], include_pi=True)
basic_trig_v2       = pg.gen_trig(nb_vals, bodies=basic_fracs, funcs=['sin', 'cos', 'tan', 'cot', 'sec', 'csc'], include_pi=True)
basic_log           = pg.gen_log(nb_vals, bodies=all_nums, bases=['10', '2', 'e'], include_con=False)
basic_log_v2        = pg.gen_log(nb_vals, bodies=basic_fracs, bases=['10', '2', 'e'], include_con=False)

### Simple expressions of one variable ###
simple_bodies_var1 = pg.gen_exp(n=nb_vals, bodies=['x'], muls=[1,9], exps=[1,2])
simple_bodies_var1 = pg.gen_ops(n=nb_vals, bodies=simple_bodies_var1, ops=['+','-'], op_num=[1,2])
simple_factor_bodies_p1_var1 = pg.gen_exp(n=nb_vals, bodies=['x'], muls=[1,9], exps=[1,2])
simple_factor_bodies_p2_var1 = pg.gen_exp(n=nb_vals, bodies=['x'], muls=[1,9], exps=[2,3])
simple_factor_bodies_var1 = pg.combine_bodies(simple_factor_bodies_p1_var1, simple_factor_bodies_p2_var1, ops=['+','-'], include_con=True)


### Simple expressions of two variable ###
b1 = pg.gen_exp(n=nb_vals, bodies=['x'], muls=[1,9], exps=[1,2])
b2 = pg.gen_exp(n=nb_vals, bodies=['y'], muls=[1,9], exps=[1,2])
simple_bodies_var2 = pg.combine_bodies(b1, b2, ops=['+','-'])
simple_bodies_var2 = pg.gen_ops(nb_vals, bodies=simple_bodies_var2, ops=['+','-'], op_num=[0,0])

### Simple expressions of three variable ###
b1 = pg.gen_exp(n=nb_vals, bodies=['x'], muls=[1,9], exps=[1,2])
b2 = pg.gen_exp(n=nb_vals, bodies=['y'], muls=[1,9], exps=[1,2])
b3 = pg.gen_exp(n=nb_vals, bodies=['z'], muls=[1,9], exps=[1,2])
simple_bodies_var3 = pg.combine_bodies(b1, b2, ops=['+','-'])
simple_bodies_var3 = pg.combine_bodies(simple_bodies_var3, b3, ops=['+','-'])
simple_bodies_var3 = pg.gen_ops(nb_vals, bodies=simple_bodies_var3, ops=['+','-'], op_num=[0,0])

### More complex expressions of one variable ###
bodies = pg.gen_exp(nb_vals, exps=[1,4])
bodies = pg.gen_ops(nb_vals, bodies=bodies, ops=['+','-'], op_num=[1,1], add_constant=True)
#bodies = pg.gen_div(nb_vals, bodies=bodies, p=0.1)
#bodies = pg.gen_ops(nb_vals, bodies=bodies, ops=['+','-'], op_num=[1,1])
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

### Elementary Math ##########################################################
simple_math_prompts = []
for p in basic_bodies_mul_20:
    if(len(p) > 2):
        simple_math_prompts.append('Find '+p)
    if(len(simple_math_prompts) >= np_vals):
        break

simple_frac_prompts = []
for p in basic_fracs_99:
    simple_frac_prompts.append('Simplify the fraction '+p.replace('(','').replace(')',''))
    if(len(simple_frac_prompts) >= np_vals):
        break
##############################################################################
        
    
### Algebra ##################################################################
simple_alg_prompts = []
for i in range(len( bodies )):
    p1, p2 = bodies[i*2], bodies[i*2+1]
    simple_alg_prompts.append('Solve for x %s = %s'%(p1,p2))
    if(len(simple_alg_prompts) >= np_vals):
        break
    
simple_factor_prompts = []
for i in range(len( simple_factor_bodies_var1 )):
    p = simple_factor_bodies_var1[i]
    simple_factor_prompts.append('Factor %s'%(p))
    if(len(simple_factor_prompts) >= np_vals):
        break
    
simple_sys_eq_prompts = []
for i in range(len( simple_bodies_var3 )):
    p1 = (simple_bodies_var3[i*3][:-3] + '= %s'%(simple_bodies_var3[i*3][-3:].replace(' ','').replace('+',''))).replace('*','').replace('^1','')
    p2 = (simple_bodies_var3[i*3+1][:-3] + '= %s'%(simple_bodies_var3[i*3+1][-3:].replace(' ','').replace('+',''))).replace('*','').replace('^1','')
    p3 = (simple_bodies_var3[i*3+2][:-3] + '= %s'%(simple_bodies_var3[i*3+2][-3:].replace(' ','').replace('+',''))).replace('*','').replace('^1','')
    simple_sys_eq_prompts.append('%s, %s, %s'%(p1,p2,p3))
    if(len(simple_sys_eq_prompts) >= np_vals):
        break

##############################################################################
    

### Save Calc 1&2 ############################################################
### Single integral prompts ###
ints = pg.gen_integral(np_vals, bodies=bodies, bound_range=[-100,100], specific_bounds=[-np.inf, 0, np.inf, 1], p=0.2)
for i in ints:
    print(i)

### Derivative prompts ###
devs  = pg.gen_derivative(np_vals, bodies=bodies)
devs2 = pg.gen_2nd_derivative(np_vals, bodies=bodies)
devs3 = pg.gen_3rd_derivative(np_vals, bodies=bodies)
for d in devs:
    print(d)
for d in devs2:
    print(d)
for d in devs3:
    print(d)
    
devs_var2  = pg.gen_derivative(np_vals, bodies=simple_bodies_var2)
devs2_var2 = pg.gen_2nd_derivative(np_vals, bodies=simple_bodies_var2)
devs3_var2 = pg.gen_3rd_derivative(np_vals, bodies=simple_bodies_var2)

devs_var3  = pg.gen_derivative(np_vals, bodies=simple_bodies_var3)
devs2_var3 = pg.gen_2nd_derivative(np_vals, bodies=simple_bodies_var3)
devs3_var3 = pg.gen_3rd_derivative(np_vals, bodies=simple_bodies_var3)

### System of equation prompts ###
eq1 = pg.eq_solve(np_vals, bodies=simple_bodies_var1, num_vars=1)
for d in eq1:
    print(d)
    
eq2 = pg.eq_solve(np_vals, bodies=simple_bodies_var2, num_vars=2)
for d in eq2:
    print(d)
    
eq3 = pg.eq_solve(np_vals, bodies=simple_bodies_var3, num_vars=3)
for d in eq3:
    print(d)
##############################################################################



##############################################################################
#################################### Main ####################################
##############################################################################
### Save Vars ###
dir_save = '/home/francesco/Documents/Projects/Research_ass/AMLL_LLM_Expr/data-gen-tools/annotations/'
elem_fn    = 'elementary_math.json'
algebra_fn = 'algebra.json'
calc_12_fn = 'calc_basic.json'

### Save Elementary Math ###
out = {'annotations':[]}
out['prompt types'] = ['simple operations', 'fractions']
for p in simple_math_prompts:
    out['annotations'].append({'prompt':p, 'type':'simple operations'})
for p in simple_frac_prompts:
    out['annotations'].append({'prompt':p, 'type':'fractions'})
out_obj = json.dumps(out, indent=4)
#with open(dir_save+elem_fn, "w") as outfile:
#    outfile.write(out_obj)

### Save Algebra ###
out = {'annotations':[]}
out['prompt types'] = ['Solve for x', 'Factor eq', 'Solve system of three equations']
for p in simple_alg_prompts:
    out['annotations'].append({'prompt':p, 'type':'Solve for x'})
for p in simple_factor_prompts:
    out['annotations'].append({'prompt':p, 'type':'Factor eq'})
for p in simple_sys_eq_prompts:
    out['annotations'].append({'prompt':p, 'type':'Solve system of three equations'})
out_obj = json.dumps(out, indent=4)
#with open(dir_save+algebra_fn, "w") as outfile:
#    outfile.write(out_obj)


### Save Calc 1&2 ###
out = {'annotations':[]}
for p in devs:
    out['annotations'].append({'prompt':p, 'type':'derivative'})
for p in ints:
    out['annotations'].append({'prompt':p, 'type':'integral'})
out_obj = json.dumps(out, indent=4)
with open(dir_save+calc_12_fn, "w") as outfile:
    outfile.write(out_obj)