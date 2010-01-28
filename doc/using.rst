.. _using:

Using GeoScript
===============

The fastest way to run GeoScript is to follow the :ref:`quickstart` and run the :command:`geoscript` command. But more often than not GeoScript will be used from an existing program.

Like any other Python library GeoScript is imported into existing programs. However GeoScript is special in that it relies on the GeoTools libraries being available. The GeoTools libraries are shipped as Java archive (jar) files and are made available to GeoScript using the ``CLASSPATH``. 

CLASSPATH Explained
-------------------

In Java the ``CLASSPATH`` is a path variable that enumerates locations from which Java classes can be loaded. It is the equivalent of ``sys.path`` in Python. Actually in Jython the ``CLASSPATH`` becomes parrt of ``sys.path``.

The ``CLASSPATH`` is how the GeoTools libraries are made available to GeoScript.When the :command:`geoscript` command is invoked it does two things:

 #. It generates the ``CLASSPATH`` from all the necessary GeoTools jars
 #. It invokes the Jython interpreter

.. note::

   Because of the way GeoTools works internally GeoScript can only function if the ``CLASSPATH`` is set before Jython is invoked.

The :command:`geoscript` command relies on the fact that all the required GeoTools jars are shipped with the GeoScript library itself.

Importing GeoScript
-------------------

As stated above the way a library like GeoScript is typically used by importing it into an existing program. When this is the case it is the job of the user to ensure that the ``CLASSPATH`` has been appropriatly initialized as discussed in the previous section.

Consider the following::

  % jython
  Jython 2.5.1 (Release_2_5_1:6813, Sep 26 2009, 13:47:54) 
  [Java HotSpot(TM) 64-Bit Server VM (Apple Inc.)] on java1.6.0_15
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import geoscript
  Error: Could not find GeoTools libraries on classpath.
  
When this occurs it means the ``CLASSPATH`` has not been properly setup. The :command:`geoscript-classpath` command can prove useful in this regard. When invoked the command will output the ``CLASSPATH`` built from the GeoTools jars shipped with GeoScript. Users can use this output to set the ``CLASSPATH`` for whatever environment is being worked in.

Consider again::

  % CLASSPATH=`geoscript-claspath`
  % export CLASSPATH
  % jython
  Jython 2.5.1 (Release_2_5_1:6813, Sep 26 2009, 13:47:54) 
  [Java HotSpot(TM) 64-Bit Server VM (Apple Inc.)] on java1.6.0_15
  Type "help", "copyright", "credits" or "license" for more information.
  >>> import geoscript
  >>> geoscript
  <module 'geoscript' from 'geoscript/__init__$py.class'>

In this case the ``CLASSPATH`` has been properly setup and GeoScript successfully imported. 

The method for setting the ``CLASSPATH`` will differ depending on the environment. For instance when developing a web application setting the ``CLASSPATH`` can depend on the web container being used. 
