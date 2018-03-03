#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 18 16:34:04 2018

@author: hasnainmamdani
"""

import fibonacci_heap_mod
import heapq
import node
import queue as Q


def compute_min_cost_path(x, y, node_mat):
    
    #pq = fibonacci_heap_mod.Fibonacci_heap()
    heap = []
    #q = Q.PriorityQueue()
    
    #print("node matrix dimensions: ")
    node_mat_dim_x = len(node_mat)
    node_mat_dim_y = len(node_mat[0])
    #print(node_mat_dim_x)
    #print(node_mat_dim_y)
    
    seed = node_mat[x][y] 
    seed.set_total_cost(0)
    
    print("seed node is:")
    print(seed)
    
    #pq.enqueue(seed, seed.get_total_cost())
    heapq.heappush(heap, (seed.get_total_cost(), seed))
    #q.put((seed.get_total_cost(), seed))
    
    #while(pq.__len__() > 0):
    while(len(heap) > 0):
    #while not q.empty():
        #min_node = pq.dequeue_min().get_value()
        min_node = heapq.heappop(heap)[1]
        #min_node = q.get()[1]
        
        #print("min node is:")
        #print(min_node)
        min_node.set_state(node.EXPANDED)
        
        ncoord = get_neighbour_coordinates(min_node.get_row_index(), min_node.get_column_index())
        
        for i in range(0, len(ncoord)):
            
            if (ncoord[i][0] >= node_mat_dim_x) or (ncoord[i][1] >= node_mat_dim_y):
                continue
            #print("index")
            #print(str(ncoord[i][0]))
            #print(str(ncoord[i][1]))
            neighbour = node_mat[ncoord[i][0]][ncoord[i][1]]  
            
            if neighbour.get_state() == node.EXPANDED:
                continue
                
            if neighbour.state == node.INITIAL:
                neighbour.set_prev_node(min_node)
                neighbour.set_total_cost(min_node.get_total_cost() + min_node.get_links_cost()[i])
                neighbour.set_state(node.ACTIVE)
                #pq.enqueue(neighbour, neighbour.get_total_cost())
                heapq.heappush(heap, (neighbour.get_total_cost(), neighbour))
                #q.put((neighbour.get_total_cost(), neighbour))
                
            elif neighbour.state == node.ACTIVE:
                if (min_node.get_total_cost() + min_node.get_links_cost()[i]) < neighbour.get_total_cost():
                    neighbour.set_prev_node(min_node)
                    neighbour.set_total_cost(min_node.get_total_cost() + min_node.get_links_cost()[i])


def get_neighbour_coordinates(i, j):
    return ((i+1,j), (i+1,j-1), (i,j-1), (i-1,j-1), (i-1,j), (i-1,j+1), (i,j+1), (i+1,j+1))

def get_min_path_from_seed(x, y, node_mat):  
    curr_node = node_mat[x][y]
    path_mat = [curr_node]
    prev_node = curr_node.get_prev_node()
    
    while (prev_node != None):
        path_mat.append(prev_node)
        prev_node = prev_node.get_prev_node()
        
    return path_mat
        
def reset_node_matrix(node_mat):

    node_mat_dim_x = len(node_mat)
    node_mat_dim_y = len(node_mat[0]) 
    
    for i in range(0, node_mat_dim_x):
        for j in range(0, node_mat_dim_y):
            node_mat[i][j].reset()
            
            
            
            
            