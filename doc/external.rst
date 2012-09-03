.. _external:

Installing external geoprocessing applications
===============================================

This section describes how to install external applications that can be called from GeoScript to provide geoprocessing capabilites. These applications are not included as part of GeoScript, and must be downloaded separately.

Currently, two applications are used by GeoScript to extend its collection of geoprocesses: SAGA and GRASS.

SAGA
-----

SAGA algorithms are called by GeoScript using its command line version ``saga_cmd``. To install SAGA, follow the next steps.

- If you are running Windows, download SAGA from http://saga-gis.org
- Unzip the content of the downloaded file to a folder you select (let's say ``c:\saga``)
- Add thar folder to the PATH environment variable 
- To check that everything is OK, open a console (Windows key + R, then type ``cmd`` and press Enter) and type ``saga_cmd``. You should see something like this.

:: 

	_____________________________________________
	  #####   ##   #####    ##
	 ###     ###  ##       ###
	  ###   # ## ##  #### # ##
	   ### ##### ##    # #####
	##### #   ##  ##### #   ##
	_____________________________________________


	error: module library

	available module libraries:
	- contrib_a_perego.dll
	- docs_html.dll
	- docs_pdf.dll
	- garden_3d_viewer.dll
	- garden_webservices.dll
	- geostatistics_grid.dll
	- geostatistics_kriging.dll
	- geostatistics_points.dll
	.
	.
	.


-If you are running Linux, packages are available from https://launchpad.net/~johanvdw/+archive/saga-gis
-After installing, just make sure that the command line version of SAGA is available, by running ``saga_cmd`` from a console.

In all cases, SAGA 2.0.8 is recommended, as it is the only version tested and supported for running from GeoScript.

GRASS
-----

GRASS modules are available as GeoScript processes unider both Windows and Linux. The way GeoScript calls GRASS is, however, different depending on the Operating System, and different configuration is needed.

-If you are running Linux, just install GRASS the usual way, as explained at http://grass.osgeo.org/wiki/Installation_Guide
-Make sure that GRASS is installed by running ``grass`` in a console. You are ready to go, as no further configuration is needed. 

-If you are running Windows, install a native WinGRASS package from http://grass.osgeo.org/grass64/binary/mswindows/native/
-Add an environment variable named ``GRASS_BIN_PATH`` and set it to the folder where GRASS is installed
-Add an environment variable named ``GRASS_SHELL_PATH`` and set it to the folder where the shell interpreter is installed (usually an ``msys`` folder at the same level as the GRASS folder)

GRASS funcionality has been tested with GRASS 6.5.2, and that is the recommended version to use.

.. note::

	VICTOR: By default, the GRASS binding is configured to work with projected data, not LatLon. I Have to think about the best way to let the user configure this...
