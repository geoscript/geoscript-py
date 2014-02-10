.. _quickstart:

Quick Start
===========

Install Java
------------

A Java Runtime Environment (JRE), version greater than *1.6*, is required to run Jython and GeoScript. Chances are your system already has a JRE installed on it. A quick way to test is to execute the following from the command line::

   % java -version
   java version "1.6.0_26"
   Java(TM) SE Runtime Environment (build 1.6.0_26-b03-384-10M3425)
   Java HotSpot(TM) 64-Bit Server VM (build 20.1-b02-384, mixed mode)

If the command is not found or the Java version is less than 1.6 you must install a new JRE. Otherwise you can continue to the :ref:`next step <install_jython>`.

A JRE can be downloaded from `Sun Microsystems <http://java.sun.com/javase/downloads/index.jsp>`_. 

  .. note:: It is possible to run GeoScript with a different non Sun JRE. However the Sun JRE is recommended as it has been thoroughly tested.

.. _install_jython:

Install Jython
--------------

Jython version greater than *2.5.1* is required for GeoScript. The current version can be downloaded from http://www.jython.org/. After install ensure that 
the Jython :file:`bin` directory is on the path::

  export PATH=$PATH:<JYTHON_DIR>/bin

Where `<JYTHON_DIR>` is the root Jython installation directory. 

Install Setuptools
------------------

#. Download http://peak.telecommunity.com/dist/ez_setup.py

#. Run `ez_setup.py` with Jython:: 

     jython ez_setup.py

Install GeoScript
-----------------

#. Download `GeoScript <http://ares.boundlessgeo.com/geoscript/py/release/geoscript-1.2.1.zip>`_

   .. note:: Some newer features are only avaialble in the 
     `latest 1.3 build <http://ares.boundlessgeo.com/geoscript/py/release/geoscript-1.3-latest.zip>`_, which is still considered experimental.

#. Unpack the GeoScript archive::

     unzip geoscript-1.2.1.zip 

#. Change directory into the root of the unpacked archive and execute :file:`setup.py`::

     cd geoscript-1.2.1
     jython setup.py install
     
   .. note:: 
   
      Depending on your setup the install may require root privileges.

That's it. GeoScript should now be installed on the system. To verify the install execute the :command:`geoscript` command::

      % geoscript
      Jython 2.5.1 (Release_2_5_1:6813, Sep 26 2009, 13:47:54) 
      [Java HotSpot(TM) Client VM (Apple Inc.)] on java1.5.0_20
      Type "help", "copyright", "credits" or "license" for more information.
      >>> import geoscript
      >>> 

If you do not get an import error congratulations! GeoScript is installed on the system.

