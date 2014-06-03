geoscript-py README
===================

Pre-requisites
--------------

Running geoscript-py requires:

* [Java 1.6+](https://www.java.com/en/download/)
* [Jython 2.5.1+](http://www.jython.org/downloads.html)


Developing
----------

Building geoscript-py requires [Maven 3](http://maven.apache.org/download.html). 

After cloning the repository:

    git clone https://github.com/geoscript/geoscript-py.git

Use maven to build:

    mvn clean install

More details can be found [here](http://geoscript.org/py/devel.html#devel).

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
