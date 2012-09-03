.. _mixing:

Mixing Java and GeoScript code
===============================

To develop new processes and enrich you web services you can use both Java and GeoScript code at the same time, each of them as we have already seen in previous sections. While Java is best suited for implementing the actual processing part, GeoScript is better to reuse those processes with easier and more practical Python or Javascript code.

The following example shows how to add a supervised classification process based on two simple Java processes and a bit of GeoScript code to link them together. The whole process could have been put into a single Java class, but doing it this way makes it easier to reuse the created subprocesses in a different context (as we will see later in this tutorial)


Java code
----------

Here is the Java code of the first process, which takes a raster layer and a vector one, and calculate statistics of raster layer values in pixels occupied by the vector layer features. It also takes the name of a field, so geometries with the same value for that field are considered part of the same class and searate statistics for each classes can 

::

	





It basically translates geometries to cells in the raster layer (differently depending on the type of geometry) and returns an maps with values of mean and standard deviation for the different classes and bands in the raster layer.

The second process performs a paralellpiped classification based on the previous image, and its Java code is as follows.

::



The process returns a new raster layer with classified pixels, or no-data values for pixels that did not belong to any of the classes defined by the input values.

Now, if we add these processes copying the corresponding Java files to our GeoServer folder, we will have them available. Linking them into a single process can be done with the following GeoScript code.

::


And copying the file with this code we will have the global algorithm also exposed.


The first process can be reused if we later implement another classification process. For instance, the following code implements a min-dist-to-mean classificacion algorithm. 



Although the algorithm itself is different, the process is identical in its semantic, so it can be connected to the process that calculate statistics much in the same way as in the first example.



