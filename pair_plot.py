#! /usr/bin/python

import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from describe import Quartile, Count
from histogram import convert_float, read_data2, freq_per_house, plot_hist


house_colors = {'Ravenclaw': 'blue', 'Slytherin': 'green', 'Gryffindor' : 'red', 'Hufflepuff' : 'yellow'}


def scatter_plot(dico, feature1, feature2, house_colors):
    list1 = dico[feature1]
    list2 = dico[feature2]
    for house in house_colors.keys():
        x = list1[house]
        y = list2[house]
        plt.plot(x, y, 'o',color = house_colors[house], label = house, markersize=0.5)
    #plt.xlabel(feature1)
    #plt.ylabel(feature2)


def pair_plot(feature_dico, feature_list, house_colors):
    n = len(feature_list)
    fig = plt.figure(figsize = (15, 15), dpi = 100)
    grid = gridspec.GridSpec(n,n)
    for k in range(n):
        for l in range(n):
            plt.subplot(grid[k,l]) 
            if k == l:
                plot_hist(feature_dico, feature_list[k], 20, house_colors)
                if k == n:
                    plt.legend(ncol = 2, fontsize = 'x-small')
            else:
                scatter_plot(feature_dico, feature_list[k], feature_list[l], house_colors)
            if k == 0:
                plt.title(feature_list[l])
            if l == 0:
                plt.ylabel(feature_list[k])
    plt.tight_layout()
    plt.show(block = True)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset to plot')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()
    feature_dico, feature_list = read_data2(args.set)
    houses = list(feature_dico[feature_list[0]].keys())

    feature_list2 = feature_list[:6]

    pair_plot(feature_dico, feature_list2, house_colors)
