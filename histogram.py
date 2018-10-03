#! /usr/bin/python

import argparse
import matplotlib.pyplot as plt
from describe import Quartile, Count


### Quel cours de Poudlard a une repartition des notes homogenes entre les 4 maisons ?
def read_data2(dataname):
    with open('../data/' + dataname) as f:
        lis=[line for line in f]
        feature_list = lis[0].strip().split(',')[6:] # only the subjects features
        nb_subjects = len(feature_list)
        feature_dico = dict((k,dict()) for k in feature_list)
        for student in lis[1:]:
            house = student.strip().split(',')[1]
            grades = student.strip().split(',')[6:]
            for i in range(nb_subjects):
                if house in feature_dico[feature_list[i]].keys():
                    feature_dico[feature_list[i]][house].append(grades[i])
                else:
                    feature_dico[feature_list[i]][house] = [grades[i]]
        return feature_dico, feature_list

def freq_per_house(feature): # a dictionnary and its keys
    houses = feature.keys()
    # distribution of the grades for everyone
    all_grades = []
    for house in houses:
        all_grades += feature[house]
    mini = Quartile(all_grades, 0) #min
    maxi = Quartile(all_grades, 1) #max
    grade_list = [mini + (maxi-mini)/10*i for i in range(11)]
    # grade dico per range and per house
    grade_dico = dict((grade, dict()) for grade in grade_list)
    for house in houses:
        lis = [float(l) for l in feature[house] if l]
        nb_student = Count(lis) # nb of students per house enrolled in the class
        print nb_student
        for i in range(1,11):
            lis2 = [l for l in lis if (l <= grade_list[i] and l > grade_list[i-1])]
            grade_dico[grade_list[i]][house] = Count(lis2)/ float(nb_student) # count nb of grades in the range
    return grade_dico






house_colors = {'Ravenclaw': 'blue', 'Slytherin': 'green', 'Gryffindor' : 'red', 'Hufflepuff' : 'yellow'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()
    feature_dico, feature_list = read_data2(args.set)
    houses = feature_dico[feature_list[0]].keys()

    print feature_dico[feature_list[0]][houses[0]][1:3]

    grade_dico = freq_per_house(feature_dico[feature_list[1]])
    print grade_dico

    # for feature in feature_list:
    #     print feature
    #     print feature_dico[feature][10:12]
    plt.plot([1, 2, 3, 4], [10, 20, 25, 30], color='lightblue', linewidth=3)
    plt.scatter([0.3, 3.8, 1.2, 2.5], [11, 25, 9, 26], color='darkgreen', marker='^')
    plt.xlim(0.5, 4.5)
    plt.show(block = True)
