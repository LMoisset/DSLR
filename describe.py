#! /usr/bin/python
import os
import argparse
from math import sqrt

### GIVES A DICT OF ALL OF THE FEATURES
def read_data(dataname):
    with open('../data/' + dataname) as f:
        lis=[line for line in f]
        nb_features = len(lis[0].split(','))-1
        feature_list = lis[0].strip().split(',')[1:]
        first_student = lis[1].strip().split(',')[1:]
        feature_dico = dict((k, [l]) for k, l in zip(feature_list, first_student))
        print(feature_list)
        for i in range(2, len(lis)):
            student = lis[i].strip().split(',')[1:]
            for f in range(len(feature_list)):
                feature_dico[feature_list[f]].append(student[f])
        return feature_dico, feature_list

### Data Analysis
def Count(lis):
    return len(lis)

def Mean(lis):
    m = 0
    try:
        lis2 = [float(l) for l in lis if l] # remove empty strings + converts to floats
        for i in lis2:
            m += i
        m = m / len(lis2)
    except ValueError:
        m = 'Not numerical'
    return m

def Std(lis):
    n = len(lis)
    try:
        lis2 = [float(l) for l in lis if l] # remove empty strings + converts to floats
        lis3 =  [(l - Mean(lis2))**2 for l in lis2]
        sd = sqrt(sum(lis3)/n -1) # unbiaised
    except (TypeError, ValueError):
        sd = 'Not numerical'
    return sd

def Quartile(lis, p):
    n = len(lis)
    try:
        lis2 = [float(l) for l in lis if l]
        lis2 = sorted(lis2)
        if p == 1:
            quart = lis2[-1] # if we want the max
        else:
            quart = lis2[int(n*p)]
    except (TypeError, ValueError):
        quart = 'Not numerical'
    return quart


class dataframe:
    def __init__(self, dataname):
        self.dataname = dataname

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()
    feature_dico, feature_list = read_data(args.set)

    res = ['Feature', 'Count', 'Mean', 'Std', 'Min', '0.25%', '0.5%', 'O.75%', 'Max']
    print '%s' % '\t'.join([str(x) for x in res])

    for feature in feature_list:
        res = [feature]
        res.append(Count(feature_dico[feature]))
        res.append(Mean(feature_dico[feature]))
        res.append(Std(feature_dico[feature]))
        for i in [0, 0.25, 0.5, 0.75, 1]:
            res.append(Quartile(feature_dico[feature], i))

        print '%s' % '\t'.join([str(x) for x in res])
