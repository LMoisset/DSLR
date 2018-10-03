#! /usr/bin/python

import argparse
import matplotlib.pyplot as plt


### Quel cours de Poudlard a une repartition des notes homogenes entre les 4 maisons ?
def read_data2(dataname):
    with open('data/' + dataname) as f:
        lis=[line for line in f]
        feature_list = lis[0].strip().split(',')[5:] # only the subjects features
        nb_subjects = len(feature_list)
        feature_dico = dict((k,dict()) for k in feature_list)
        for student in lis[1:]:
            house = student.strip().split(',')[1]
            grades = student.strip().split(',')[5:]
            for i in range(nb_subjects):
                if house in feature_dico[feature_list[i]].keys():
                    feature_dico[feature_list[i]][house].append(grades[i])
                else:
                    feature_dico[feature_list[i]][house] = [grades[i]]
        return feature_dico, feature_list




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()
    feature_dico, feature_list = read_data2(args.set)
    houses = feature_dico[feature_list[0]].keys()

    print houses

    # for feature in feature_list:
    #     print feature
    #     print feature_dico[feature][10:12]


# plt.show(block = True)
