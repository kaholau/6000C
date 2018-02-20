#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 16:34:04 2018

@author: hasnainmamdani
"""

import fibonacci_heap_mod
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
        return x,y

def compute_min_cost_path(seed, mat):
    
    pq = fibonacci_heap_mod.Fibonacci_heap()
    seed.set_total_cost(0)
    
    pq.enqueue(seed, seed.get_total_cost())
    
    while(pq.__len__ != 0):
        min_node = pq.dequeue_min()
        min_node.set_state(EXPANDED)
        
        ncoord = get_neighbour_coordinates(min_node.get_row_index(), min_node.get_column_index())
        
        for i in range(0, len(ncoord)):
            neighbour = mat[ncoord[i][0]][ncoord[i][1]]  
            
            if neighbour.get_state() == EXPANDED:
                continue
                
            if neighbour.state == INITIAL:
                neighbour.set_prev_node(min_node)
                neighbour.set_total_cost(min_node.get_toal_cost() + min_node.get_links_cost[i])
                neighbour.set_state(ACTIVE)
                pq.enqueue(neighbour, neighbour.get_total_cost())
                
            elif neighbour.state == ACTIVE:
                if (min_node.get_toal_cost() + min_node.get_links_cost[i]) < neighbour.get_total_cost():
                    neighbour.set_prev_node(min_node)
                    neighbour.set_total_cost(min_node.get_toal_cost() + min_node.get_links_cost[i])


def get_neighbour_coordinates(i, j):
    return ((i+1,j), (i+1,j-1), (i,j-1), (i-1,j-1), (i-1,j), (i-1,j+1), (i,j+1), (i+1,j+1))

print("Hello World!")