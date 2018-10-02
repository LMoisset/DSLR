#! /usr/bin/python
import os

def read_data(dataname):
    with open("data/" + dataname) as f:
        lis=[line.split() for line in f]        # create a list of lists
        for i,x in enumerate(lis):              #print the list items
            print "line{0} = {1}".format(i,x)

read_data('dataset_train.csv')
### Data Analysis
