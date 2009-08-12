if [ ! -e target ]; then
	mkdir target
fi
base=http://repo.opengeo.org
if [ ! -e target/commons-beanutils-1.7.0.jar ]; then
	echo "Downloading commons-beanutils-1.7.0.jar"
	curl -G $base/commons-beanutils/commons-beanutils/1.7.0/commons-beanutils-1.7.0.jar -o target/commons-beanutils-1.7.0.jar
fi
if [ ! -e target/commons-logging-1.0.3.jar ]; then
	echo "Downloading commons-logging-1.0.3.jar"
	curl -G $base/commons-logging/commons-logging/1.0.3/commons-logging-1.0.3.jar -o target/commons-logging-1.0.3.jar
fi
if [ ! -e target/commons-pool-1.3.jar ]; then
	echo "Downloading commons-pool-1.3.jar"
	curl -G $base/commons-pool/commons-pool/1.3/commons-pool-1.3.jar -o target/commons-pool-1.3.jar
fi
if [ ! -e target/geoapi-2.3-M1.jar ]; then
	echo "Downloading geoapi-2.3-M1.jar"
	curl -G $base/org/opengis/geoapi/2.3-M1/geoapi-2.3-M1.jar -o target/geoapi-2.3-M1.jar
fi
if [ ! -e target/geoapi-pending-2.3-M1.jar ]; then
	echo "Downloading geoapi-pending-2.3-M1.jar"
	curl -G $base/org/opengis/geoapi-pending/2.3-M1/geoapi-pending-2.3-M1.jar -o target/geoapi-pending-2.3-M1.jar
fi
if [ ! -e target/gt-api-2.6-SNAPSHOT.jar ]; then
	echo "Downloading gt-api-2.6-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-api/2.6-SNAPSHOT/gt-api-2.6-SNAPSHOT.jar -o target/gt-api-2.6-SNAPSHOT.jar
fi
if [ ! -e target/gt-epsg-hsql-2.6-SNAPSHOT.jar ]; then
	echo "Downloading gt-epsg-hsql-2.6-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-epsg-hsql/2.6-SNAPSHOT/gt-epsg-hsql-2.6-SNAPSHOT.jar -o target/gt-epsg-hsql-2.6-SNAPSHOT.jar
fi
if [ ! -e target/gt-main-2.6-SNAPSHOT.jar ]; then
	echo "Downloading gt-main-2.6-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-main/2.6-SNAPSHOT/gt-main-2.6-SNAPSHOT.jar -o target/gt-main-2.6-SNAPSHOT.jar
fi
if [ ! -e target/gt-metadata-2.6-SNAPSHOT.jar ]; then
	echo "Downloading gt-metadata-2.6-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-metadata/2.6-SNAPSHOT/gt-metadata-2.6-SNAPSHOT.jar -o target/gt-metadata-2.6-SNAPSHOT.jar
fi
if [ ! -e target/gt-referencing-2.6-SNAPSHOT.jar ]; then
	echo "Downloading gt-referencing-2.6-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-referencing/2.6-SNAPSHOT/gt-referencing-2.6-SNAPSHOT.jar -o target/gt-referencing-2.6-SNAPSHOT.jar
fi
if [ ! -e target/hsqldb-1.8.0.7.jar ]; then
	echo "Downloading hsqldb-1.8.0.7.jar"
	curl -G $base/hsqldb/hsqldb/1.8.0.7/hsqldb-1.8.0.7.jar -o target/hsqldb-1.8.0.7.jar
fi
if [ ! -e target/jdom-1.0.jar ]; then
	echo "Downloading jdom-1.0.jar"
	curl -G $base/jdom/jdom/1.0/jdom-1.0.jar -o target/jdom-1.0.jar
fi
if [ ! -e target/jsr-275-1.0-beta-2.jar ]; then
	echo "Downloading jsr-275-1.0-beta-2.jar"
	curl -G $base/net/java/dev/jsr-275/1.0-beta-2/jsr-275-1.0-beta-2.jar -o target/jsr-275-1.0-beta-2.jar
fi
if [ ! -e target/jts-1.10.jar ]; then
	echo "Downloading jts-1.10.jar"
	curl -G $base/com/vividsolutions/jts/1.10/jts-1.10.jar -o target/jts-1.10.jar
fi
if [ ! -e target/vecmath-1.3.1.jar ]; then
	echo "Downloading vecmath-1.3.1.jar"
	curl -G $base/java3d/vecmath/1.3.1/vecmath-1.3.1.jar -o target/vecmath-1.3.1.jar
fi
