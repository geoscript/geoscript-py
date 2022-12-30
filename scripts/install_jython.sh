
# Install Jython

curl https://repo1.maven.org/maven2/org/python/jython-installer/2.7.3/jython-installer-2.7.3.jar -o target/jython-installer.jar

java -jar target/jython-installer.jar -s -d target/jython

# Pip for Jython is currently broken because of the lack of SNI support (https://github.com/jython/jython/issues/97)
#target/jython/bin/jython -m pip install nose simplejson py-dom-xpath-redux

# Install Nose

curl https://files.pythonhosted.org/packages/58/a5/0dc93c3ec33f4e281849523a5a913fa1eea9a3068acfa754d44d88107a44/nose-1.3.7.tar.gz -o target/nose-1.3.7.tar.gz

cd target

tar -xf nose-1.3.7.tar.gz

cd nose-1.3.7

../jython/bin/jython setup.py install

cd ..

# Install simplejson

curl -L https://github.com/simplejson/simplejson/archive/refs/tags/v3.17.5.tar.gz -o simplejson.tar.gz

tar -xf simplejson.tar.gz

cd simplejson-3.17.5

../jython/bin/jython setup.py install

cd ..

# Install future

curl -L https://files.pythonhosted.org/packages/45/0b/38b06fd9b92dc2b68d58b75f900e97884c45bedd2ff83203d933cf5851c9/future-0.18.2.tar.gz -o future-0.18.2.tar.gz

tar -xf future-0.18.2.tar.gz

cd future-0.18.2

../jython/bin/jython setup.py install

cd ..

# Install py-dom-xpath-redux

curl -L https://files.pythonhosted.org/packages/47/40/f7599dab3755179126e5f90db187b17e03090b242659ca8cfe8f6b3a54cf/py-dom-xpath-redux-0.1.1.tar.gz -o py-dom-xpath-redux-0.1.1.tar.gz

tar -xf py-dom-xpath-redux-0.1.1.tar.gz

cd py-dom-xpath-redux-0.1.1

../jython/bin/jython setup.py install