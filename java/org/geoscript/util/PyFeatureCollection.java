package org.geoscript.util;

import java.util.NoSuchElementException;

import org.geotools.data.simple.SimpleFeatureIterator;
import org.geotools.geometry.jts.ReferencedEnvelope;
import org.geotools.process.vector.SimpleProcessingCollection;
import org.opengis.feature.simple.SimpleFeature;
import org.opengis.feature.simple.SimpleFeatureType;
import org.python.core.PyException;
import org.python.core.PyGenerator;

/**
 * Utility collection class for wrapping a python feature generator in a gt FeatureCollection.
 * 
 * @author Justin Deoliveira, OpenGeo
 */
public class PyFeatureCollection extends SimpleProcessingCollection {

    PyGenerator gen;
    SimpleFeature next;

    public PyFeatureCollection(PyGenerator gen) {
        this.gen = gen;
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
            return (SimpleFeature) gen.next().__getattr__("_feature").__tojava__(SimpleFeature.class);
        }
        catch(Exception e) {
            //TODO: there has to be some better way to check for specific python exception type
            if (e instanceof PyException && "StopIteration".equals(e.toString().trim())) {
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
