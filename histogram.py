#! /usr/bin/python

import argparse
import matplotlib.pyplot as plt
import numpy as np

def convert_float(x):
    if x != '':
        try:
            x = float(x)
            return x
        except (TypeError, ValueError):
            return x

### Quel cours de Poudlard a une repartition des notes homogenes entre les 4 maisons ?
def read_data2(dataname):
    with open('data/' + dataname) as f:
        lis=[line for line in f]
        feature_list = lis[0].strip().split(',')[6:] # only the subjects features
        nb_subjects = len(feature_list)
        feature_dico = dict((k,dict()) for k in feature_list)
        for student in lis[1:]:
            house = student.strip().split(',')[1]
            grades = student.strip().split(',')[5:]
            for i in range(nb_subjects):
                if house in feature_dico[feature_list[i]].keys():
                    feature_dico[feature_list[i]][house].append(convert_float(grades[i]))
                else:
                    feature_dico[feature_list[i]][house] = [convert_float(grades[i])]
        return feature_dico, feature_list

def bad_scatter_plot(dict, feature1, feature2, house_colors):
    list1 = dict[feature1]
    list2 = dict[feature2]
    full_x = []
    full_y = []
    color = []
    for house in house_colors.keys():
        x = list1[house]
        y = list2[house]
        full_x = full_x + x
        full_y = full_y + y
        col = [house_colors[house]]*len(x)
        color = color + col
    plt.plot(full_x, full_y, 'o',color = color, markersize=1)
    plt.show()

def scatter_plot(dict, feature1, feature2, house_colors):
    list1 = dict[feature1]
    list2 = dict[feature2]
    for house in house_colors.keys():
        x = list1[house]
        y = list2[house]
        plt.plot(x, y, 'o',color = house_colors[house], label = house, markersize=0.5)
    plt.xlabel(feature1)
    plt.ylabel(feature2)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()
    house_colors = dict([('Ravenclaw', 'blue'), ('Slytherin', 'green'), ('Gryffindor', 'red'), ('Hufflepuff', 'yellow')])
    feature_dico, feature_list = read_data2(args.set)
    houses = feature_dico[feature_list[0]].keys()
    for i in range(len(feature_list[6:]) - 1):
        for j in feature_list[i+7:]:
            scatter_plot(feature_dico, feature_list[i + 6], j, house_colors)

    #for feature in feature_list:
    #     print (feature)
    #     print (feature_dico[feature][10:12])



#plt.show(block = True)
