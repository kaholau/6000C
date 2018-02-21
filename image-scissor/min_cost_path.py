#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 16:34:04 2018

@author: hasnainmamdani
"""

import fibonacci_heap_mod
import node


def compute_min_cost_path(x, y, node_mat):
    
    pq = fibonacci_heap_mod.Fibonacci_heap()
    
    seed = node_mat[x][y] 
    seed.set_total_cost(0)
    
    pq.enqueue(seed, seed.get_total_cost())
    
    while(pq.__len__ != 0):
        min_node = pq.dequeue_min()
        min_node.set_state(node.EXPANDED)
        
        ncoord = get_neighbour_coordinates(min_node.get_row_index(), min_node.get_column_index())
        
        for i in range(0, len(ncoord)):
            neighbour = node_mat[ncoord[i][0]][ncoord[i][1]]  
            
            if neighbour.get_state() == node.EXPANDED:
                continue
                
            if neighbour.state == node.INITIAL:
                neighbour.set_prev_node(min_node)
                neighbour.set_total_cost(min_node.get_toal_cost() + min_node.get_links_cost[i])
                neighbour.set_state(node.ACTIVE)
                pq.enqueue(neighbour, neighbour.get_total_cost())
                
            elif neighbour.state == node.ACTIVE:
                if (min_node.get_toal_cost() + min_node.get_links_cost[i]) < neighbour.get_total_cost():
                    neighbour.set_prev_node(min_node)
                    neighbour.set_total_cost(min_node.get_toal_cost() + min_node.get_links_cost[i])


def get_neighbour_coordinates(i, j):
    return ((i+1,j), (i+1,j-1), (i,j-1), (i-1,j-1), (i-1,j), (i-1,j+1), (i,j+1), (i+1,j+1))
