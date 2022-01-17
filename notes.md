# Issues
* No issues.

# New features
* Series.index, returns the index of the series in an array.
* Series.values, returns the values of the series in an array.
* Series.size, return the size of the series.
* Series.add, to add or replace a series item.
* Series.reindex, reindex series given a new index.
* Series.sort_index, reindex series based on index.

# Pseudocode
1. ??

# Image code
`import matplotlib.pyplot as plt`

`plt.rcParams["figure.figsize"] = [7.00, 3.50]`

`plt.rcParams["figure.autolayout"] = True`

`im = plt.imread('bird.jpg') # insert local path of the image.`

`fig, ax = plt.subplots()`

`ax.plot(range(10))`

`newax = fig.add_axes([0.8,0.8,0.2,0.2], anchor='NE', zorder=1)`

`newax.imshow(im)`

`newax.axis('off')`

`plt.show()`
