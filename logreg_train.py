#! /usr/bin/python

import argparse
import numpy as np
import pandas as pd


def cat_to_dummies(df):
    cat_columns = list(df.select_dtypes(include = ['object']))
    print(cat_columns)
    for col in cat_columns:
        categories = df[col].unique()
        for i in range(len(categories)-1):
            new_colname = col + '_' + categories[i]
            df[new_colname] = df[col]
            df.loc[df[new_colname] == categories[i]] = 1
            df.loc[df[new_colname] != categories[i]] = 0
        df = df.drop(col, 1)
        return df



def preprocess(dataname):
    df = pd.read_table('../data/'+dataname, sep = ',')
    X_df = df.drop(df.columns[[0,1,2, 3,4]], axis = 1) # get rid of index, name, birthday
    Y_df = df[df.columns[[1]]]
    colnames = list(X_df)
    X_df.apply(pd.to_numeric, errors = 'ignore')
    return X_df, Y_df


def g(z):
    res = 1 / (1 + np.exp(-z))
    return res

def h(x, theta):
    res = g(np.dot(np.transpose(theta), x))
    return res

def loss_function(theta, X, Y):
    m = len(X)
    J = 0
    for i in range(1, m+1):
        J += -1/m * (Y[i]*log(h(X[i], theta))) + (1-Y[i])log(1-h(X[i], theta))
    return J

def gradient(theta, X, Y, j):
    m = len(X)
    dJ = 0
    for i in range(1, m+1):
        dJ += (h(X[i], theta) - Y[i])X[i][j]
    return dJ

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()

    X_df, Y_df = preprocess(args.set)
    X_new = cat_to_dummies(X_df)
    print(X_new.head())
    print(X_df.head())
