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
    def __init__(self,x,y,links):
        self.links_cost = links
        self.state = 0
        self.total_cost = math.inf #the minimum total cost from this node to the seed node.  
        self.prev_node = None #points to its predecessor along the minimum cost path from the seed to that node. 
        self.row = x
        self.column = y
        return
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
    def set_prev_node(self, value):
        self.total_cost = value
        return
    def get_row_index(self):
        return self.row
    def get_column_index(self):
        return self.column    
    def __repr__(self):
        return self.row, self.column
