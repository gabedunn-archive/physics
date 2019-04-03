import matplotlib.pyplot as plt
import json, sys, re

# linear regression function for coefficients.


# grab course level from args.
if len(sys.argv) < 2:
    sys.exit('specify the course level (eg. 30)')
else:
    level = sys.argv[1]

# grab unit number from args.
if len(sys.argv) < 3:
    sys.exit('specify the unit number (eg. 28.1)')
else:
    unit = sys.argv[2]

# grab whether to save as a file from args. '1' and 'true' will save an image.
if len(sys.argv) == 4:
    save = True if (sys.argv[3] == '1' or sys.argv[3] =='true') else False
else:
    save = False

# open the unit file and grab data from it.
file = f'units/{level}/{unit}.json'
with open(file) as json_file:
	# Set defaults, and load from data dict if exists.
    data = json.load(json_file)
    xkcd = True if 'xkcd' not in data else data['xkcd']
    grid = True if 'grid' not in data else data['grid']
    trend = True if 'trend' not in data else data['trend']

    # check to make sure plot exists and has x & y.
    if 'plot' not in data:
    	sys.exit('no plot specified in the file')
    if 'x' not in data['plot']:
    	sys.exit('no x data in the plot')
    if 'y' not in data['plot']:
    	sys.exit('no y data in the plot')

    # save plot to variables.
    plot = data['plot']
    x = plot['x']
    y = plot['y']

    # check that x & y have values.
    if 'values' not in x:
    	sys.exit('no x values')
    if 'values' not in y:
    	sys.exit('no y values')

    # set default titles, and use titles from dict if specified.
    xtitle = 'x' if 'title' not in x else x['title']
    ytitle = 'y' if 'title' not in y else y['title']
    title = f'{ytitle} vs. {xtitle}'



def plotter ():
    # set window title, graph title, and adjust whitespace.
    fig = plt.figure()
    fig.canvas.set_window_title(re.sub('\$', '', title)) 
    plt.title(title)
    plt.subplots_adjust(left=0.15, bottom=0.15)

  

    # set x & y axis labels
    plt.xlabel(xtitle)
    plt.ylabel(ytitle)

    # plot the trend line first so it shows underneath (if trend is true).
    if trend:
        plt.plot(x['values'], y['values'])

    # plot the data points with blue circles.
    plt.plot(x['values'], y['values'], 'bo')

    # if grid is true, turn on the grid.
    if grid:
    	plt.grid(linewidth='1')

    # if specified, save to file.
    if save:
        plt.savefig(f'Physics {level} Figure {unit}.png')

    # show the graph.
    plt.show()

# if xkcd is true, display the graph in xkcd style.
if xkcd:
    with plt.xkcd():
        plotter()
else:
    plotter()