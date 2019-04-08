from math import sqrt
import numpy as np

def combine (x, y):
    """
    Combine two lists of [x1, x2, x3] and [y1, y2, y3] into [[x1, y1], [x2, y2], [x3, y3].
    :param x: List of x values.
    :param y: List of y values.
    :return: List of pairs of x & y values.
    """
    return [[x['values'][i], y['values'][i]] for i in range(len(x['values']))]

def mean (values):
    """
    Calculate the mean values of a list of numbers.
    :param values: List of numbers.
    :return: Mean value of list of numbers.
    """
    return sum(values)/float(len(values))

def variance (values):
    """
    Calculate the variance of a list of numbers.
    :param values: List of numbers.
    :return: Variance of values in values.
    """
    values_mean = mean(values)
    return sum([(x - values_mean)**2 for x in values])

def covariance (x, y):
    """
    Calculate covariance between x and y
    :param x: List of x values.
    :param y: List of y values.
    :return: Covariance of x & y values.
    """
    mean_x = mean(x)
    mean_y = mean(y)
    covar = 0.0
    for i in range(len(x)):
        covar += (x[i] - mean_x)*(y[i] - mean_y)
    return covar

def coefficients (dataset):
    """
    Calculate coefficients.
    :param dataset: Dataset of x & y values.
    :return: Coefficients of a trend line for x & y values.
    """
    x = [row[0] for row in dataset]
    y = [row[1] for row in dataset]
    x_mean, y_mean = mean(x), mean(y)
    b1 = covariance(x, y)/variance(x)
    b0 = y_mean - b1*x_mean
    return [b0, b1]

def linear_regression (train, test):
    """
    Linear regression algorithm.
    :param train: Training dataset.
    :param test: Testing dataset.
    :return: Predictions for y values.
    """
    predictions = list()
    b0, b1 = coefficients(train)
    for row in test:
        yhat = b0 + b1*row[0]
        predictions.append(round(yhat, 3))
    return predictions

def rmse_metric (actual, predicted):
    """
    Calculate root mean squared error.
    :param actual: List of actual values.
    :param predicted: List of predicted values.
    :return: Root mean squared error of actual and predicted values.
    """
    sum_error = 0.0
    for i in range(len(actual)):
        prediction_error = predicted[i] - actual[i]
        sum_error += (prediction_error**2)
    mean_error = sum_error/float(len(actual))
    return sqrt(mean_error)

def evaluate_algorithm (dataset, algorithm):
    """
    Evaluate regression algorithm on training dataset.
    :param dataset: Original dataset.
    :param algorithm: Algorithm to run.
    :return: Root mean squared error, predictions, and coefficients.
    """
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

# Test functions for the straightening.
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

def linearize (x, y):
    """
    One time linearization function.
    :param x: List of x values.
    :param y: List of y values.
    :return: One iteration of straightened graph.
    """
    # Test functions to run.
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
    # For each operation, run it against the function and get RMSE.
    for op in ops:
        func = op[1]
        # noinspection PyCallingNonCallable
        new_y = func(y)
        dataset = [[x[i], new_y[i]] for i in range(len(x))]
        rmse, predictions, coeffs = evaluate_algorithm(dataset, linear_regression)
        results[op[0]] = [round(rmse, 5), new_y]
    # Select the value with the lowest RMSE.
    closest = min(results, key=results.get)
    # Return operation, it's RMSE, and the new values.
    return [closest, results[closest][1], results[closest][0]]

def linearize_complete (x, y, threshold = 0.01):
    """
    Keep running the linearize function until the RMSE is under a specific threshold.
    :param x: List of x values.
    :param y: List of y values.
    :param threshold: Threshold for highest RMSE.
    :return: New y values, RMSE, operations, and interations.
    """
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