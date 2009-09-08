geoscript-py README
===================

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
