if [ ! -e target ]; then
	mkdir target
fi
base=http://repo.opengeo.org
if [ ! -e target/batik-anim-1.7.jar ]; then
	echo "Downloading batik-anim-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-anim/1.7/batik-anim-1.7.jar -o target/batik-anim-1.7.jar
fi
if [ ! -e target/batik-awt-util-1.7.jar ]; then
	echo "Downloading batik-awt-util-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-awt-util/1.7/batik-awt-util-1.7.jar -o target/batik-awt-util-1.7.jar
fi
if [ ! -e target/batik-bridge-1.7.jar ]; then
	echo "Downloading batik-bridge-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-bridge/1.7/batik-bridge-1.7.jar -o target/batik-bridge-1.7.jar
fi
if [ ! -e target/batik-css-1.7.jar ]; then
	echo "Downloading batik-css-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-css/1.7/batik-css-1.7.jar -o target/batik-css-1.7.jar
fi
if [ ! -e target/batik-dom-1.7.jar ]; then
	echo "Downloading batik-dom-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-dom/1.7/batik-dom-1.7.jar -o target/batik-dom-1.7.jar
fi
if [ ! -e target/batik-ext-1.7.jar ]; then
	echo "Downloading batik-ext-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-ext/1.7/batik-ext-1.7.jar -o target/batik-ext-1.7.jar
fi
if [ ! -e target/batik-gvt-1.7.jar ]; then
	echo "Downloading batik-gvt-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-gvt/1.7/batik-gvt-1.7.jar -o target/batik-gvt-1.7.jar
fi
if [ ! -e target/batik-parser-1.7.jar ]; then
	echo "Downloading batik-parser-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-parser/1.7/batik-parser-1.7.jar -o target/batik-parser-1.7.jar
fi
if [ ! -e target/batik-script-1.7.jar ]; then
	echo "Downloading batik-script-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-script/1.7/batik-script-1.7.jar -o target/batik-script-1.7.jar
fi
if [ ! -e target/batik-svg-dom-1.7.jar ]; then
	echo "Downloading batik-svg-dom-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-svg-dom/1.7/batik-svg-dom-1.7.jar -o target/batik-svg-dom-1.7.jar
fi
if [ ! -e target/batik-svggen-1.7.jar ]; then
	echo "Downloading batik-svggen-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-svggen/1.7/batik-svggen-1.7.jar -o target/batik-svggen-1.7.jar
fi
if [ ! -e target/batik-transcoder-1.7.jar ]; then
	echo "Downloading batik-transcoder-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-transcoder/1.7/batik-transcoder-1.7.jar -o target/batik-transcoder-1.7.jar
fi
if [ ! -e target/batik-util-1.7.jar ]; then
	echo "Downloading batik-util-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-util/1.7/batik-util-1.7.jar -o target/batik-util-1.7.jar
fi
if [ ! -e target/batik-xml-1.7.jar ]; then
	echo "Downloading batik-xml-1.7.jar"
	curl -G $base/org/apache/xmlgraphics/batik-xml/1.7/batik-xml-1.7.jar -o target/batik-xml-1.7.jar
fi
if [ ! -e target/commons-beanutils-1.7.0.jar ]; then
	echo "Downloading commons-beanutils-1.7.0.jar"
	curl -G $base/commons-beanutils/commons-beanutils/1.7.0/commons-beanutils-1.7.0.jar -o target/commons-beanutils-1.7.0.jar
fi
if [ ! -e target/commons-io-1.1.jar ]; then
	echo "Downloading commons-io-1.1.jar"
	curl -G $base/commons-io/commons-io/1.1/commons-io-1.1.jar -o target/commons-io-1.1.jar
fi
if [ ! -e target/commons-logging-1.0.3.jar ]; then
	echo "Downloading commons-logging-1.0.3.jar"
	curl -G $base/commons-logging/commons-logging/1.0.3/commons-logging-1.0.3.jar -o target/commons-logging-1.0.3.jar
fi
if [ ! -e target/commons-pool-1.3.jar ]; then
	echo "Downloading commons-pool-1.3.jar"
	curl -G $base/commons-pool/commons-pool/1.3/commons-pool-1.3.jar -o target/commons-pool-1.3.jar
fi
if [ ! -e target/fop-0.94.jar ]; then
	echo "Downloading fop-0.94.jar"
	curl -G $base/org/apache/xmlgraphics/fop/0.94/fop-0.94.jar -o target/fop-0.94.jar
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
if [ ! -e target/gt-coverage-2.6-SNAPSHOT.jar ]; then
	echo "Downloading gt-coverage-2.6-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-coverage/2.6-SNAPSHOT/gt-coverage-2.6-SNAPSHOT.jar -o target/gt-coverage-2.6-SNAPSHOT.jar
fi
if [ ! -e target/gt-cql-2.6-SNAPSHOT.jar ]; then
	echo "Downloading gt-cql-2.6-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-cql/2.6-SNAPSHOT/gt-cql-2.6-SNAPSHOT.jar -o target/gt-cql-2.6-SNAPSHOT.jar
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
if [ ! -e target/gt-render-2.6-SNAPSHOT.jar ]; then
	echo "Downloading gt-render-2.6-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-render/2.6-SNAPSHOT/gt-render-2.6-SNAPSHOT.jar -o target/gt-render-2.6-SNAPSHOT.jar
fi
if [ ! -e target/gt-shapefile-2.6-SNAPSHOT.jar ]; then
	echo "Downloading gt-shapefile-2.6-SNAPSHOT.jar"
	curl -G $base/org/geotools/gt-shapefile/2.6-SNAPSHOT/gt-shapefile-2.6-SNAPSHOT.jar -o target/gt-shapefile-2.6-SNAPSHOT.jar
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
if [ ! -e target/vecmath-1.3.2.jar ]; then
	echo "Downloading vecmath-1.3.2.jar"
	curl -G $base/java3d/vecmath/1.3.2/vecmath-1.3.2.jar -o target/vecmath-1.3.2.jar
fi
if [ ! -e target/xalan-2.6.0.jar ]; then
	echo "Downloading xalan-2.6.0.jar"
	curl -G $base/xalan/xalan/2.6.0/xalan-2.6.0.jar -o target/xalan-2.6.0.jar
fi
if [ ! -e target/xml-apis-1.3.04.jar ]; then
	echo "Downloading xml-apis-1.3.04.jar"
	curl -G $base/xml-apis/xml-apis/1.3.04/xml-apis-1.3.04.jar -o target/xml-apis-1.3.04.jar
fi
if [ ! -e target/xml-apis-ext-1.3.04.jar ]; then
	echo "Downloading xml-apis-ext-1.3.04.jar"
	curl -G $base/xml-apis/xml-apis-ext/1.3.04/xml-apis-ext-1.3.04.jar -o target/xml-apis-ext-1.3.04.jar
fi
if [ ! -e target/xmlgraphics-commons-1.2.jar ]; then
	echo "Downloading xmlgraphics-commons-1.2.jar"
	curl -G $base/org/apache/xmlgraphics/xmlgraphics-commons/1.2/xmlgraphics-commons-1.2.jar -o target/xmlgraphics-commons-1.2.jar
fi
