# -*- coding: utf-8 -*-
"""
Created on Sun May  9 17:09:23 2021

@author: brand
"""
import numpy as np
from array import *
from collections import Counter
matrix1 = np.matrix('0 1 0 0 0; 1 0 1 1 0; 0 1 0 1 0; 0 1 1 0 1; 0 0 0 1 0')

def degree_distribution(matrix):
    test = matrix.sum(axis=0)
    new_list=[]
    test2 = test.tolist()
    for x in test2[0]:
        new_list.append(x)
    Counting_dict=(Counter(new_list))
    length = len(new_list)
    probability_distribution = {}
    for value in Counting_dict.items():
        probability_distribution[value[0]]=value[1]/length
    print(probability_distribution)
    
degree_distribution(matrix1)

def average_degree_node(matrix):
    mean_degree = matrix.sum()/matrix.shape[0]
    return mean_degree

average_degree_node(matrix1)

def calculate_clustering_coefficent(matrix):
        for x in range(matrix.shape[0]):
            node = x+1
            neighbours = []
            for item in matrix[x,:]:
                item = item.tolist()
                for element in item:
                    for number in element:
                        print(number)
                print("")
    
calculate_clustering_coefficent(matrix1)

