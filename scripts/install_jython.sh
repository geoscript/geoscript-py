curl https://repo1.maven.org/maven2/org/python/jython-installer/2.7.2/jython-installer-2.7.2.jar -o target/jython-installer.jar

java -jar target/jython-installer.jar -s -d target/jython

target/jython/bin/jython -m pip install nose simplejson py-dom-xpath-redux
