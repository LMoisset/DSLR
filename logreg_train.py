#! /usr/bin/python
import csv
import argparse
import math
from describe import Mean
from matrix_class import Matrix, read_data3


def cat_to_dummies(X, features, all_cat = True):
    ind_to_drop = []
    for i in range(X.ncol):
        cat = X.unique(i, axis = 1)
        if len(cat) <5: # si moins de 5 uniques, on assume que la var est cat
            ind_to_drop.append(i)
            if all_cat == True:
                for j in range(len(cat)):
                    new_cat = features[i] + '_' + cat[j]
                    new_col = [1 if x == cat[j] else 0 for x in [row[i] for row in X]]
                    X.append_col(new_col)
                    features.append(new_cat)
            else:
                for j in range(len(cat)-1):
                    new_cat = features[i] + '_' + cat[j]
                    new_col = [1 if x == cat[j] else 0 for x in [row[i] for row in X]]
                    X.append_col(new_col)
                    features.append(new_cat)
    X = X.drop(ind_to_drop, axis = 1)
    features = [features[i] for i in range(len(features)) if i not in ind_to_drop]
    return X, features

def impute_na(X): # pour l'instant mean imputation
    return Matrix([[Mean([row[i] for row in X]) if row[i] =='' else row[i] for i in range(X.ncol)] for row in X])

def preprocess(dataname):
    df = read_data3('../data/'+dataname)
    Y = df.col(1)
    Y = Y.drop([0], axis = 0)

    # We saw in the data viz scatter plot part that Astronomy and Defense against
    # the dark arts seemed to be extremely similar. We therefore can try predicting
    # without one of them (Astronomy).

    # We also saw with the histograms that Arithmancy and Care of Magical Creatures
    # have a similar repartition in each house, thus only adding noise when trying
    # to predict, so we can try without them.
    X = df.drop([0,1,2,3,4, 6, 7], axis = 1) # get rid of index, house, firstname,
    # lastname, birthday, arithmancy, astronomy, care of magical creatures


    features = X[0]
    X = X.drop([0], axis = 0)
    X = X.to_float()
    X_2, features = cat_to_dummies(X, features, all_cat = False) # handle categorical variables
    #print(X_2.count_null())
    X_3 = impute_na(X_2) # get rid of missing values
    X_4 = X_3.standardize()
    #print(X_3.count_null())
    # get rid of correlated data
    Y, y_name = cat_to_dummies(Y, ['House'], all_cat = True)
    return X_4, Y, features, y_name


def g(z):  # z est une matrix de dim 1/1
    return 1 / float(1 + math.exp(-z[0][0]))

def h(X, theta): # X is here an individual transformed into a lign / theta une colonne
    return g(Matrix(X.dot(theta)))

def loss_function(X, Y, theta): # X is an array, Y a column array
    m = len(Y)
    J = 0
    for i in range(m):
        J += -1/m * (Y[i][0]*math.log(h(X.row(i), theta)) + (1-Y[i][0])*math.log(1-h(X.row(i), theta)))
    return J

def delta(X, Y, theta, j): # X is an array, Y a column array
    m = len(Y)
    dJ = 0
    for i in range(m):
        dJ += 1/m*(h(X.row(i), theta) - Y[i][0])*X[i][j]
    return dJ

def gradient(X, Y, theta):
    return Matrix([[delta(X,Y,theta,j)] for j in range(X.ncol)])


def gradient_descent(X, Y, num_iter, learning_rate):
    theta = Matrix([[0] for i in range(X.ncol)])
    for i in range(num_iter):
        grad = gradient(X,Y,theta)
        theta = theta.sub(grad.product(learning_rate))
        if i % 500 == 0:
            print('Loss Function after '+ str(i)+' iterations : ', loss_function(X,Y,theta))
    print('Final Loss function : ', loss_function(X,Y,theta))
    return theta


def write_csv(file, columns, file_name):
    with open('../data/' + str(file_name) + '.csv', mode='w') as output:
        weights = csv.writer(output, lineterminator = '\n')
        weights.writerow(columns)
        for line in file:
            weights.writerow(line)


def one_vs_all_fit(X, Y, y_name, num_iter, learning_rate):
    all_theta = gradient_descent(X, Y.col(0), num_iter, learning_rate)
    for i in range(1, Y.ncol):
        all_theta.append_col(gradient_descent(X, Y.col(i), num_iter, learning_rate).to_list())
    write_csv(all_theta, y_name, 'theta_weights')
    return all_theta


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Dataset you want to describe')
    parser.add_argument('set', type = str, help = 'Name of the file to read')
    args = parser.parse_args()

    X, Y, features, y_name = preprocess(args.set)
    all_theta = one_vs_all_fit(X,Y, y_name, 1000, 0.1)








    #theta = gradient_descent(X,Y, 10000, 0.1)
    #print(theta)
    #print(gradient(X,Y, theta).product(0.01))
    #print(gradient_descent(X,Y, 100, 0.01))
    #X.row(508).show()
    #theta = Matrix([[0] for i in range(X.ncol)])
    #print(loss_function(X,Y,theta))
    #print(h(X, theta))
    #print(delta(X,Y, theta, 0))

    #print(gradient_descent(X,Y,100, 0.01))
    #Y.col(0).show()
    #print(gradient_descent(X,Y, 1000, 0.1))

    #print(features)
    #theta = Matrix([[1],[2],[3]])
    #X = Matrix([[4], [5], [6]])
    #theta.transpose().dot(X).show()
    #theta2 = Matrix([[1]])
    #theta2.product(-1).Exp().show()
    #print(h(X, theta))
    #print(h(theta,X))
    #print(X)
    #print(Y)
    #print(Y[0])
    #print(X[0])
    #print(X[[0]][0])
    #print(len(X))
    #print(gradient_descent(X,Y1, 10000, 0.01))

    # ENEVER LES COLONNES INUTILES UNE FOIS que cela marche hhoho
