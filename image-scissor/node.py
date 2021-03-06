#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 16:34:04 2018

@author: hasnainmamdani
"""

import math


INITIAL = 0
ACTIVE = 1
EXPANDED = 2

class Node:
    def __init__(self,x,y,pixel,links):
        self.row = x
        self.column = y
        self.pixel = pixel
        self.links_cost = links
        self.state = INITIAL
        self.total_cost = math.inf #the minimum total cost from this node to the seed node.  
        self.prev_node = None #points to its predecessor along the minimum cost path from the seed to that node. 
        return
    def get_pixel(self):
        return self.pixel
    def get_links_cost(self):
        return self.links_cost
    def get_state(self):
        return self.state
    def set_state(self, value):
        self.state = value
        return
    def get_total_cost(self):
        return self.total_cost
    def set_total_cost(self, value):
        self.total_cost = value
        return
    def get_prev_node(self):
        return self.prev_node
    def set_prev_node(self, value):
        self.prev_node = value
        return
    def get_row_index(self):
        return self.row
    def get_column_index(self):
        return self.column
    def reset(self):
        self.state = INITIAL
        self.total_cost = math.inf  
        self.prev_node = None
        return
    def __cmp__(self, other):
        return cmp(self.total_cost, other.total_cost)
    def __lt__(self, other):
        return self.total_cost < other.total_cost
    def __repr__(self):
        return "row:{:s}, column:{:s}, links_cost:{:s}, state:{:s}, total_cost:{:s}".format(str(self.row), str(self.column), str(self.links_cost), str(self.state), str(self.total_cost)) 
    