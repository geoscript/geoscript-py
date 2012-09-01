.. _external:

Installing external geoprocessing applications
===============================================

This section describes how to install external applications that can be called from GeoScript to provide geoprocessing capabilites. These applications are not included as part of GeoScript, and must be downloaded separately.

Currently, two applications are used by GeoScript to extend its collection of geoprocesses: SAGA and GRASS.

SAGA
-----

SAGA algorithms are called by GeoScript usign its command line version ``saga_cmd``. To install SAGA, follow the next steps.

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


-If you are running Linux *********+


