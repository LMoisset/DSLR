#! /usr/bin/python
import os
import argparse


### GIVES A DIT OF ALL OF THE FEATURES
def read_data(dataname):
    with open('data/' + dataname) as f:
        lis=[line for line in f]
        nb_features = len(lis[0].split(','))-1
        feature_list = lis[0].strip().split(',')[1:]
        first_student = lis[1].strip().split(',')[1:]
        feature_dico = dict((k, [l]) for k, l in zip(feature_list, first_student))
        for i in range(2, len(lis)):
            student = lis[i].strip().split(',')[1:]
            for f in range (len(feature_list)):
                feature_dico[feature_list[f]].append(student[f])

        print(count(feature_dico[feature_list[-2]]))
        print(mean(feature_dico[feature_list[-2]]))
        #for i in nb_features:
        #    features_{0}.format(str(i)) = []
        #    feature_list.append(features_{0}.format(str(i)))

        #for i,x in enumerate(lis):              #print the list items
        #    print 'line{0} = {1}'.format(i,x)

### Data Analysis

def count(list):
    return len(list)

def mean(list):
    m = 0
    for i in list:
        m += float(i)
    m = m / len(list)
    return m

### TO DO: enlever le premier (index dans la liste)



class dataframe:
    def __init__(self, dataname):
        self.dataname = dataname




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()
    read_data(args.set)
