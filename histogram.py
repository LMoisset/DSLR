#! /usr/bin/python

import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from describe import Quartile, Count, Mean


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



def anova4(x, y, z, t):
    x = [float(l) for l in x if l]
    y = [float(l) for l in y if l]
    z = [float(l) for l in z if l]
    t = [float(l) for l in t if l]
    tot = x + y +z + t
    tot_nest = [x, y, z, t]
    SSbetween = - sum(tot)**2/float(len(tot))
    for i in range(4):
        SSbetween += sum(tot_nest[i])**2/float(len(tot_nest[i]))
    SSwithin  = sum([l**2 for l in tot]) - sum(tot)**2/float(len(tot))
    dfb = len(tot_nest) - 1
    dfw = len(tot)- len(tot_nest)
    MSbetween = SSbetween/ dfb
    MSwithin = SSwithin / dfw
    F = MSbetween /MSwithin
    return F



def freq_per_house(feature, b = 20): # a dictionnary / b = nb of bins, an integer
    houses = feature.keys()
    # distribution of the grades for everyone
    all_grades = []
    for house in houses:
        all_grades += feature[house]
    mini = Quartile(all_grades, 0) #min
    maxi = Quartile(all_grades, 1) #max
    grade_list = [mini + (maxi-mini)/b*i for i in range(b+1)]
    # grade dico per range and per house
    #grade_dico = dict((house, dict()) for house in houses)
    xy_dico = dict((house, dict()) for house in houses)
    for house in houses:
        xy_dico[house]['x'] = [mini]
        xy_dico[house]['y'] = [0]
        lis = [float(l) for l in feature[house] if l]
        nb_student = Count(lis) # nb of students per house enrolled in the class
        for i in range(1,b+1):
            lis2 = [l for l in lis if (l <= grade_list[i] and l > grade_list[i-1])]
            freq = Count(lis2)/float(nb_student)
            #grade_dico[grade_list[house]][i] = freq
            xy_dico[house]['x'].extend((grade_list[i-1], grade_list[i]))
            xy_dico[house]['y'].extend((freq, freq))
        xy_dico[house]['x'].append(grade_list[b]) # pour refermer le graph
        xy_dico[house]['y'].append(0)
    score_hg = 0
    return xy_dico


house_colors = {'Ravenclaw': 'blue', 'Slytherin': 'green', 'Gryffindor' : 'red', 'Hufflepuff' : 'yellow'}

# ANOVA F stat with confidence alpha = 0.05
# grade repartition is homogeneous if F <= F_3_1550
F_3_1550 = 2.6





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

    homogen_features = []
    for feature in feature_list:
        X = feature_dico[feature]
        F = anova4(X[houses[0]],X[houses[1]], X[houses[2]], X[houses[3]])
        # print(F)
        if F <= F_3_1550:
            homogen_features.append(feature)


    k = 0
    fig = plt.figure(figsize = (20,10), dpi = 100)
    grid = gridspec.GridSpec(1, len(homogen_features))

    for feature in homogen_features:
        xy_dico = freq_per_house(feature_dico[feature], 20)
        plt.subplot(grid[0, k])

        for house in houses:
            x = xy_dico[house]['x']
            y = xy_dico[house]['y']
            plt.fill(x, y, color= house_colors[house], linewidth=2, label = house, alpha = 0.5)
        plt.xlim(Quartile(x,0),)
        plt.ylim(Quartile(y,0),)
        plt.title(feature_list[k])
        plt.legend(ncol = 2, fontsize = 'x-small')
        k += 1

    plt.tight_layout()
    plt.show(block = True)


    houses = feature_dico[feature_list[0]].keys()
    for i in range(len(feature_list[6:]) - 1):
        for j in feature_list[i+7:]:
            scatter_plot(feature_dico, feature_list[i + 6], j, house_colors)

    #ISOLER LES 3/4 PLUS PROCHES, RESSORTIR QUE CELLES LA






#plt.show(block = True)
