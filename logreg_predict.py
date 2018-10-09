import csv
import argparse
import math
from describe import Mean
from matrix_class import Matrix, read_data3

def retrieve_weights(file_name):
    all_theta = read_data3(file_name)
    return all_theta
