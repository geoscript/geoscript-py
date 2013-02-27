package org.geoscript.util;

import java.util.NoSuchElementException;

import org.geotools.data.simple.SimpleFeatureIterator;
import org.geotools.geometry.jts.ReferencedEnvelope;
import org.geotools.process.vector.SimpleProcessingCollection;
import org.opengis.feature.simple.SimpleFeature;
import org.opengis.feature.simple.SimpleFeatureType;
import org.python.core.PyException;
import org.python.core.PyGenerator;
import org.python.core.PyObject;

/**
 * Utility collection class for wrapping a python feature generator in a gt FeatureCollection.
 * 
 * @author Justin Deoliveira, OpenGeo
 */
public class PyFeatureCollection extends SimpleProcessingCollection {

    PyObject gen;
    SimpleFeature next;
    SimpleFeatureType schema;

    public PyFeatureCollection(PyObject gen) {
        this(gen, null);
    }

    public PyFeatureCollection(PyObject gen, SimpleFeatureType schema) {
        this.schema = schema;
        this.gen = gen;
        if (gen.__getattr__("next") == null) {
            throw new IllegalArgumentException("Object has no 'next' attribute");
        }
    }

    @Override
    public SimpleFeatureIterator features() {
        return new PyFeatureIterator();
    }

    @Override
    public ReferencedEnvelope getBounds() {
        return null;
    }
    
    @Override
    public int size() {
        return -1;
    }

    @Override
    protected SimpleFeatureType buildTargetFeatureType() {
        if (schema != null) {
            return schema;
        }

        SimpleFeature next = getNext();
        return next != null ? next.getFeatureType() : null;
    }

    SimpleFeature getNext() {
        if (next != null) {
            return  next;
        }

        return next = readNext();
    }

    SimpleFeature readNext() {
        try {
            PyObject n = gen.__getattr__("next").__call__();
            return (SimpleFeature) n.__getattr__("_feature").__tojava__(SimpleFeature.class);
            //return (SimpleFeature) gen.next().__getattr__("_feature").__tojava__(SimpleFeature.class);
        }
        catch(Exception e) {
            if (isStopIteration(e)) {
                return null;
            }
            else {
                if (e instanceof RuntimeException) {
                    throw (RuntimeException) e;
                }
                throw new RuntimeException(e);
            }
        }
    }

    boolean isStopIteration(Exception e) {
        //TODO: there has to be some better way to check for specific python exception type
        if (e instanceof PyException) {
            PyException pye = (PyException)e;

            if ("StopIteration".equals(e.toString().trim())) {
                return true;
            }


            if (pye.type.toString().contains("exceptions.StopIteration")) {
                return true;
            }
        }
        return false;
    }

    class PyFeatureIterator implements SimpleFeatureIterator {

        @Override
        public boolean hasNext() {
            return getNext() != null;
        }

        @Override
        public SimpleFeature next() throws NoSuchElementException {
            try {
                return getNext();
            }
            finally {
                next = null;
            }
        }

        @Override
        public void close() {
        }
    }

}
