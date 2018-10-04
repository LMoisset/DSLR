#! /usr/bin/python

import argparse
import numpy as np
import pandas as pd
import copy


def cat_to_dummies(df):
    df2 = df.copy()
    cat_columns = list(df2.select_dtypes(include = ['object'])) 
    print(cat_columns)
    for col in cat_columns:
        categories = df[col].unique()
        for i in range(len(categories)-1):
            new_colname = col + '_' + categories[i]
            df2[new_colname] = df2[col]
            df2.loc[df2[new_colname] == categories[i], new_colname] = 1
            df2.loc[df2[new_colname] != categories[i], new_colname] = 0
        df2 = df2.drop(col, 1)
        return df2
    
        
def preprocess(dataname):
    df = pd.read_table('../data/'+dataname, sep = ',')
    X_df = df.drop(df.columns[[0,1,2, 3,4]], axis = 1) # get rid of index, name, birthday
    Y_df = df[df.columns[[1]]]
    colnames = list(X_df)
    X_df.apply(pd.to_numeric, errors = 'ignore')
    X_df2 = cat_to_dummies(X_df)
    return X_df2, Y_df


def g(z):
    res = 1 / (1 + np.exp(-z))
    return res

def h(x, theta):
    res = g(np.dot(np.transpose(theta), x))
    return res

def loss_function(theta, X, Y):
    return X


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()
    
    X_df, Y_df = preprocess(args.set)
    print(X_df.head())
    print(X_df.isnull().sum())
    






