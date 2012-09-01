.. _raster:

Working with raster data
=========================


Raster data are represented in GeoScript by the :class:`Raster` class. It contains method to access several properties of the layer and perform some common operations on it. It also contains method to access the values in the cells(pixels) of the layer.


Creating a raster layer
-----------------------

A raster layer can be created from a given raster file (mostly to be used for reading its values and performing some operation based on them) or from an array of values previously created (mostly for saving it later as a raster layer that can be opened by some other software or used with a method that needs a Raster object as input)

Classes derived from :class:`Raster` can be used to open a particular type of raster layer file. Two of the most common ones are :class:`GeoTIFF` and :class:`WorldImage`.

::

    >>> from geoscript.layer import GeoTIFF, WorldImage
    >>> gtiff = GeoTIFF('dem.tif')
    >>> wi = WorldImage('image.tif')
    ...

.. note::

    Other classes exist for opening different file formats, and they are used much in the same way. Check the GeoScript API for more information


To create a raster layer from an array of data values, the static method *create* from :class:`Raster` is used.
The next example shows how to create a small raster layer with random values.

::

    >>> from geoscript.layer import Raster
    >>> import random
    >>> size = 10 # the size to be used for both dimensions of the data matrix
    >>> data = [][]
    >>> for x in range(size):
    >>>    for y in range(size):
    >>>	      data[x][y] = random.random()
    >>> Raster.create(data, bounds, nbands = 1)
    ...

    
.. note::
    
    The layer we have created is small enough to be stored in memory. Larger layers might need an array larger than the amount of data that can be stored in memory, so they could not be created that way. Classes for handling those cases might be added to GeoScript in the future, but currently there is no special support for them.

Notice that we have to pass the number of layers explicitly. Also, the method needs a :class:`Bounds` object to know where exactly this layer is located. This extent, along with the dimensions of the matrix, allows to calculate parameters such as pixel size (cell size).

Once we have created a layer, there are several methods to get more information about it and work with it. For instance, we can get the extent covered by a raster layer, as a Bounds object, and it size in pixels. The following example shows how this can be used to create another random layer, but this time covering the same extent as a previous one and with the same pixel size. (For the following examples, we assume that `gtiff` is the GeoTIFF layer created in the first example)


::

    >>> width, height = gtiff.getsize()
    >>> data = [][]
    >>> for x in range(width):
    >>>    for y in range(height):
    >>>	      data[x][y] = random.random()
    >>> Raster.create(data, gtiff.getextent(), nbands = 1)


Operations on a raster layer 
--------------------------------

We can query a raster layer in several ways to know the value at any location within it extent. The simplest way of doing it is using the :meth:`getvalueatcoord` method, passing a real world coordinate.

::

    >>> gtiff.getvalueatcoord(8.5, 4.46)
    1222.7
    
    
However, if you want to run some analysis on the layer that needs to access a large part of its extent sistematically, it is a better idea to query the layer in a per-cell basis. The :meth:`getvalueatcell` method should be used for that. Its  `x` and `y` parameters represent in this case the column and row of the pixel whose value is to be returned.

::

    >>> gtiff.getvalueatcoord(3, 3)
    655.9    

    
Querying the layer using a real coordinate is usually slower than using a cell coordinate, since it involves interpolation calculations.

Both methods accept a third parameter called *band* indicating the band to be used to query the layer. If it is not used, as in the cases above, the first band (band = 0) is used.

Also, both methods will return a special value called the *no-data value* if the coordinate falls outside the extent of the layer. Although the passed coordinate is not suitable to be applied to this layer, GeoScript will not throw an exception, but return this value instead. The no-data value is used whenever the query cannot be answered because there is no data on that given cell or point. 

Each layer has its own no-data value (it has to be a value that cannot be used for a "normal" value of the variable represented in the raster layer), and the :meth:`getnodatavalue` method returns that value.

::

    >>> gtiff.getnodatavalue()
    -32768


With the above methods we can perform a small analysis on our `gtiff` layer with just a few lines of code. The following example calculates the maximum and minimum values of the layer (a method named *extrema* can be used as well. It returns a (min,max) tuple and it will be much faster than this little piece of code, since calculations are done at a lower level. However, this is added here for the sake of showing a simple example about how to use GeoScript raster methods)

.::

    >>> width, height = gtiff.getsize()
    >>> min = max = gtiff.getvalueatcell(0, 0)
    >>> for y in range(height):
    >>>    for x in range(width):  
    >>>		value = gtiff.getvalueatcell(x,y)
    >>>		min = min(value, min)
    >>>		max = max(value, min)
    >>> min
    XXXX
    >>> max
    XXXXX

    
This code can be improved to be more robust and to handle special values. Although :meth:`getvalueatcell` and :meth:`getvalueatcoord` return the no-value data when queried outside of the layer's bounding box, they might also return it for an interior point, since the no-data value might be used in the layer to indicate that there is no data for a given cell. (some processes migth use it as well to leave out certain cells, or to indicate that the result of the process could not be computed. For instance, a process calculating aspect from a Digital Elevation Model will not be able to calculate the aspect of a flat area, and will assign the no-data value to that location in the output aspect layer). Since no-data values should not be considered for our minimum and maximum calculation, we should handle them separately.
 
The :meth:`isnodatavalue` method comes very handy for checking whether a value is valid or not. Here is the improved version of the previous algorithm.

::

    >>> width, height = gtiff.getsize()
    >>> min = max = gtiff.getnodatavalue();
    >>> for y in range(height):
    >>>    for x in range(width):  
    >>>	      value = gtiff.getvalueatcell(x,y)
    >>>       if not gtiff.isnodatavalue(value):
    >>>          if min != gtiff.getnodatavalue():
    >>>	            min = min(value, min)
    >>>		    max = max(value, min)
    >>>          else:
    >>>             min = max = value
    >>> min
    XXXX
    >>> max
    XXXXX

 
Although you can create you own algorithms, if they are going to be applied to large datasets or contain some complex analysis, it is always better to rely on an external algorithm. Since GeoScript can access a large collection of algorithms (meaning that, whatever you want to do, you will most likely find a process that already does it, or a combination of them that produces the result you are looking for), it is better to use it to create a workflow and let those algorithms do the actual computation. See the :ref:`Processing geospatial data with GeoScript <processing>` section to know more about this powerful feature of GeoScript.