package org.geoscript.util;

import java.awt.RenderingHints.Key;
import java.io.IOException;
import java.util.Collections;
import java.util.Set;

import org.geotools.data.DataAccess;
import org.geotools.data.FeatureListener;
import org.geotools.data.FeatureSource;
import org.geotools.data.Query;
import org.geotools.data.QueryCapabilities;
import org.geotools.data.ResourceInfo;
import org.geotools.data.simple.SimpleFeatureCollection;
import org.geotools.data.simple.SimpleFeatureIterator;
import org.geotools.data.simple.SimpleFeatureSource;
import org.geotools.data.store.FilteringFeatureCollection;
import org.geotools.data.store.FilteringFeatureIterator;
import org.geotools.feature.FeatureCollection;
import org.geotools.feature.FeatureIterator;
import org.geotools.geometry.jts.ReferencedEnvelope;
import org.opengis.feature.Feature;
import org.opengis.feature.simple.SimpleFeature;
import org.opengis.feature.simple.SimpleFeatureType;
import org.opengis.feature.type.FeatureType;
import org.opengis.feature.type.Name;
import org.opengis.filter.Filter;
import org.opengis.referencing.crs.CoordinateReferenceSystem;

/**
 * FeatureSource that delegates to a FeatureCollection.
 * 
 * @author Justin Deoliveira, OpenGeo
 */
public class CollectionDelegatingFeatureSource<T extends FeatureType, F extends Feature> 
    implements FeatureSource<T,F> {

    FeatureCollection<T,F> collection;

    public CollectionDelegatingFeatureSource(FeatureCollection<T,F> collection) {
        this.collection = collection;
    }

    public FeatureCollection<T, F> getCollection() {
        return collection;
    }

    @Override
    public Name getName() {
        return collection.getSchema().getName();
    }

    @Override
    public ResourceInfo getInfo() {
        return null;
    }

    @Override
    public DataAccess<T, F> getDataStore() {
        return null;
    }

    @Override
    public QueryCapabilities getQueryCapabilities() {
        return null;
    }

    @Override
    public void addFeatureListener(FeatureListener listener) {
    }

    @Override
    public void removeFeatureListener(FeatureListener listener) {
    }

    @Override
    public T getSchema() {
        return (T) collection.getSchema();
    }

    @Override
    public ReferencedEnvelope getBounds() throws IOException {
        return collection.getBounds();
    }

    @Override
    public ReferencedEnvelope getBounds(Query query) throws IOException {
        if (query.getFilter() == null || query.getFilter() == Filter.INCLUDE) {
            return getBounds();
        }
     
        ReferencedEnvelope env = new ReferencedEnvelope();
        env.setToNull();

        T schema = getSchema();
        if (schema.getGeometryDescriptor() == null) {
            //geometryless, nothing to do
            return env;
        }
        
        CoordinateReferenceSystem crs = getSchema().getCoordinateReferenceSystem();
        if (crs != null) {
            env = new ReferencedEnvelope(crs);
            env.setToNull();
        }

        
        //calculate manually based on filter
        SimpleFeatureIterator it = 
            new FilteringFeatureIterator((SimpleFeatureIterator) collection.features(), query.getFilter());

        //TODO: fix this casting
        
        try {
            if (it.hasNext()) {
                env.init(it.next().getBounds());
            }
            while(it.hasNext()) {
                env.include(it.next().getBounds());
            }
        }
        finally {
            it.close();
        }

        return env;
    }

    @Override
    public int getCount(Query query) throws IOException {
        if (query.getFilter() == null || query.getFilter() == Filter.INCLUDE) {
            return collection.size();
        }

        SimpleFeatureIterator it = 
            new FilteringFeatureIterator((SimpleFeatureIterator) collection.features(), query.getFilter());
        int count = 0;
        try {
            while(it.hasNext()) {
                it.next();
                count++;
            }
        }
        finally {
            it.close();
        }

        return count;
    }

    @Override
    public Set<Key> getSupportedHints() {
        return Collections.EMPTY_SET;
    }

    @Override
    public FeatureCollection<T, F> getFeatures() throws IOException {
        return collection;
    }

    @Override
    public FeatureCollection<T, F> getFeatures(Filter filter)
            throws IOException {
        if (filter == null || filter == Filter.INCLUDE) {
            return getFeatures();
        }

        return new FilteringFeatureCollection<T, F>(collection, filter);
    }
 
    @Override
    public FeatureCollection<T, F> getFeatures(Query query) throws IOException {
        //TODO: retype/sort/etc... based on the query 
        return getFeatures(query.getFilter());
    }
}