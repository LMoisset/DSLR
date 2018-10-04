import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from describe import Quartile, Count, Mean
from histogram import read_data2



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

    houses = feature_dico[feature_list[0]].keys()
    for i in range(len(feature_list[6:]) - 1):
        for j in feature_list[i+7:]:
            scatter_plot(feature_dico, feature_list[i + 6], j, house_colors)

    #ISOLER LES 3/4 PLUS PROCHES, RESSORTIR QUE CELLES LA






#plt.show(block = True)
