#! /usr/bin/python

import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from describe import Quartile, Count, Mean
from histogram import read_data2, freq_per_house

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
    grid = gridspec.GridSpec(4,4)
    
    for k in range(len(feature_list)):
        xy_dico = freq_per_house(feature_dico[feature_list[k]], 20)
        if k <4:
            l = k
        else:
            m = k//4
            l = k - 4*m
        
        plt.subplot(grid[m, l])
        
        for house in houses:
            x = xy_dico[house]['x']
            y = xy_dico[house]['y']
            plt.fill(x, y, color= house_colors[house], linewidth=2, label = house, alpha = 0.5)
        plt.xlim(Quartile(x,0),)
        plt.ylim(Quartile(y,0),)
        plt.title(feature_list[k])
        plt.legend(ncol = 2, fontsize = 'x-small')
    plt.tight_layout()
    plt.show(block = True)





