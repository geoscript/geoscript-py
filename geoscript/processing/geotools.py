#!/usr/bin/python
# -*- coding: utf-8 -*-
from org.geotools.process import Processors
from geoscript import core
from geoscript.processing.process import Process
from geoscript.processing.provider import ProcessProvider
from geoscript.processing.parameters import ParameterRaster, \
    ParameterVector, ParameterBoolean, ParameterNumber, \
    ParameterString, ParameterObject, ParameterSelection, ParameterCrs, \
    ParameterExtent, ParameterGeometry
from geoscript.processing.outputs import OutputRaster, OutputVector, \
    OutputNumber, OutputObject
import java
from org.geotools.coverage.grid import GridCoverage2D
from org.geotools.feature import FeatureCollection
from org.geotools.referencing import CRS
from org.opengis.referencing.crs import CoordinateReferenceSystem
from com.vividsolutions.jts.geom import Envelope, Geometry


def getgeoscriptoutputs(outputs):

    m = {}
    for (k, v) in dict(outputs).iteritems():
        if v.type == GridCoverage2D:
            m[v.name] = OutputRaster(v.name, v.description)
        elif issubclass(v.type, FeatureCollection):
            m[v.name] = OutputVector(v.name, v.description)
        elif issubclass(v.type, java.lang.Number):
            m[v.name] = OutputNumber(v.name, v.description)
        else:

        # TODO: add other types

            m[v.name] = OutputObject(v.name, v.description)

    return m


def getgeoscriptinputs(inputs):
    m = {}
    for (k, v) in dict(inputs).iteritems():
        t = v.type
        desc = str(v.description)
        name = str(v.name)
        if t == GridCoverage2D:
            m[v.name] = ParameterRaster(name, desc)
        elif issubclass(t, FeatureCollection):
            m[v.name] = ParameterVector(name, desc)
        elif issubclass(t, Geometry):
            m[v.name] = ParameterGeometry(name, desc)            
        elif t == java.lang.Boolean or t == bool:
            m[v.name] = ParameterBoolean(name, desc)
        elif issubclass(v.type, java.lang.Number) or t == int or t == float:
            m[v.name] = ParameterNumber(name, desc)
        elif t == CRS or t == CoordinateReferenceSystem:
            m[v.name] = ParameterCrs(name, desc)
        elif issubclass(t, Envelope):
            m[v.name] = ParameterExtent(name, desc)
        elif t == java.lang.String:
            m[v.name] = ParameterString(name, desc)
        elif hasattr(t, 'values'):# is Enum                                 
            options = [str(s) for s in t.values()]                        
            m[v.name] = ParameterSelection(name, desc,
                    options)
            m[v.name].enum = t;
        else:
            m[v.name] = ParameterObject(name, v.description, v.type)

    return m


class GeotoolsProvider(ProcessProvider):

    """
    A provider for Geotools algorithms
    """

    def __init__(self):
        ProcessProvider.__init__(self)

    def loadprocesses(self):
        for pf in Processors.getProcessFactories():
            for n in pf.getNames():
                p = GeotoolsProcess(pf.create(n))
                p.name = str(':'.join((n.namespaceURI, n.localPart)))
                p.title = str(pf.getTitle(n))
                p.description = str(pf.getDescription(n))

                paraminfo = pf.getParameterInfo(n)
                p.inputs = getgeoscriptinputs(paraminfo)
                resultinfo = pf.getResultInfo(n, paraminfo)
                p.outputs = getgeoscriptoutputs(resultinfo)

                self._processes.append(p)

    def name(self):
        return 'GeoTools'


class GeotoolsProcess(Process):

    def __init__(self, process=None):
        Process.__init__(self)
        self._process = process

    def _run(self):

        # map the inputs to java.

        m = {}
        for inp in self.input:
            if isinstance(inp, ParameterRaster):
                m[inp.name] = core.unmap(inp.aslayer())
            elif isinstance(inp, ParameterVector):
                m[inp.name] = core.unmap(inp.aslayer().cursor())
            elif isinstance(inp, ParameterSelection):
                name = inp.asvalue()
                enumvalue = java.lang.Enum.valueOf(name, inp.enum)
                m[inp.name] = enumvalue
            else:
                m[inp.name] = core.unmap(inp.value)

        # run the process

        result = self._process.execute(m, None)

        # reverse map the outputs back

        r = {}
        for (k, v) in dict(result).iteritems():
            self.outputs[k].value = core.map(v)
            r[k] = self.outputs[k]

        return r
