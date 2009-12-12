if [ ! -e target ]; then
	mkdir target
fi
base=http://repo.opengeo.org
if [ ! -e target/commons-beanutils-1.7.0.jar ]; then
	echo "Downloading commons-beanutils-1.7.0.jar"
	curl -G $base/commons-beanutils/commons-beanutils/1.7.0/commons-beanutils-1.7.0.jar -o target/commons-beanutils-1.7.0.jar
fi
if [ ! -e target/commons-collections-3.1.jar ]; then
	echo "Downloading commons-collections-3.1.jar"
	curl -G $base/commons-collections/commons-collections/3.1/commons-collections-3.1.jar -o target/commons-collections-3.1.jar
fi
if [ ! -e target/commons-dbcp-1.2.2.jar ]; then
	echo "Downloading commons-dbcp-1.2.2.jar"
	curl -G $base/commons-dbcp/commons-dbcp/1.2.2/commons-dbcp-1.2.2.jar -o target/commons-dbcp-1.2.2.jar
fi
if [ ! -e target/commons-logging-1.0.3.jar ]; then
	echo "Downloading commons-logging-1.0.3.jar"
	curl -G $base/commons-logging/commons-logging/1.0.3/commons-logging-1.0.3.jar -o target/commons-logging-1.0.3.jar
fi
if [ ! -e target/commons-pool-1.5.3.jar ]; then
	echo "Downloading commons-pool-1.5.3.jar"
	curl -G $base/commons-pool/commons-pool/1.5.3/commons-pool-1.5.3.jar -o target/commons-pool-1.5.3.jar
fi
if [ ! -e target/geoapi-2.3-M1.jar ]; then
	echo "Downloading geoapi-2.3-M1.jar"
	curl -G $base/org/opengis/geoapi/2.3-M1/geoapi-2.3-M1.jar -o target/geoapi-2.3-M1.jar
fi
if [ ! -e target/geoapi-pending-2.3-M1.jar ]; then
	echo "Downloading geoapi-pending-2.3-M1.jar"
	curl -G $base/org/opengis/geoapi-pending/2.3-M1/geoapi-pending-2.3-M1.jar -o target/geoapi-pending-2.3-M1.jar
fi
if [ ! -e target/gt-api-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-api-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-api/2.7-SNAPSHOT/gt-api-2.7-SNAPSHOT.jar -o target/gt-api-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-coverage-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-coverage-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-coverage/2.7-SNAPSHOT/gt-coverage-2.7-SNAPSHOT.jar -o target/gt-coverage-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-cql-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-cql-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-cql/2.7-SNAPSHOT/gt-cql-2.7-SNAPSHOT.jar -o target/gt-cql-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-data-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-data-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-data/2.7-SNAPSHOT/gt-data-2.7-SNAPSHOT.jar -o target/gt-data-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-directory-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-directory-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-directory/2.7-SNAPSHOT/gt-directory-2.7-SNAPSHOT.jar -o target/gt-directory-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-epsg-hsql-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-epsg-hsql-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-epsg-hsql/2.7-SNAPSHOT/gt-epsg-hsql-2.7-SNAPSHOT.jar -o target/gt-epsg-hsql-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-jdbc-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-jdbc-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-jdbc/2.7-SNAPSHOT/gt-jdbc-2.7-SNAPSHOT.jar -o target/gt-jdbc-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-jdbc-h2-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-jdbc-h2-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/jdbc/gt-jdbc-h2/2.7-SNAPSHOT/gt-jdbc-h2-2.7-SNAPSHOT.jar -o target/gt-jdbc-h2-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-jdbc-mysql-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-jdbc-mysql-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-jdbc-mysql/2.7-SNAPSHOT/gt-jdbc-mysql-2.7-SNAPSHOT.jar -o target/gt-jdbc-mysql-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-jdbc-mysql-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-jdbc-mysql-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/jdbc/gt-jdbc-mysql/2.7-SNAPSHOT/gt-jdbc-mysql-2.7-SNAPSHOT.jar -o target/gt-jdbc-mysql-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-jdbc-postgis-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-jdbc-postgis-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/jdbc/gt-jdbc-postgis/2.7-SNAPSHOT/gt-jdbc-postgis-2.7-SNAPSHOT.jar -o target/gt-jdbc-postgis-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-jdbc-spatialite-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-jdbc-spatialite-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-jdbc-spatialite/2.7-SNAPSHOT/gt-jdbc-spatialite-2.7-SNAPSHOT.jar -o target/gt-jdbc-spatialite-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-jdbc-spatialite-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-jdbc-spatialite-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/jdbc/gt-jdbc-spatialite/2.7-SNAPSHOT/gt-jdbc-spatialite-2.7-SNAPSHOT.jar -o target/gt-jdbc-spatialite-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-main-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-main-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-main/2.7-SNAPSHOT/gt-main-2.7-SNAPSHOT.jar -o target/gt-main-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-metadata-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-metadata-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-metadata/2.7-SNAPSHOT/gt-metadata-2.7-SNAPSHOT.jar -o target/gt-metadata-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-referencing-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-referencing-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-referencing/2.7-SNAPSHOT/gt-referencing-2.7-SNAPSHOT.jar -o target/gt-referencing-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-render-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-render-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-render/2.7-SNAPSHOT/gt-render-2.7-SNAPSHOT.jar -o target/gt-render-2.7-SNAPSHOT.jar
fi
if [ ! -e target/gt-shapefile-2.7-SNAPSHOT.jar ]; then
	echo "Downloading gt-shapefile-2.7-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-shapefile/2.7-SNAPSHOT/gt-shapefile-2.7-SNAPSHOT.jar -o target/gt-shapefile-2.7-SNAPSHOT.jar
fi
if [ ! -e target/h2-1.1.104.jar ]; then
	echo "Downloading h2-1.1.104.jar"
	curl -G $base/org/h2database/h2/1.1.104/h2-1.1.104.jar -o target/h2-1.1.104.jar
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
	curl -G $base/net/java/dev/jsr-275/jsr-275/1.0-beta-2/jsr-275-1.0-beta-2.jar -o target/jsr-275-1.0-beta-2.jar
fi
if [ ! -e target/jts-1.10.jar ]; then
	echo "Downloading jts-1.10.jar"
	curl -G $base/com/vividsolutions/jts/1.10/jts-1.10.jar -o target/jts-1.10.jar
fi
if [ ! -e target/lib-1.0-SNAPSHOT.jar ]; then
	echo "Downloading lib-1.0-SNAPSHOT.jar"
	curl -G $base/geoscript/lib/1.0-SNAPSHOT/lib-1.0-SNAPSHOT.jar -o target/lib-1.0-SNAPSHOT.jar
fi
if [ ! -e target/maven-archiver ]; then
	echo "Downloading maven-archiver"
	curl -G $base/org/apache/maven/maven-archiver -o target/maven-archiver
fi
if [ ! -e target/mysql-connector-java-5.1.5.jar ]; then
	echo "Downloading mysql-connector-java-5.1.5.jar"
	curl -G $base/mysql/mysql-connector-java/5.1.5/mysql-connector-java-5.1.5.jar -o target/mysql-connector-java-5.1.5.jar
fi
if [ ! -e target/postgresql-8.4-701.jdbc3.jar ]; then
	echo "Downloading postgresql-8.4-701.jdbc3.jar"
	curl -G $base/postgresql/postgresql/8.4-701.jdbc3/postgresql-8.4-701.jdbc3.jar -o target/postgresql-8.4-701.jdbc3.jar
fi
if [ ! -e target/sqlite-jdbc-3.6.19.1-SNAPSHOT.jar ]; then
	echo "Downloading sqlite-jdbc-3.6.19.1-SNAPSHOT.jar"
	curl -G $base/org/xerial/sqlite-jdbc/3.6.19.1-SNAPSHOT/sqlite-jdbc-3.6.19.1-SNAPSHOT.jar -o target/sqlite-jdbc-3.6.19.1-SNAPSHOT.jar
fi
if [ ! -e target/vecmath-1.3.2.jar ]; then
	echo "Downloading vecmath-1.3.2.jar"
	curl -G $base/java3d/vecmath/1.3.2/vecmath-1.3.2.jar -o target/vecmath-1.3.2.jar
fi
