'''
Created on Jan 27, 2012

@author: yati

simple utility functions
'''
from random import random
import math
from settings import *
#-------------------------------------------------------------------------------
def get_random_bit():
    if random() < 0.5:
        return 0
    
    return 1
#-------------------------------------------------------------------------------
def get_random_bits(length):
    return [get_random_bit() for i in xrange(length)]
#-------------------------------------------------------------------------------
def get_random_triple(do_clamp=True):
    if do_clamp:
        r = random() * MAX_RADIUS
        x = clamp(random() * WINDOW_WIDTH ,r , (WINDOW_WIDTH - r))
        y = clamp(random() * WINDOW_HEIGHT, r, (WINDOW_HEIGHT -r))
    else:
        r = random() * MAX_RADIUS * 2
        x = random() * MAX_RADIUS
        y = random() * MAX_RADIUS
        
    return x, y, r
#-------------------------------------------------------------------------------
def clamped_rand():
    return random() - random()
#-------------------------------------------------------------------------------
def overlap(circ1, circ2):
    '''
    Checks if two circles overlap.
    The basis is that two circles do overlap partially or completely, if 
    the distance between their centers is less than the sum of their radii.
    Instead of taking the sqrt in the two point distance formula, we square the
    radius, as a > b <=> a ** 2 > b ** 2 for a, b >= 0
    ''' 
    (x1, y1, r1) = circ1
    (x2, y2, r2) = circ2
    y2_y1 = y2 - y1
    x2_x1 = x2 - x1
    r1r2 = r1 + r2
    return (x2_x1 * x2_x1 + y2_y1 * y2_y1) < (r1r2 * r1r2)
#-------------------------------------------------------------------------------
def clamp(x, lo, hi):
    if x < lo:
        return lo
    
    if x > hi:
        return hi
    
    return x
#-------------------------------------------------------------------------------
def clamp_triple(trip):
    x, y, r = trip
    r = clamp(r, 0, MAX_RADIUS)
    x = clamp(x, r, WINDOW_WIDTH - r)
    y = clamp(y, r, WINDOW_HEIGHT - r)
    
    return x, y, r
#-------------------------------------------------------------------------------