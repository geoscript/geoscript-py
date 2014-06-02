geoscript-py README
===================

Build
---------------
Building geoscript-py is quite easy.  You will need to have git, Java, Jython, and  Maven installed.

Use git to clone the repository::

    git clone https://github.com/geoscript/geoscript-py.git

Use maven to build, test, and package::

    mvn clean install

Classpath Setup
---------------

GeoScript requires a number of GeoTools libraries to be present on the CLASSPATH
environment variable. Use the 'classpath' script to download the necessary 
libraries and set up the CLASSPATH environment::

  source classpath

Testing
-------

Some test cases require actual running services to test against (eg. Postgis). 
Edit 'tests/dbexts.ini' to configure database servers the tests will run 
against.
