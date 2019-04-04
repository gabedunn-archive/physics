from math import sqrt
import numpy as np

def combine (x, y):
    return [[x['values'][i], y['values'][i]] for i in range(len(x['values']))]

# calculate the mean value of a list of numbers.
def mean (values):
    return sum(values)/float(len(values))

# calculate the variance of a list of numbers.
def variance (values, mean):
    return sum([(x - mean)**2 for x in values])

# calculate covariance between x and y.
def covariance (x, mean_x, y, mean_y):
    covar = 0.0
    for i in range(len(x)):
        covar += (x[i] - mean_x)*(y[i] - mean_y)
    return covar

# calculate coefficients.
def coefficients (dataset):
    x = [row[0] for row in dataset]
    y = [row[1] for row in dataset]
    x_mean, y_mean = mean(x), mean(y)
    b1 = covariance(x, x_mean, y, y_mean)/variance(x, x_mean)
    b0 = y_mean - b1*x_mean
    return [b0, b1]

# linear regression algorithm.
def linear_regression (train, test):
    predictions = list()
    b0, b1 = coefficients(train)
    for row in test:
        yhat = b0 + b1*row[0]
        predictions.append(round(yhat, 3))
    return predictions

# calculate root mean squared error.
def rmse_metric (actual, predicted):
    sum_error = 0.0
    for i in range(len(actual)):
        prediction_error = predicted[i] - actual[i]
        sum_error += (prediction_error**2)
    mean_error = sum_error/float(len(actual))
    return sqrt(mean_error)

# evaluate regression algorithm on training dataset.
def evaluate_algorithm (dataset, algorithm):
    test_set = list()
    for row in dataset:
        row_copy = list(row)
        row_copy[-1] = None
        test_set.append(row_copy)
    predicted = algorithm(dataset, test_set)
    actual = [row[-1] for row in dataset]
    rmse = rmse_metric(actual, predicted)
    coeffs = coefficients(dataset)
    return [rmse, predicted, coeffs]

# functions for the straightening.
def y_exp_3 (y):
    return np.array(y, dtype=float)**3

def y_exp_2 (y):
    return np.array(y, dtype=float)**2

def y_exp_1 (y):
    return np.array(y, dtype=float)

def root_y (y):
    return np.sqrt(np.array(y, dtype=float))

def log_y (y):
    return np.log(np.array(y, dtype=float))

def inverse_y (y):
    return 1/np.array(y, dtype=float)

def inverse_y_exp_2 (y):
    return 1/np.array(y, dtype=float)**2

def inverse_y_exp_3 (y):
    return 1/np.array(y, dtype=float)**3

# one time linearization function.
def linearize (x, y):
    ops = list(
        {
            'y^3': y_exp_3,
            'y^2': y_exp_2,
            'y': y_exp_1,
            'sqrt(y)': root_y,
            'log(y)': log_y,
            '1/y': inverse_y,
            '1/y^2': inverse_y_exp_2,
            '1/y^3': inverse_y_exp_3
        }.items()
    )
    results = {}
    for op in ops:
        func = op[1]
        # noinspection PyCallingNonCallable
        new_y = func(y)
        dataset = [[x[i], new_y[i]] for i in range(len(x))]
        rmse, predictions, coeffs = evaluate_algorithm(dataset, linear_regression)
        results[op[0]] = [round(rmse, 5), new_y]
    closest = min(results, key=results.get)
    return [closest, results[closest][1], results[closest][0]]

# keep running the linearize function until the rmse is under a specific threshold.
def linearize_complete (x, y, threshold = 0.01):
    iterations = 0
    manipulations = list()
    y_values = list()
    rmse = threshold + 1
    new_y = y

    while rmse > threshold:
        operation, y_values, rmse = linearize(x, new_y)
        new_y = y_values
        manipulations.append(operation)
        iterations += 1

    if manipulations[-1] == 'y':
        iterations -= 1

    return [y_values, rmse, manipulations, iterations]