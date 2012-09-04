#!/usr/bin/python
# -*- coding: utf-8 -*-
# TODO: implement more types of accepted value formats, as stated in the documentation

from geoscript.geom.bounds import Bounds
from geoscript.layer.raster import Raster
from geoscript.processing import utils
from geoscript.layer.geotiff import GeoTIFF
from geoscript.layer.layer import Layer
from geoscript.layer.shapefile import Shapefile


class Parameter:

    '''
    Base class for all input parameters that a process might take. Subclasses of this class are
    used to define the semantics of an algorithm
    '''

    def __init__(self, name='', description=''):
        self.name = name.lower()
        self.description = description
        self.value = None

        self.isAdvanced = False

        # a hidden parameter can be used to set a hard-coded value.
        # It can be used as any other parameter, but it should not be shown to the user

        self.hidden = False

    def setValue(self, obj):
        '''sets the value of the parameter.
        Returns true if the value passed is correct for the type of parameter'''

        self.value = str(obj)
        return True

    def isDefaultValueOK(self):
        return True

    def __str__(self):
        return self.name + ' <' + self.__class__.__name__ + '>'

    def description(self):
        return self.name + ' <' + self.__class__.__name__ + '>'

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description


class ParameterBoolean(Parameter):

    def __init__(
        self,
        name='',
        description='',
        default=True,
        ):
        Parameter.__init__(self, name, description)
        self.default = default

    def setValue(self, value):
        if value is None:
            self.value = self.default
            return True
        self.value = str(value) == str(True)
        return True

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + str(self.default)

    def deserialize(self, s):
        tokens = s.split('|')
        return ParameterBoolean(tokens[0], tokens[1], tokens[2]
                                == str(True))


class ParameterCrs(Parameter):

    def __init__(
        self,
        name='',
        description='',
        default='4326',
        ):
        '''The value is the EPSG code of the CRS'''

        Parameter.__init__(self, name, description)
        self.value = None
        self.default = default

    def setValue(self, value):
        if value is None:
            self.value = self.default
            return True
        self.value = str(value)
        return True

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + str(self.default)

    def deserialize(self, s):
        tokens = s.split('|')
        return ParameterCrs(tokens[0], tokens[1], tokens[2])


class ParameterExtent(Parameter):

    def __init__(
        self,
        name='',
        description='',
        default=Bounds(0, 0, 1, 1),
        ):
        Parameter.__init__(self, name, description)
        self.default = default
        self.value = None  # The value is a Bounds object

    def setValue(self, obj):
        if obj is None:
            self.value = self.default
            return True
        if isinstance(obj, Bounds):
            self.value = obj
        elif isinstance(obj, list):
            if len(obj != 4):
                return False
            try:
                self.value = Bounds(float(obj[0]), float(obj[2]),
                                    float(obj[1]), float(obj[3]))
                return True
            except:
                return False
        elif isinstance(obj, str):

            tokens = obj.split(',')
            if len(tokens) != 4:
                return False
            try:
                self.value = Bounds(float(tokens[0]), float(tokens[2]),
                                    float(tokens[1]), float(tokens[3]))
                return True
            except:
                return False
        else:
            return False

    def aslist(self):
        return [self.value.getwest(), self.value.getsouth(),
                self.value.geteast(), self.value.getnorth()]

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + str(self.default)

    def deserialize(self, s):
        tokens = s.split('|')
        return ParameterExtent(tokens[0], tokens[1], tokens[2])


class ParameterFile(Parameter):  # This is really like a ParameterString

    def __init__(
        self,
        name='',
        description='',
        default='',
        ):
        Parameter.__init__(self, name, description)
        self.default = default
        self.value = None

    def setValue(self, obj):
        if obj is None:
            self.value = self.default
            return True
        self.value = str(obj)
        return True

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + str(self.default)

    def deserialize(self, s):
        tokens = s.split('|')
        return ParameterString(tokens[0], tokens[1], tokens[2])


class ParameterFixedTable(Parameter):

    def __init__(
        self,
        name='',
        description='',
        cols=['value'],
        numRows=3,
        fixedNumOfRows=False,
        ):
        Parameter.__init__(self, name, description)
        self.cols = cols
        self.numRows = numRows
        self.fixedNumOfRows = fixedNumOfRows
        self.value = None

    def setValue(self, obj):

        # #TODO: check that it contains a correct number of elements

        if isinstance(obj, str):
            self.value = obj
        else:
            self.value = ParameterFixedTable.tableToString(obj)
        return True

    @staticmethod
    def tableToString(table):
        tablestring = ''
        for i in range(len(table)):
            for j in range(len(table[0])):
                tablestring = tablestring + table[i][j] + ','
        tablestring = tablestring[:-1]
        return tablestring

    def deserialize(self, s):
        tokens = s.split('|')
        return ParameterFixedTable(tokens[0], tokens[1],
                                   tokens[3].split(';'),
                                   int(tokens[2]), tokens[4]
                                   == str(True))

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + str(self.numRows) + '|' \
            + ';'.join(self.cols) + '|' + str(self.fixedNumOfRows)


class ParameterGeometry(Parameter):

    def __init__(
        self,
        name='',
        description='',
        optional=False,
        ):
        Parameter.__init__(self, name, description)
        self.value = None
        self.optional = optional

    def setValue(self, value):

        # TODO: check that obj is a valid object

        if value == None:
            if self.optional:
                self.value = None
                return True
            else:
                return False
        self.value = value
        return True

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + str(self.optional)

    def deserialize(self, s):
        tokens = s.split('|')
        return ParameterRaster(tokens[0], tokens[1], str(True)
                               == tokens[2])

    def isDefaultValueOK(self):
        return not self.optional

    def asgeom(self):

        # TODO: fill this

        pass


class ParameterMultipleInput(Parameter):

    '''A parameter representing several data objects.
    Its value is a list of data sources.'''

    exported = None

    TYPE_VECTOR_ANY = -1
    TYPE_VECTOR_POINT = 0
    TYPE_VECTOR_LINE = 1
    TYPE_VECTOR_POLYGON = 2
    TYPE_RASTER = 3

    def __init__(
        self,
        name='',
        description='',
        datatype=-1,
        optional=False,
        ):
        Parameter.__init__(self, name, description)
        self.datatype = datatype
        self.optional = optional
        self.value = None

    def setValue(self, obj):
        if not isinstance(obj, list):
            return False
        self.exported = None
        if obj == None:
            if self.optional:
                self.value = None
                return True
            else:
                return False

        if isinstance(obj, list):
            if len(obj) == 0:
                if self.optional:
                    return True
                else:
                    return False
            self.value = obj
            return True
        else:
            return False

    def isDefaultValueOK(self):
        return not self.optional

    def aslayers(self):
        pass

    def asfiles(self):
        if self.exported is not None:
            return self.exported
        self.exported = []
        for layer in self.value:
            if self.datatype == self.TYPE_RASTER:
                if isinstance(layer, str):
                    self.exported.append(layer)
                else:
                    if hasattr(layer.file) and layer.file is not None:
                        self.exported.append(layer.file)
                    else:
                        filename = utils.gettempfilename('tif')
                        GeoTIFF.save(self.value, filename)
                        self.exported.append(filename)
            else:
                if isinstance(layer, str):
                    self.exported.append(self.value)
                elif isinstance(layer, Layer):
                    if hasattr(layer, 'shapefile'):
                        self.exported.append(layer.shapefile)
                    else:
                        filename = utils.gettempfilename('shp')
                        Shapefile.save(layer, filename)
                        self.exported.append(filename)
        return self.exported

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + str(self.datatype) + '|' \
            + str(self.optional)

    def deserialize(self, s):
        tokens = s.split('|')
        return ParameterMultipleInput(tokens[0], tokens[1],
                float(tokens[2]), tokens[3] == str(True))


class ParameterNumber(Parameter):

    def __init__(
        self,
        name='',
        description='',
        minValue=None,
        maxValue=None,
        default=0.0,
        ):
        Parameter.__init__(self, name, description)
        try:
            self.default = int(str(default))
            self.isInteger = True
        except:
            self.default = default
            self.isInteger = False
        self.min = minValue
        self.max = maxValue
        self.value = None

    def setValue(self, n):
        if n is None:
            self.value = self.default
            return True
        try:
            if float(n) - int(float(n)) == 0:
                value = int(float(n))
            else:
                value = float(n)
            if self.min:
                if value < self.min:
                    return False
            if self.max:
                if value > self.max:
                    return False
            self.value = value
            return True
        except:
            return False

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + str(self.min) + '|' \
            + str(self.max) + '|' + str(self.default)

    def deserialize(self, s):
        tokens = s.split('|')
        for i in range(2, 4):
            if tokens[i] == str(None):
                tokens[i] = None
            else:
                tokens[i] = float(tokens[i])
        try:
            val = int(tokens[4])
        except:
            val = float(tokens[4])
        return ParameterNumber(tokens[0], tokens[1], tokens[2],
                               tokens[3], val)


class ParameterObject(Parameter):

    '''
    This is a wildcard class to be used for unusual parameter that do not fit
    into any of the other classes.
    '''

    def __init__(
        self,
        name='',
        description='',
        objecttype=None,
        ):
        Parameter.__init__(self, name, description)
        self.value = None
        self.objecttype = objecttype

    def setValue(self, obj):
        self.value = obj
        return True

    def deserialize(self, s):
        tokens = s.split('|')
        return ParameterString(tokens[0], tokens[1])

    def __str__(self):
        return self.name + ' <' + self.__class__.__name__ + ':' \
            + str(self.objecttype) + '>'


class ParameterRange(Parameter):

    def __init__(
        self,
        name='',
        description='',
        default='0,1',
        ):
        Parameter.__init__(self, name, description)
        self.value = None

    def setValue(self, obj):
        if obj is None:
            self.setValue(self.default)
            return True
        if isinstance(obj, str):
            try:
                tokens = obj.split(',')
                if len(tokens) != 2:
                    return False
                self.value = [float(tokens[0]), float(tokens[1])]
            except:
                return False
        if isinstance(obj, list):
            if len(obj) != 2:
                return False
            self.value = obj
            return True
        else:
            return False

    def asrange(self):
        return self.value.sort()

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + str(self.default)

    def deserialize(self, s):
        tokens = s.split('|')
        if len(tokens) == 3:
            return ParameterRange(tokens[0], tokens[1], tokens[2])
        else:
            return ParameterRange(tokens[0], tokens[1])


class ParameterRaster(Parameter):

    def __init__(
        self,
        name='',
        description='',
        optional=False,
        ):
        Parameter.__init__(self, name, description)
        self.optional = optional

        # the object value can be expressed as several type. Using the asXXX method is the recommended way
        # of getting it as a given data type

        self.value = None
        self.exported = None

    def setValue(self, obj):

        # TODO: check that obj is a valid object

        if obj == None:
            if self.optional:
                self.value = None
                return True
            else:
                return False
        self.value = obj
        return True

    def isDefaultValueOK(self):
        return not self.optional

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + str(self.optional)

    def deserialize(self, s):
        tokens = s.split('|')
        return ParameterRaster(tokens[0], tokens[1], str(True)
                               == tokens[2])

    def aslayer(self):
        if isinstance(self.value, Raster):
            return self.value
        elif isinstance(self.value, str):
            return Raster(file=self.value)

    def asfile(self):
        if isinstance(self.value, str):
            return self.value
        elif isinstance(self.value, Raster):
            if self.value.file is not None:
                return self.value.file
            else:
                if self.exported is not None:
                    return self.exported
                else:
                    self.exported = utils.gettempfilename('tif')
                    GeoTIFF.save(self.value, self.exported)
                    return self.exported

    def __str__(self):
        if self.optional:
            return self.name + ' (optional) <' \
                + self.__class__.__name__ + '>'
        else:
            return self.name + ' <' + self.__class__.__name__ + '>'


class ParameterSelection(Parameter):

    def __init__(
        self,
        name='',
        description='',
        options=[],
        default=0,
        ):
        Parameter.__init__(self, name, description)
        self.options = options
        self.value = None  # # value is the zero-based index of the selected option
        self.default = default

    def setValue(self, obj):
        if obj is None:
            self.value = self.default
            return True
        if isinstance(obj, str):
            if str in self.options:
                self.value = self.options.index(obj)
                return True
            else:
                return False
        elif isinstance(obj, int):
            self.value = obj
            return True
        else:
            return False

    def deserialize(self, s):
        tokens = s.split('|')
        if len(tokens) == 4:
            return ParameterSelection(tokens[0], tokens[1],
                    tokens[2].split(';'), int(tokens[3]))
        else:
            return ParameterSelection(tokens[0], tokens[1],
                    tokens[2].split(';'))

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + ';'.join(self.options)

    def __str__(self):
        s = self.name + ' <' + self.__class__.__name__ + '>\n'
        s += len(self.name) * ' ' + 'Options:\n'
        i = 0
        for opt in self.options:
            s += ' ' * (len(self.name) + len('Options:')) + str(i) \
                + ': ' + str(opt) + '\n'
            i += 1
        return s
    
    def asindex(self):
        return self.value

    def asvalue(self):
        return self.options[self.value]


class ParameterString(Parameter):

    def __init__(
        self,
        name='',
        description='',
        default='',
        ):
        Parameter.__init__(self, name, description)
        self.default = default
        self.value = None

    def setValue(self, obj):
        if obj is None:
            self.value = self.default
            return True
        self.value = str(obj)
        return True

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + str(self.default)

    def deserialize(self, s):
        tokens = s.split('|')
        return ParameterString(tokens[0], tokens[1], tokens[2])


class ParameterTable(Parameter):

    def __init__(
        self,
        name='',
        description='',
        optional=False,
        ):
        Parameter.__init__(self, name, description)
        self.optional = optional
        self.value = None
        self.exported = None

    def setValue(self, obj):

        # TODO: check that obj is a valid object

        if obj == None:
            if self.optional:
                self.value = None
                return True
            else:
                return False
        self.value = obj
        return True

    def isDefaultValueOK(self):
        return not self.optional

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + str(self.optional)

    def deserialize(self, s):
        tokens = s.split('|')
        return ParameterTable(tokens[0], tokens[1], str(True)
                              == tokens[2])

    def aslayer(self):
        if isinstance(self.value, Layer):
            return self.value
        elif isinstance(self.value, str):
            return Shapefile(self.value)

    def asfile(self):
        if isinstance(self.value, str):
            return self.value
        elif isinstance(self.value, Layer):
            if self.value.file is not None:
                return self.value.file
            else:
                if self.exported is not None:
                    return self.exported
                else:
                    self.exported = utils.gettempfilename('shp')
                    Shapefile.save(self.value, self.exported)
                    return self.exported


class ParameterTableField(Parameter):

    DATA_TYPE_NUMBER = 0
    DATA_TYPE_STRING = 1
    DATA_TYPE_ANY = -1

    def __init__(
        self,
        name='',
        description='',
        parent=None,
        datatype=-1,
        ):
        Parameter.__init__(self, name, description)
        self.parent = parent
        self.value = None
        self.datatype = datatype

    def isDefaultValueOK(self):
        return False

    def setValue(self, obj):
        if obj is None:
            return False
        self.value = str(obj)
        return True

    def serialize(self):
        return self.__class__.__name__ + '|' + self.name + '|' \
            + self.description + '|' + str(self.parent) + '|' \
            + str(self.datatype)

    def deserialize(self, s):
        tokens = s.split('|')
        if len(tokens) == 4:
            return ParameterTableField(tokens[0], tokens[1], tokens[2],
                    int(tokens[3]))
        else:
            return ParameterTableField(tokens[0], tokens[1], tokens[2])

    def __str__(self):
        return self.name + ' <' + self.__class__.__name__ + ' from ' \
            + self.parent + '>'


class ParameterVector(Parameter):

    VECTOR_TYPE_POINT = 0
    VECTOR_TYPE_LINE = 1
    VECTOR_TYPE_POLYGON = 2
    VECTOR_TYPE_ANY = -1

    def __init__(
        self,
        name='',
        description='',
        shapetype=-1,
        optional=False,
        ):
        Parameter.__init__(self, name, description)
        self.optional = optional
        self.shapetype = shapetype
        self.value = None
        self.exported = None

    def isDefaultValueOK(self):
        return not self.optional

    def setValue(self, obj):

        # TODO: check that obj is a valid object

        if obj == None:
            if self.optional:
                self.value = None
                return True
            else:
                return False
        self.value = obj
        return True

    def serialize(self):
        return self.__module__.split('.')[-1] + '|' + self.name + '|' \
            + self.description + '|' + str(self.shapetype) + '|' \
            + str(self.optional)

    def deserialize(self, s):
        tokens = s.split('|')
        return ParameterVector(tokens[0], tokens[1], int(tokens[2]),
                               str(True) == tokens[3])

    def aslayer(self):
        if isinstance(self.value, Layer):
            return self.value
        elif isinstance(self.value, str):

            # TODO: do not assume that the file is a shapefile

            return Shapefile(file=self.value)

    def asfile(self):
        if isinstance(self.value, str):
            return self.value
        elif isinstance(self.value, Layer):
            if hasattr(self.value, 'shapefile'):
                return self.value.shapefile
            else:
                if self.exported is not None:
                    return self.exported
                else:
                    self.exported = utils.gettempfilename('shp')
                    Shapefile.save(self.value, self.exported)
                    return self.exported

    def __str__(self):
        if self.optional:
            return self.name + ' (optional) <' \
                + self.__class__.__name__ + '>'
        else:
            return self.name + ' <' + self.__class__.__name__ + '>'


def getparameterfromstring(s):
    classes = [
        ParameterBoolean,
        ParameterMultipleInput,
        ParameterNumber,
        ParameterRaster,
        ParameterString,
        ParameterVector,
        ParameterTableField,
        ParameterTable,
        ParameterSelection,
        ParameterFixedTable,
        ParameterExtent,
        ParameterCrs,
        ParameterFile,
        ParameterGeometry,
        ParameterRange,
        ]
    for clazz in classes:
        if s.startswith(clazz().__class__.__name__):
            return clazz().deserialize(s[len(clazz().__class__.__name__)
                    + 1:])
