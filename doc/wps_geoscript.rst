.. _Exposing GeoScript processes:

Exposing GeoScript processes
=============================

The real power of GeoScript as a scripting engine to define workflows comes when those workflows are exposed through GeoServer. Processes written in GeoScript (whether with their analysis procedures purely based on GeoScript or reusing other available processes) can be easily incorporated to GeoServer and exposed through its WPS capabilities. GeoScript is the easiest way of configuring and expanding the analytical capabilities of GeoServer.


Wrapping and simplyfing existing processes
--------------------------------------------

An easy and interesting thing that you can do is to wrap an existing process and expose a simplified version of it. This is specially interesting for processes coming from external application, mainly for two reasons. The first one is that those algorithms are not exposed by default, like GeoTools ones, since GeoServer knows nothing about those application that provide these processes. It is GeoScript who knows about them, but since GeoServer supports GeoScript, you can make GeoServer aware of a process just creating the corresponding script as we saw before. Second, most of those external algorithms come from applications that are a bit too technical many users, with a large number of configuration parameters that require a certain knowledge of the process. You can set fixed-values for some of these parameters, hiding them from the user (the person using the exposed WPS service)

Here's an example that exposes the ``saga:slopeaspectcurvature`` algorithm that we already know, with no simplifying at all.

.::

	def slopeaspect(elevation, method):


Now suppose that you want to expose a method that calculates slope, and make it as simple as possible. Below you have a simplified version that just takes an elevation layer as input, but no method, and that only generates the slope layer. Internally, the algorithm is identical, since it calls the same process, but externally it will look much simpler and maybe easier and more practical to integrate into a web application.

.::

	def slope(elevation, method):
	
