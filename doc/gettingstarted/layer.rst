.. _gettingstarted.layer:

Layers and Workspaces
=====================

A :class:`Layer <geoscript.layer.layer.Layer>` represents a particular set of spatial data. It contains methods that provide information about a data set such as the :meth:`count <geoscript.layer.layer.Layer.count>` of entries and the spatial :meth:`bounds <geoscript.layer.layer.Layer.bounds>` of the data::

  >>> from geoscript.layer import Shapefile
  >>> shp = Shapefile('states.shp')

  >>> shp.count()
  49
  >>> shp.bounds()
  (-124.731422, 24.955967, -66.969849, 49.371735, EPSG:4326)

.. note::

   In the above code sample the :class:`Shapefile <geoscript.layer.shapefile.Shapefile>` class is a layer subclass specific to the `Shapefile <http://en.wikipedia.org/wiki/Shapefile>`_ format.

Each entry in a Layer is known as a *feature* and represented by the :class:`Feature <geoscript.feature.Feature>` class. A feature is a set of attributes and an associated geometry. The :meth:`Layer.features() <geoscript.layer.layer.Layer.features>` method provides an iterator over the features of a layer:: 

  >>> for f in shp.features():
  >>>    print f 
  states.1 {the_geom: MULTIPOLYGON (((-88.071564 37.51099000000001, ... ,-88.071564 37.51099000000001))), STATE_NAME: Illinois, STATE_FIPS: 17, SUB_REGION: E N Cen, STATE_ABBR: IL, LAND_KM: 143986.61, WATER_KM: 1993.335, PERSONS: 11430602.0, FAMILIES: 2924880.0, HOUSHOLD: 4202240.0, MALE: 5552233.0, FEMALE: 5878369.0, WORKERS: 4199206.0, DRVALONE: 3741715.0, CARPOOL: 652603.0, PUBTRANS: 538071.0, EMPLOYED: 5417967.0, UNEMPLOY: 385040.0, SERVICE: 1360159.0, MANUAL: 828906.0, P_MALE: 0.486, P_FEMALE: 0.514, SAMP_POP: 1747776.0}
  ...

The :attr:`Layer.schema <geoscript.layer.layer.layer.schema>` property of a layer is a reference to the :class:`Schema <geoscript.feature.Schema>` of the features of the layer. The schema describes the structure of the features in the layer::

  >>> shp.schema
  states [the_geom: MultiPolygon, STATE_NAME: str, STATE_FIPS: str, SUB_REGION: str, STATE_ABBR: str, LAND_KM: float, WATER_KM: float, PERSONS: float, FAMILIES: float, HOUSHOLD: float, MALE: float, FEMALE: float, WORKERS: float, DRVALONE: float, CARPOOL: float, PUBTRANS: float, EMPLOYED: float, UNEMPLOY: float, SERVICE: float, MANUAL: float, P_MALE: float, P_FEMALE: float, SAMP_POP: float]

A schema is comprised of :class:`Field <geoscript.feature.Field>` objects that describe each attribute of a feature. A field describes the name and the type of a feature attribute. The :attr:`Schema.fields <geoscript.feature.Schema.fields>` method provides a list of all the fields in a schema, and the :meth:`Schema.get() <geoscript.feature.Schema.field>` method retrieves a field by name::

  >>> f = shp.schema.get('STATE_NAME')
  >>> f.name
  'STATE_NAME'
  >>> f.typ
  <type 'str'>

Every layer object is part of a :class:`Workspace <geoscript.workspace.workspace.Workspace>`. A workspace is a source of layers. The :meth:`Workspace.layers() <geoscript.workspace.workspace.Workspace.layers>` method provides a list of the layer names that the workspace provides::

  >>> ws = shp.workspace
  >>> ws
  Directory[/Users/bob]
  >>> ws.layers()
  ['counties', 'states']

.. note:: 

   The :class:`Shapefile <geoscript.layer.shapefile.Shapefile>` layer is implicitly part of a :class:`Directory <geoscript.workspace.directory.Directory>` workspace. The layers of a directory workspace correspond to the spatial files in the directory.

Workspaces provide the ability to create new layers as well as accessing existing ones. The :meth:`Workspace.create() <geoscript.workspace.workspace.Workspace.create>` method is used to create a new layer::

  >>> from geoscript import geom
  >>> l = ws.create('cities', [('geom', geom.Point), ('name', str)])
  >>> ws.layers()
  ['cities', 'counties', 'states']
  >>> l.count()
  0
  >>> l.add([geom.Point(37.78, -122.42), 'San Francisco'])
  >>> l.add([geom.Point(40.47, -73.58), 'New York'])
  >>> l.count()
  2
