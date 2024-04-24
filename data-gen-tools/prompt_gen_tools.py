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

np.random.seed(19960806)

##############################################################################
#################################### Funcs ###################################
##############################################################################
def gen_integral(n=1, bodies=['x'], bound_range=[-1,1], specific_bounds=[-np.inf, 0, np.inf, 1], p=0.2):
    rets = []
    for i in range(n):
        if(np.random.uniform() > p):
            bounds = np.random.uniform(bound_range[0], bound_range[1], 2)
        else:
            bounds = [0,0]
            while(bounds[0] == bounds[1]):
                bounds = np.random.choice(specific_bounds, 2)
        lb = str(min(bounds))
        ub = str(max(bounds))
        body = np.random.choice(bodies)
        rets.append( 'integral %s from %s to %s'%(body, lb, ub) )
    return rets

def gen_derivative(n=1, bodies=['x']):
    rets = []
    for i in range(n):
        body = np.random.choice(bodies)
        rets.append( 'derivative of %s'%(body) )
    return rets

def gen_2nd_derivative(n=1, bodies=['x']):
    rets = []
    for i in range(n):
        body = np.random.choice(bodies)
        rets.append( 'second derivative of %s'%(body) )
    return rets

def gen_3rd_derivative(n=1, bodies=['x']):
    rets = []
    for i in range(n):
        body = np.random.choice(bodies)
        rets.append( 'third derivative of %s'%(body) )
    return rets

def gen_exp(n=1, bodies=['x'], muls=[1,9], exps=[0,4], only_int_mul=True, only_int_exp=True):
    rets = []
    for i in range(n):
        body = np.random.choice(bodies)
        if(only_int_mul):
            mul = str(int(np.random.uniform(muls[0], muls[1])))
        else:
            mul = str(np.random.uniform(muls[0], muls[1]))
        if(only_int_exp):
            exp = str(int(np.random.uniform(exps[0], exps[1])))
        else:
            exp = str(np.random.uniform(exps[0], exps[1]))            
        rets.append( '%s*%s^%s'%(mul, body, exp) )
    return rets

def gen_trig(n=1, bodies=['x'], funcs=['sin', 'cos', 'tan'], include_con=False, include_pi=False):
    rets = []
    for i in range(n):
        ret = ''
        body = np.random.choice(bodies)
        func = np.random.choice(funcs)
        if(include_con):
            ret += np.random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
            ret += '*'
        ret += func + '(' + body
        if(include_pi):
            ret += '*pi'
        ret += ')' 
        rets.append( ret )
    return rets

def gen_log(n=1, bodies=['x'], bases=['10', '2', 'e'], include_con=False):
    rets = []
    for i in range(n):
        ret = ''
        body = np.random.choice(bodies)
        base = np.random.choice(bases)
        if(include_con):
            ret += np.random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
            ret += '*'
        if(base == '10'):
            l = 'log'
        elif(base == 'e'):
            l = 'ln'
        else:
            l = 'log'+base
        rets.append( '%s%s(%s)'%(ret, l, body) )
    return rets

def gen_ops(n=1, bodies=['x'], ops=['+','-','*'], op_num=[1,3], add_constant=True):
    rets = []
    for i in range(n):
        body = np.random.choice(bodies)
        op_n = int(np.random.uniform(op_num[0], op_num[1]))
        for j in range(op_n):
            b = np.random.choice(bodies)
            op = np.random.choice(ops)
            body += ' %s %s'%(op,b)
        if(add_constant):
            op = np.random.choice(ops)
            con = np.random.choice(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
            body += ' %s %s'%(op, con)            
        rets.append( body )
    return rets

def gen_div(n=1, bodies=['x'], p=1):
    rets = []
    for i in range(n):
        body_1 = np.random.choice(bodies)
        body_2 = np.random.choice(bodies)
        if(np.random.uniform() < p):
            rets.append( '((%s)/(%s))'%(body_1,body_2) )
        else:
            rets.append(body_1)
    return rets

def eq_solve(n=1, bodies=['x'], num_vars=1):
    rets = []
    for i in range(n):
        rets.append('solve for x in ')
        left  = np.random.choice(bodies, num_vars)
        right = np.random.choice(bodies, num_vars)
        for j in range(num_vars):
            if(j > 0):
                rets[-1] += ', '
            rets[-1] += '%s = %s'%(left[j], right[j])
    return rets

def combine_bodies(body1, body2, ops=['+','-']):
    rets = []
    for i in range(len(body1)):
        op = np.random.choice(ops)
        rets.append('%s %s %s'%(body1[i], op, body2[i]))
    return rets
    











