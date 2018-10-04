import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from describe import Quartile, Count, Mean
from scatter_plot import scatter_plot
from histogram import read_data2

house_colors = {'Ravenclaw': 'blue', 'Slytherin': 'green', 'Gryffindor' : 'red', 'Hufflepuff' : 'yellow'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()
    feature_dico, feature_list = read_data2(args.set)
    houses = list(feature_dico[feature_list[0]].keys())


    l = 0
    m = 0
    fig = plt.figure(figsize = (20,10), dpi = 100)
    grid = gridspec.GridSpec(10,8)
    for k in range(int((len(feature_list) - 1)*len(feature_list)/2)):
        if k <8:
            l = k
        else:
            m = k//8
            l = k - 8*m
        plt.subplot(grid[m, l])
        for i in range(len(feature_list[10:]) - 1):
            for j in feature_list[i+1:]:
                list1 = feature_dico[feature_list[i]]
                list2 = feature_dico[j]
                for house in house_colors.keys():
                    x = list1[house]
                    y = list2[house]
                    plt.fill(x, y, 'o', color = house_colors[house], label = house)
    plt.tight_layout()
    plt.show(block = True)
                #plt.xlabel(feature_list[i + 6])
                #plt.ylabel(j)
