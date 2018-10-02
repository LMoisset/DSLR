#! /usr/bin/python
import os
import argparse

def read_data(dataname):
    with open('data/' + dataname) as f:
        lis=[line.split() for line in f]        # create a list of lists
        for i,x in enumerate(lis):              #print the list items
            print 'line{0} = {1}'.format(i,x)

#read_data('dataset_train.csv')
### Data Analysis

class dataframe:
    def __init__(self, dataname):
        self.dataname = dataname

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'name of the file to read')
    args = parser.parse_args()
    read_data(args.set)
