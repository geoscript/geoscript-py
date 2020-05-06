.. _devel:

Developing with GeoScript
=========================

This section describes how to set up a GeoScript development environment.

Install Jython
--------------

Jython version 2.7.2 or greater is required for GeoScript.

* Install `Jython <http://www.jython.org/downloads.html>`_

  For the remainder of the document the Jython installation root will be referred to as ``JYTHON_HOME_DIR``.

Install setuptools 
------------------

#. Downlaod `ez_setup.py <http://peak.telecommunity.com/dist/ez_setup.py>`_
#. Execute :file:`ez_setup.py` with the :command:`jython` command::

     $ <JYTHON_HOME_DIR>/bin/jython ez_setup.py

  Upon success :file:`<JYTYON_HOME>/bin/easy_install` will be created.

Install virtualenv
------------------

  .. note:: 

     Creating a virtualenv for GeoScript is not neccessary but is highly recomended.

#. Using :file:`easy_install` installed in the previous section easy install the virtualenv library::

    $ <JYTHON_HOME_DIR>/bin/easy_install virtualenv

#. Create a new virtualenv named ``geoscript``::

    $ <JYTHON_HOME_DIR>/bin/virtualenv geoscript

#. Activate the ``geoscript`` virtualenv::

    $ source geoscript/bin/activate

Obtain Source Code
------------------

The GeoScript sources are stored in a git repository hosted at github. 

#. Install `git <http://git-scm.com/>`_
#. Clone the ``geoscript`` git repository::

     (geoscript)$ git clone git://github.com/jdeolive/geoscript-py.git

Obtain GeoTools Libraries
-------------------------

GeoScript requires the GeoTools libraries to function. There are a number of ways to obtain them.

Maven
^^^^^

If `Apache Maven <>`_ is installed on the system execute the following command from the root of the local git repository::

   $ mvn install

Upon success the required GeoTools libraries will be located in the :file:`jars` directory.

Ant
^^^

If `Apache Ant <>`_ is installed on the system execute the :command:`ant` comand from the root of the local git repository::

  $ ant

Upon success the required GeoTools libraries will be located in the :file:`jars` directory.

Download
^^^^^^^^

If neither of the above methods are appealing: 

#. Download the latest GeoTools 2.6 release
#. Unpack the zip archive
#. Copy :file:`geotools-2.6.?/*.jar` into the :file:`jars` directory

Setup the CLASSPATH
-------------------

Once the GeoTools libraries are located in the :file:`jars` directory source the :file:`classpath` file located in the root the local git repository::

  $ source classpath

Install Python Dependencies
---------------------------
GeoScript also requires a few Python dependencies.  

* Easy install simplejson::

     (geoscript)$ easy_install simplejson

* Easy install py-dom-xpath::

     (geoscript)$ easy_install py-dom-xpath-redux

Install nose
------------

Running GeoScript unit tests requires the `nose <http://somethingaboutorange.com/mrl/projects/nose/0.11.1/>`_ library.

* Easy install nose::

     (geoscript)$ easy_install nose

Install sphinx
--------------

Writing GeoScript documentation requires the `sphinx <http://sphinx.pocoo.org/>`_ library.

* Easy install sphinx::

     (geoscript)$ easy_install sphinx
