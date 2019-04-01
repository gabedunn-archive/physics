import matplotlib.pyplot as plt
import json

with open('unit28.1.json') as json_file:
    data = json.load(json_file)
    xkcd = data['xkcd']
    grid = data['grid']
    values = data['plots']

def plotter ():
    # grab data from dictionary and add it to the plot
    plt.plot(values[0]['x']['values'], values[0]['y']['values'], 'bo')
    plt.xlabel(values[0]['x']['title'])
    plt.ylabel(values[0]['y']['title'])

    # if grid is true, turn on the grid
    if grid:
        plt.grid()

    # show the grid
    plt.show()

# if xkcd is true, display the graph in xkcd style
if xkcd:
    with plt.xkcd():
        plotter()
# otherwise, display it normally
else:
    plotter()