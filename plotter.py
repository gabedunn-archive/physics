import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from linearize import coefficients, combine, linearize_complete, rmse_metric
import json, sys, re, os
import argparse

# set up some options and save them to variables.
parser = argparse.ArgumentParser(description='Plot a graph based on the input file and specified options.')

# Main argument - the json file with all the required data.
parser.add_argument('file', metavar='file', type=str,
                    help='a file to pull data from')
# Linearize the graph if specified.
parser.add_argument('-l', '--linearize', dest='linearize', action='store_const',
                    const=True, default=False,
                    help='Show a second, linearized graph.')
# Save the graph to a png file if specified.
parser.add_argument('-s', '--save', dest='save', action='store_const',
                    const=True, default=False,
                    help='Save the graph to a png file.')
# Show only the linearized graph. Only valid if -l is specified.
parser.add_argument('-o', '--only', dest='only', action='store_const',
                    const=True, default=False,
                    help='Show only the linearized graph. Only valid if -l is specified.')
# RMSE threshold to consider a line straightened.
parser.add_argument( '-r', '--rmse', default='0.01',
                     help='RMSE threshold to consider a line straightened.')
# Disable the xkcd style of the graph.
parser.add_argument('-x', '--xkcd', dest='xkcd', action='store_const',
                    const=True, default=False,
                    help='Disable the xkcd style of the graph.')
# Disable the grid lines on the graph.
parser.add_argument('-g', '--grid', dest='grid', action='store_const',
                    const=True, default=False,
                    help='Disable the grid lines on the graph.')
# Disable the trend line on the graph.
parser.add_argument('-t', '--trend', dest='trend', action='store_const',
                    const=True, default=False,
                    help='Disable the trend line on the graph.')
# Disable the line connecting the data points on the graph.
parser.add_argument('-c', '--connecting', dest='connecting', action='store_const',
                    const=True, default=False,
                    help='Disable the line connecting the data points on the graph.')

# Parse the args and assign them to variables.
args = parser.parse_args()

file = args.file
save = args.save
threshold = float(args.rmse)
linearize = args.linearize
linear_only = args.only
xkcd_override = args.xkcd
grid_override = args.grid
trend_override = args.trend
connecting_line_override = args.line

# If the file doesn't exists, exit. Otherwise, set the png filename to the file path with png extension.
if not Path(file).is_file():
    sys.exit(f'{file} does\'t exist.')
else:
    filename = 'Figure ' + re.sub('\.json$', '.png', os.path.basename(file))

# Open the json file and grab the data from it.
with open(file) as json_file:
    # Check for overrides, and if present, set values false. Otherwise, check for presence in data. Otherwise assign the default.
    data = json.load(json_file)
    xkcd = False if xkcd_override else True if 'xkcd' not in data else data['xkcd']
    grid = False if grid_override else True if 'grid' not in data else data['grid']
    trend = False if trend_override else True if 'trend' not in data else data['trend']
    line = False if connecting_line_override else True if 'line' not in data else data['line']

    # Check to make sure plot exists and has x & y.
    if 'plot' not in data:
        sys.exit('No plot specified in the file.')
    if 'x' not in data['plot']:
        sys.exit('No x data in the plot.')
    if 'y' not in data['plot']:
        sys.exit('No y data in the plot.')

    # Save plot to variables.
    plot = data['plot']
    x = plot['x']
    y = plot['y']

    # Check that x & y have values.
    if 'values' not in x:
        sys.exit('No x values')
    if 'values' not in y:
        sys.exit('No y values')

    # Combine x & y values into one list of pairs.
    dataset = combine(x, y)

def plotter (x, y, linearize):
    """
    :param x: List of x values.
    :param y: List of y values.
    :param linearize: Whether or not the line is linearized.
    :return: Nothing.
    note::  Plot the graph given the specified variables.
    """

    # Set titles from x & y variables. If they don't exists, default to 'x' & 'y'.
    xtitle = 'x' if 'title' not in x else x['title']
    ytitle = 'y' if 'title' not in y else y['title']
    title = f'{ytitle} vs. {xtitle}'

    # Save the figure into a variable.
    fig = plt.figure()
    # Set the window title to a readable format. Removes slashes and replaces \to with arrows.
    fig.canvas.set_window_title(re.sub('(\$)|(\\\)', '', re.sub('(\\\\to)', '→', title)))
    plt.title(title)
    # Adjust whitespace on the graph.
    plt.subplots_adjust(left=0.15, bottom=0.15)

    # Set x & y axis labels
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)

    # If specified, plot the trend line first so it is underneath the rest of the data. Don't plot if linearized.
    if trend and not linearize:
        # Get the coefficient of the trend line.
        b0, b1 = coefficients(dataset)
        # Set trend_y to each y value multiplied by b1 & added to b0.
        trend_y = np.array(x['values'])*b1 + b0
        # Calculate root mean squared error between y values and the trend line.
        rmse = rmse_metric(y['values'], trend_y)
        # Plot the trend line in red.
        plt.plot(x['values'], trend_y, 'r')
        # Put a dot at the beginning and end of the trend lone.
        plt.plot([x['values'][0], x['values'][-1]], [trend_y[0], trend_y[-1]], 'ro')

    # If specified, plot the connecting line before data points so it shows above them.
    if line:
        # Plot the connecting line first.
        plt.plot(x['values'], y['values'], 'b', label=ytitle)
        # Plot data points as blue circles second.
        plt.plot(x['values'], y['values'], 'bo')
    else:
        # Simply plot the data points without a connecting line.
        plt.plot(x['values'], y['values'], 'bo', label=ytitle)

    # If specified, turn on the grid.
    if grid:
        plt.grid(linewidth='1')

    # If specified, save graph to png file.
    if save:
        # Add linearized to filename if graph is linearized.
        if linearize:
            plt.savefig(f'Linearized {filename}')
        else:
            plt.savefig(filename)

    # Show plot legend.
    plt.legend()

    # Finally, show the graph.
    plt.show()

# Define function to plot graph with xkcd style if specified.
def use_xkcd(x, y, linearize, xkcd):
    """
    :param xkcd: Whether or not to use the xkcd style.
    :return: Nothing.
    note:: Plot in xkcd style if specified, otherwise plot normally.
    """
    if xkcd:
        with plt.xkcd():
            plotter(x, y, linearize)
    else:
        plotter(x, y, linearize)

# Print some information about whether the graph can be straightened.
# Grab the coefficient of the trend line.
b0, b1 = coefficients(dataset)
# If use a '+' if b0 is positive, otherwise use a '-'.
separator = '+' if b0 >= 0 else '-'
b0 = b0 if b0 >= 0 else -b0
# Calculate root mean squared error of the trend line.
trend_y = np.array(x['values'])*b1 + b0
rmse = rmse_metric(y['values'], trend_y)
# If rmse is below the threshold, show that the line is straight.
straight = True if rmse < threshold else False

# Print the data to the console.
dash_line = '----------------------------------------'
print(dash_line)
print(f'Trend Line (LBF):   {round(b1, 3)}x {separator} {round(b0, 3)}')
print(f'Trend Line RMSE:    {round(rmse, 4)}%')
print(f'Line is Straight:   {straight}')
# If the line isn't straight, straighten in and show the process.
if not straight:
    # Grab y values, rmse, operations, and iterations of the straightened line.
    y_values, straight_rmse, manipulations, iterations = linearize_complete(x['values'], y['values'], threshold)
    # Join the manipulations into one string.
    manipulations_string = ' → '.join(manipulations)
    # Display this data to the console.
    print(f'To Straighten:      {manipulations_string}')
    print(f'Straightened RMSE:  {round(straight_rmse, 4)}%')
    print(f'Iterations:         {iterations}.')
    print('Y Values After Straightening:')
    print(f'{y_values}')
    # Prompt to linearize data if not already doing so.
    if not linearize:
        print(f'To graph the linearized version, run the command with \'-l\' appended.')
print(dash_line)


# If linearize isn't specified, just show the graph. Otherwise, decide how to show the linearized graph.
if not linearize:
    use_xkcd(x, y, False, xkcd)
else:
    # If linear_only isn't specified, show the initial graph first, only if graph isn't initially straight.
    if (not linear_only) and (not straight):
        use_xkcd(x, y, False, xkcd)
    # If the graph is already straight, simply display it.
    if straight:
        # Set the title to show that it was already straight.
        y['title'] += ' (Already Straight)'
        use_xkcd(x, y, False, xkcd)
    else:
        # Grab the y values, rmse, operations, and iterations from the straightened graph.
        y_values, straight_rmse, manipulations, iterations = linearize_complete(x['values'], y['values'], threshold)
        # Join the manipulations into one string and add it to the y title.
        manipulations_string = '$' + ('\ \\to\ '.join(manipulations)) + '$'
        y['title'] = y['title'] + ' $\\to$ ' + manipulations_string
        # Assign new values to y.
        y['values'] = y_values
        # Display the graph.
        use_xkcd(x, y, True, xkcd)
