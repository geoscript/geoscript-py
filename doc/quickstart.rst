.. _quickstart:

Quick Start
===========

Install Java
------------

A Java Runtime Environment (JRE), version greater than *1.5*, is required to run Jython and GeoScript. Chances are your system already has a JRE installed on it. A quick way to test is to execute the following from the command line::

   % java -version
   java version "1.5.0_20"
   Java(TM) 2 Runtime Environment, Standard Edition (build 1.5.0_20-b02-315)
   Java HotSpot(TM) Client VM (build 1.5.0_20-141, mixed mode, sharing)

If the command is not found or the Java version is less than 1.5 you must install a JRE. Otherwise you can continue to the next step.

A JRE can be downloaded from `Sun Microsystems <http://java.sun.com/javase/downloads/index.jsp>`_. 

  .. note:: It is possible to run GeoScript with a different non Sun JRE. However the Sun JRE is recommended as it has been thoroughly tested.

Install Jython
--------------

Jython version greater than *2.5.0* is required for GeoScript. The current version can be downloaded from http://www.jython.org/.

Install GeoScript
-----------------

#. Download `GeoScript <>`_

#. Unpack the GeoScript tarball::

     tar xzvf geoscript-0.1.tgz 

#. Change directory into the root of the unpacked tarball and execute :file:`setup.py`::

     cd geoscript-0.1
     jython setup.py install

That's it. GeoScript should now be installed on the system. To verify the install start the Jython interpreter and execute the following statement::

      % jython 
      Jython 2.5.1 (Release_2_5_1:6813, Sep 26 2009, 13:47:54) 
      [Java HotSpot(TM) Client VM (Apple Inc.)] on java1.5.0_20
      Type "help", "copyright", "credits" or "license" for more information.
      >>> import geoscript
      >>> 

If you do not get an import error congratulations! GeoScript is installed on the system.
     

