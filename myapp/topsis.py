import numpy as np
import csv
import re
from .models import Document
from django.shortcuts import redirect, render


class Topsis:
    def __init__(self, matrix, criteria, weight, alternative_list):
        self.matrix = np.array(matrix, dtype="float")
        self.criteria = np.array(criteria)
        self.weight = np.array(weight, dtype="float")
        # para fazer a proporção dos pesos
        self.weight = self.weight/sum(self.weight)
        self.alternative_list = np.array(alternative_list)

        self.normalized_matrix = np.array([])
        self.weighted_matrix = np.array([])
        self.row_size = len(matrix)  # amount of alternatives
        self.column_size = len(matrix[0])  # amount of criteria

    def normalize_matrix(self):  # to find the normalization score #step2
        np.set_printoptions(suppress=True)
        self.normalized_matrix = np.copy(self.matrix)
        squared_sum = np.zeros(self.column_size)

        for i in range(self.row_size):
            for j in range(self.column_size):
                squared_sum[j] += self.matrix[i, j]**2

        for i in range(self.row_size):
            for j in range(self.column_size):
                self.normalized_matrix[i, j] = float(
                    self.matrix[i, j]/(squared_sum[j]**0.5))

        return np.round_(np.sqrt(squared_sum), decimals=5)

    def weight_matrix(self):  # to multiply the values to their weights #step3
        self.weighted_matrix = np.copy(self.normalized_matrix)

        for i in range(self.row_size):
            for j in range(self.column_size):
                self.weighted_matrix[i, j] *= self.weight[j]

        return self.weighted_matrix

    def best_worst_ideal_solution(self):  # step4
        self.best_ideal_solution = np.zeros(self.column_size)
        self.worst_ideal_solution = np.zeros(self.column_size)

        highest_values = self.weighted_matrix.max(axis=0)
        lowest_values = self.weighted_matrix.min(axis=0)

        for i in range(self.column_size):
            if self.criteria[i]:  # caso o maior valor seja o ideal positivo
                self.best_ideal_solution[i] = highest_values[i]
                self.worst_ideal_solution[i] = lowest_values[i]
            elif self.criteria[i] == False:  # caso o menor valor seja o ideal positivo
                self.best_ideal_solution[i] = lowest_values[i]
                self.worst_ideal_solution[i] = highest_values[i]

        return (self.best_ideal_solution, self.worst_ideal_solution)

    def find_distance(self):  # step5
        self.positive_distance = np.zeros(self.row_size)
        self.negative_distance = np.zeros(self.row_size)

        for i in range(self.row_size):
            distance_pos = 0
            distance_neg = 0
            for j in range(self.column_size):
                distance_pos += (
                    (self.best_ideal_solution[j]-self.weighted_matrix[i, j])**2)
                distance_neg += (
                    (self.worst_ideal_solution[j]-self.weighted_matrix[i, j])**2)
                if j == (self.column_size-1):
                    distance_pos = distance_pos**0.5
                    self.positive_distance[i] = distance_pos
                    distance_neg = distance_neg**0.5
                    self.negative_distance[i] = distance_neg

        return (self.positive_distance, self.negative_distance)

    def find_similarity_worse_decision(self):  # step 6
        np.seterr(all='ignore')
        dtype = [("alternative-name", 'U16'), ("score", float)]
        self.scores = np.empty(self.row_size, dtype=dtype)

        for i in range(self.row_size):
            value = self.negative_distance[i] / \
                (self.positive_distance[i] + self.negative_distance[i])
            self.scores[i] = (self.alternative_list[i], value)

        return self.scores

    def ranking_by_worst(self):
        self.ranking = np.sort(self.scores, order="score")[::-1]
        return self.ranking

    def ranking_by_worst_inverted(self):
        self.ranking_inverted = np.sort(self.scores, order="score")
        return self.ranking_inverted
