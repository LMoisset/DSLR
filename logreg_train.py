#! /usr/bin/python

import argparse
import copy
import math
import pandas as pd
import numpy as np
from describe import Mean
import pickle


class Matrix(list):
    def __init__(self, mat):
        super().__init__(mat)

    @property
    def nrow(self):
        return len(self)

    @property
    def ncol(self):
        return len(self[0])

    def product(self,scalar):
        return Matrix([[row[i]*scalar for i in range(self.ncol)] for row in self])

    def Exp(self):
        return Matrix([[math.exp(row[i]) for i in range(self.ncol)] for row in self])

    def dot(self,mat2):
        if self.ncol == mat2.nrow:
            mat = [[0]*mat2.ncol for i in range(self.nrow)]
            for i in range(self.nrow):
                for j in range(mat2.ncol):
                    mat[i][j] = sum([self[i][k]*mat2[k][j] for k in range(self.ncol)])
        else:
            raise TypeError('The matrix are not compatible for multiplication')
        return Matrix(mat)

    def transpose(self): 
        return Matrix([[row[i] for row in self] for i in range(self.ncol)])    

    def show(self):
        for row in self:
            print ('%s' % '\t'.join([str(x) for x in row]))

    def append_col(self, col): # col should be a list here
        if self.nrow == len(col):
            for i in range(self.nrow):
                self[i].append(col[i])
        else:
            raise TypeError('Cannot append column of different size')
        return Matrix(self)

    def col(self,i):
        return Matrix([[row[i]] for row in self])

    def row(self,i):
        return Matrix([self[i]])

    def drop(self, k_list, axis):
        if axis == 0: # rows
            mat = Matrix([self[i] for i in [x for x in range(self.nrow) if x != k_list[0]]]) # initialisation
            if len(k_list) > 1:
                for k in k_list:
                    mat = Matrix([self[i] for i in [x for x in range(self.nrow) if x != k]])
        elif axis ==1: # columns
            mat = Matrix([[row[i] for row in self] for i in [x for x in range(self.ncol) if x != k_list[0]]])
            if len(k_list) >1:
                for k in k_list:
                    mat = Matrix([[row[i] for row in mat] for i in [x for x in range(self.ncol) if x != k]])
        return mat

    def to_float(self):
        return Matrix([[float(row[i]) if row[i].replace('.', '',1).isdigit() else row[i] for i in range(self.ncol)] for row in self])

    def unique(self, i, axis):
        res = []
        if axis == 0:
            for k in range(self.ncol):
                if self[i][k] not in res:
                    res.append(self[i][k])
        elif axis == 1:
            for k in range(self.nrow):
                if self[k][i] not in res:
                    res.append(self[k][i])
        return res                 

        



def read_data3(dataname):
    with open('../data/' + dataname) as f:
        return Matrix([line.strip().split(',') for line in f])

def cat_to_dummies(X): ### ATTENTION PB  --- pas le nom des colonens, on va se perdre dans les features
    ind_to_drop = []
    for i in range(X.ncol):
        cat = X.col(i).unique()
        if len(cat) <5: # si moins de 5 uniques, on assume que la var est cat
            ind_to_drop.append(i)
            for j in range(len(cat)-1):
                new_col = [1 if x == cat[j] else 0 for x in [row[i] for row in X]]
                X.append_col(new_col)
    X.drop(ind_to_drop, axis = 1)
    return X

def impute_na(X): # pour l'instant mean imputation/ pk pas EM si temps
    return Matrix([Mean([[row[i] for row in X]) if row[i] =='' else row[i] for i in range(self.ncol)] for row in self])

def preprocess(dataname):
    df = read_data3('../data/'+dataname, sep = ',')
    Y = df.col(1)
    X = df.drop([0,1,2, 3,4], axis = 1) # get rid of index, name, birthday
    features = X[0]
    X = X.drop([0], axis = 0)
    X = X.to_float()
    # 1rst, we transform categorical variables into dummies
    X_2 = cat_to_dummies(X)
    # 2nd, handling Missing Values
    X_3 = impute_na(X_2)
    # get rid of correlated data 
    return X_2, Y, features


def g(z):
    res = 1 / (1 + z.Exp().product(-1))
    return res

def h(X, theta): # X is here an individual transformed into a column
    res = g(theta.transpose.dot(X))
    return res

def loss_function(X, Y, theta): # X is an array, Y a column array
    m = len(Y)
    J = 0
    for i in range(m):
        X_t = X[[i]].transpose()
        J += -1/m * (Y[i]*log(h(X_t, theta))) + (1-Y[i])*log(1-h(X_t, theta))
    return J

def gradient(X, Y, theta, j): # X is an array, Y a column array
    m = len(Y)
    dJ = 0
    for i in range(m):
       dJ += 1/m*(h(X[[i]].transpose(), theta) - Y[i])*X[[i],[j]]
    return dJ


#def gradient_descent(X, Y, theta, learning_rate = 0.01, iterations = 100):
#    m = len(Y)
#    cost = np.zeros(iterations)



    
       



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()

    #X = read_data3(args.set)
    #print(X.drop([0], axis = 0)[0])
    test = Matrix([['1','2.5', '']])
    #t2 = [float(x) if x.replace('.', '',1).isdigit() else x for x in test]
    print(test)
    print(test.nrow, test.ncol)
    print(test.to_float())


    #X, Y, features = preprocess(args.set)
    #print(X)
    #print(X[[0]])
    #print(Y)
    #print(Y[0])
    #print(X[[0],[1]])
    #print(X[[0]][0])
    #print(len(X))




