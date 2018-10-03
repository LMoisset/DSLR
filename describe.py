#! /usr/bin/python
import os
import argparse
from math import sqrt

### GIVES A DICT OF ALL OF THE FEATURES
def read_data(dataname):
    with open('data/' + dataname) as f:
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
        for i in lis:
            m += float(i)
        m = m / len(lis)
    except TypeError:
        m = 'Not numerical'
    return m

def Std(lis):
    n = len(lis)
    try:
        lis2 =  [(l - Mean(lis))**2 for l in lis]
        sd = sqrt(sum(lis2)/n -1)
    except (TypeError, ValueError):
        sd = 'Not numerical'
    return sd

def Quartile(lis, p):
    n = len(lis)
    try:
        lis2 = [float(l) for l in lis]
        lis2 = sorted(lis2)
        if p == 1:
            quart = lis2[-1] # le max
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

    for feature in feature_list:
        print feature_dico[feature][10]
        res = []
        #res.append(Count(feature_dico[feature]))
        res.append(Mean(feature_dico[feature]))
        # res.append(Std(feature_dico[feature]))
        # for i in [0, 0.25, 0.5, 0.75, 1]:
        #     res.append(Quartile(feature_dico[feature], i))

        print '%s' % '\t'.join([str(x) for x in res])

#### PB : certains floats pas convertis ??

    # print Count(feature_dico[feature_list[-1]])
    # print Mean(feature_dico[feature_list[-1]])
    # print Quartile(feature_dico[feature_list[-1]], 0)
    # print Quartile(feature_dico[feature_list[-1]], 0.25)
    # print Quartile(feature_dico[feature_list[-1]], 0.5)
    # print Quartile(feature_dico[feature_list[-1]], 0.75)
    # print Quartile(feature_dico[feature_list[-1]], 1)
