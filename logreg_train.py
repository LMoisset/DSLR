#! /usr/bin/python

import argparse
import copy
import math
from describe import Mean
#import pickle


## TEST

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
            mat = Matrix([self[i] for i in [k for k in range(self.nrow) if k not in k_list]])
        elif axis == 1: # columns
            mat = Matrix([[row[i] for i in [k for k in range(self.ncol) if k not in k_list]] for row in self])
        return mat

    def to_float(self):
        return Matrix([[float(row[i]) if row[i].replace('-','',1).replace('.', '',1).isdigit() else row[i] for i in range(self.ncol)] for row in self])

    def unique(self, i, axis):
        unique_values = []
        if axis == 0:
            for k in range(self.ncol):
                if self[i][k] not in unique_values:
                    unique_values.append(self[i][k])
        elif axis == 1:
            for k in range(self.nrow):
                if self[k][i] not in unique_values:
                    unique_values.append(self[k][i])
        return unique_values
    
    def count_null(self):
        null_dico = dict((k, 0) for k in range(self.ncol))
        for i in range(self.ncol):
            for j in range(self.nrow):
                if self[j][i] == '':
                    null_dico[i] +=1
        return null_dico  


        
def read_data3(dataname):
    with open('../data/' + dataname) as f:
        return Matrix([line.strip().split(',') for line in f])

def cat_to_dummies(X, features): 
    ind_to_drop = []
    for i in range(X.ncol):
        cat = X.unique(i, axis = 1)
        if len(cat) <5: # si moins de 5 uniques, on assume que la var est cat
            ind_to_drop.append(i)
            for j in range(len(cat)-1):
                new_cat = features[i] + '_' + cat[j]
                new_col = [1 if x == cat[j] else 0 for x in [row[i] for row in X]]
                X.append_col(new_col)
                features.append(new_cat)
    X = X.drop(ind_to_drop, axis = 1)
    features = [features[i] for i in range(len(features)) if i not in ind_to_drop]
    return X, features

def impute_na(X): # pour l'instant mean imputation
    return Matrix([[Mean([row[i] for row in X]) if row[i] =='' else row[i] for i in range(X.ncol)] for row in X])

def preprocess(dataname):
    df = read_data3('../data/'+dataname)
    Y = df.col(1)
    print(df[0])
    X = df.drop([0,1,2,3,4], axis = 1) # get rid of index, house, firstname, lastname, birthday
    features = X[0]
    X = X.drop([0], axis = 0)
    X = X.to_float()
    # 1rst, we transform categorical variables into dummies
    X_2, features = cat_to_dummies(X,features)
    print(X_2.count_null())
    # 2nd, handling Missing Values
    X_3 = impute_na(X_2)
    print(X_3.count_null())
    # get rid of correlated data 
    return X_3, Y, features


def g(z):  # z est un reel
    return 1 / (1 + z.product(-1).Exp())

def h(X, theta): # X is here an individual transformed into a column
    return g(theta.transpose().dot(X))

def loss_function(X, Y, theta): # X is an array, Y a column array
    m = len(Y)
    J = 0
    for i in range(m):
        J += -1/m * (Y[i]*log(h(X.col(i), theta))) + (1-Y[i])*log(1-h(X.col(i), theta))
    return J

def derive_part(X, Y, theta, j): # X is an array, Y a column array
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
    #test = Matrix([['1','2', '3'], ['4', '5', '6']])
    #t2 = [float(x) if x.replace('.', '',1).isdigit() else x for x in test]
    #test.show()
    #test.drop([], axis = 1).show()
    #print(test.unique(0, axis = 1))
    

    #X, Y, features = preprocess(args.set)
    #print(features)
    theta = Matrix([[1],[2],[3]])
    X = Matrix([[4], [5], [6]])
    theta.transpose().dot(X).show()
    theta.product(-1).show()
    #print(h(theta,X))
    #print(X)
    #print(Y)
    #print(Y[0])
    #print(X[0])
    #print(X[[0]][0])
    #print(len(X))




