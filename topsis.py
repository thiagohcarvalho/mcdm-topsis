import numpy as np

class Topsis:
  def __init__(self, matrix, criteria, weight, alternative_list):
    self.matrix = np.array(matrix, dtype="float")
    self.criteria = np.array(criteria)
    self.weight = np.array(weight, dtype="float")
    self.weight = self.weight/sum(self.weight) #para fazer a proporção dos pesos
    self.alternative_list = np.array(alternative_list)

    self.normalized_matrix = np.array([])
    self.weighted_matrix = np.array([])
    self.row_size = len(matrix) #amount of alternatives
    self.column_size = len(matrix[0]) #amount of criteria

  def normalize_matrix(self): #to find the normalization score #step2
    self.normalized_matrix = np.copy(self.matrix)
    squared_sum = np.zeros(self.column_size)

    for i in range(self.row_size):
      for j in range(self.column_size):
        squared_sum[j]+=self.matrix[i, j]**2

    for i in range(self.row_size): 
      for j in range(self.column_size):
        self.normalized_matrix[i, j] = float(self.matrix[i, j]/(squared_sum[j]**0.5))

  def weight_matrix(self): #to multiply the values to their weights #step3
    self.weighted_matrix = np.copy(self.normalized_matrix)

    for i in range(self.row_size):
      for j in range(self.column_size):
        self.weighted_matrix[i, j]*=self.weight[j]

  def best_worst_ideal_solution(self): #step4
    self.best_ideal_solution = np.zeros(self.column_size)
    self.worst_ideal_solution = np.zeros(self.column_size)

    highest_values = self.weighted_matrix.max(axis = 0)
    lowest_values = self.weighted_matrix.min(axis = 0)

    for i in range(self.column_size):
      if self.criteria[i]: #caso o maior valor seja o ideal positivo
        self.best_ideal_solution[i] = highest_values[i]
        self.worst_ideal_solution[i] = lowest_values[i]
      elif self.criteria[i] == False: #caso o menor valor seja o ideal positivo
        self.best_ideal_solution[i] = lowest_values[i]
        self.worst_ideal_solution[i] = highest_values[i]

  def find_distance(self): #step5
    self.positive_distance = np.zeros(self.row_size)
    self.negative_distance = np.zeros(self.row_size)

    for i in range(self.row_size):
      distance_pos = 0
      distance_neg = 0
      for j in range(self.column_size):
        distance_pos+=((self.best_ideal_solution[j]-self.weighted_matrix[i, j])**2)
        distance_neg+=((self.worst_ideal_solution[j]-self.weighted_matrix[i, j])**2)
        if j == (self.column_size-1):
          distance_pos = distance_pos**0.5
          self.positive_distance[i] = distance_pos 
          distance_neg = distance_neg**0.5
          self.negative_distance[i] = distance_neg

  def find_similarity_worse_decision(self): #step 6
    np.seterr(all='ignore')
    dtype = [("alternative-name", 'U16'), ("score", float)]
    self.scores = np.empty(self.row_size, dtype=dtype)

    for i in range(self.row_size):
      value = self.negative_distance[i]/(self.positive_distance[i] + self.negative_distance[i])
      self.scores[i] = (self.alternative_list[i], value)



    ###########


    # self.scores = []

    # for i in range(self.row_size):
    #   value = self.negative_distance[i]/(self.positive_distance[i] + self.negative_distance[i])
    #   self.scores.append((self.alternative_list[i], value))
    #   #self.scores[i] = [self.alternative_list[i], value]
    # dtype = [("alternative-name", 'U16'), ("score", float)]
    # self.scores_temp = np.asarray(self.scores, dtype=dtype)

  def ranking_by_worst(self):
    self.ranking = np.sort(self.scores, order="score")[::-1]
    self.ranking_inverted = np.sort(self.scores, order="score")

    print("Ranqueamento Topsis:")
    for rank in self.ranking:
      print(rank[0] + ":", rank[1])

    print("\nRanqueamento Topsis invertido:")
    for rank in self.ranking_inverted:
      print(rank[0] + ":", rank[1])

matrix = np.array([
    [3,1,1,1,0,18,120,10000],
    [3,3,3,1,0,27,365,90000],
    [4,3,3,1,0,27,120,30000],
    [2,4,1,1,0,24,200,35000],
    [2,4,1,1,0,24,200,40000],
    [5,3,2,1,0,27,120,90000],
    [3,1,1,1,0,3,400,20000],
    [3,4,3,1,0,27,120,20000],
    [3,1,1,1,0,27,420,80000],
    [2,1,1,1,0,27,120,60000],
    [1,1,1,1,0,27,120,70000],
    [2,3,1,1,0,8,150,45000],
    [5,5,3,1,0,48,200,80000],
    [3,3,3,1,0,36,120,50000],
    [5,3,2,1,100,125,120,200000],
])

weight = [12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5, 12.5,]

criteria = np.array([True, True, True, True, True, False, False, False]) #True means highest is best, False means lowest is best

alternative_list = ["Projeto 1", "Projeto 2", "Projeto 3", "Projeto 4", "Projeto 5", "Projeto 6", "Projeto 7", "Projeto 8", "Projeto 9", "Projeto 10", "Projeto 11", "Projeto 12", "Projeto 13", "Projeto 14", "Projeto 15"]

topsis = Topsis(matrix, criteria, weight, alternative_list)

topsis.normalize_matrix()
topsis.weight_matrix()
topsis.best_worst_ideal_solution()
topsis.find_distance()
topsis.find_similarity_worse_decision()
topsis.ranking_by_worst()