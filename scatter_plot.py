import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from describe import Quartile, Count, Mean
from histogram import read_data2


house_colors = {'Ravenclaw': 'blue', 'Slytherin': 'green', 'Gryffindor' : 'red', 'Hufflepuff' : 'yellow'}

def scatter_plot(dict, feature1, feature2, house_colors):
    list1 = dict[feature1]
    list2 = dict[feature2]
    for house in house_colors.keys():
        x = list1[house]
        y = list2[house]
        plt.plot(x, y, 'o',color = house_colors[house], label = house, markersize=0.5)
    return plt

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()
    house_colors = dict([('Ravenclaw', 'blue'), ('Slytherin', 'green'), ('Gryffindor', 'red'), ('Hufflepuff', 'yellow')])
    feature_dico, feature_list = read_data2(args.set)

    houses = feature_dico[feature_list[0]].keys()
    for i in range(len(feature_list[6:]) - 1):
        for j in feature_list[i+7:]:
            plt = scatter_plot(feature_dico, feature_list[i + 6], j, house_colors)
            plt.xlabel(feature_list[i + 6])
            plt.ylabel(j)
            plt.show()

    #ISOLER LES 3/4 PLUS PROCHES, RESSORTIR QUE CELLES LA






#plt.show(block = True)
