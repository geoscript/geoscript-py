class Parameter:
    '''
    Base class for all input parameters that a process might take. Subclasses of this class are
    used to define the semantics of an algorithm
    '''

    def __init__(self, name="", description=""):
        self.name = name
        self.description = description
        self.value = None

        self.isAdvanced = False

        #a hidden parameter can be used to set a hard-coded value.
        #It can be used as any other parameter, but it will not be shown to the user
        self.hidden = False


    def setValue(self, obj):
        '''sets the value of the parameter.
        Returns true if the value passed is correct for the type of parameter'''
        self.value = str(obj)
        return True

    def __str__(self):
        return self.name + " <" + self.__class__.__name__ +">"

    def serialize(self):
        return self.__class__.__name__ + "|" + self.name + "|" + self.description

    

class ParameterBoolean(Parameter):

    def __init__(self, name="", description="", default=True):
        Parameter.__init__(self, name, description)
        self.default = default

    def setValue(self, value):
        if value is None:
            self.value = self.default
            return True
        self.value = str(value) == str(True)
        return True

    def serialize(self):
        return self.__class__.__name__ + "|" + self.name + "|" + self.description + "|" + str(self.default)

    def deserialize(self, s):
        tokens = s.split("|")
        return ParameterBoolean (tokens[0], tokens[1], tokens[2] == str(True))

class ParameterCrs(Parameter):

    def __init__(self, name="", description="", default = "4326"):
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
        return self.__class__.__name__ + "|" + self.name + "|" + self.description +\
                        "|" + str(self.default)

    def deserialize(self, s):
        tokens = s.split("|")
        return ParameterCrs(tokens[0], tokens[1], tokens[2])

class ParameterExtent(Parameter):

    def __init__(self, name="", description="", default="0,1,0,1"):
        Parameter.__init__(self, name, description)
        self.default = default
        self.value = None #The value is a string in the form "xmin, xmax, ymin, ymax"

    def setValue(self, text):
        ##TODO: adapt it so it accepts other forms of input, like a list or a Bounds object
        if text is None:
            self.value = self.default
            return True
        tokens = text.split(",")
        if len(tokens)!= 4:
            return False
        try:
            float(tokens[0])
            float(tokens[1])
            float(tokens[2])
            float(tokens[3])
            self.value=text
            return True
        except:
            return False

    def serialize(self):
        return self.__class__.__name__ + "|" + self.name + "|" + self.description +\
                        "|" + str(self.default)

    def deserialize(self, s):
        tokens = s.split("|")
        return ParameterExtent(tokens[0], tokens[1], tokens[2])


class ParameterFixedTable(Parameter):

    def __init__(self, name="", description="", cols=["value"], numRows=3, fixedNumOfRows = False):
        Parameter.__init__(self, name, description)
        self.cols = cols
        self.numRows = numRows
        self.fixedNumOfRows = fixedNumOfRows
        self.value = None

    def setValue(self, obj):
        ##TODO: check that it contains a correct number of elements
        if isinstance(obj, str):
            self.value = obj
        else:
            self.value = ParameterFixedTable.tableToString(obj)
        return True

    @staticmethod
    def tableToString(table):
        tablestring = ""
        for i in range(len(table)):
            for j in range(len(table[0])):
                tablestring = tablestring + table[i][j] + ","
        tablestring = tablestring[:-1]
        return tablestring

    def deserialize(self, s):
        tokens = s.split("|")
        return ParameterFixedTable(tokens[0], tokens[1], tokens[3].split(";"), int(tokens[2]), tokens[4] == str(True))

    def serialize(self):
        return self.__class__.__name__ + "|" + self.name + "|" + self.description +\
                        "|" + str(self.numRows) + "|" + ";".join(self.cols) + "|" +  str(self.fixedNumOfRows)


class ParameterMultipleInput(Parameter):
    '''A parameter representing several data objects.
    Its value is a list of data sources.'''

    exported = None

    TYPE_VECTOR_ANY = -1
    TYPE_VECTOR_POINT = 0
    TYPE_VECTOR_LINE = 1
    TYPE_VECTOR_POLYGON = 2
    TYPE_RASTER = 3

    def __init__(self, name="", description="", datatype=-1, optional = False):
        Parameter.__init__(self, name, description)
        self.datatype = datatype
        self.optional = optional
        self.value = None        

    def setValue(self, obj):
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
            self.value = obj;
            return True
        else:            
            return False


    def serialize(self):
        return self.__class__.__name__ + "|" + self.name + "|" + self.description +\
                        "|" + str(self.datatype) + "|" + str(self.optional)

    def deserialize(self, s):
        tokens = s.split("|")
        return ParameterMultipleInput(tokens[0], tokens[1], float(tokens[2]), tokens[3] == str(True))

class ParameterNumber(Parameter):

    def __init__(self, name="", description="", minValue = None, maxValue = None, default = 0.0):
        Parameter.__init__(self, name, description)
        '''if the passed value is an int or looks like one, then we assume that float values
        are not allowed'''
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
            if (float(n) - int(float(n)) == 0):
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
        return self.__class__.__name__ + "|" + self.name + "|" + self.description +\
                        "|" + str(self.min) + "|" + str(self.max)  + "|" + str(self.default)

    def deserialize(self, s):
        tokens = s.split("|")
        for i in range (2,4):
            if tokens[i] == str(None):
                tokens[i] = None
            else:
                tokens[i] = float(tokens[i])
        '''we force the default to int if possible, since that indicates whether it is restricted
        to ints or not'''
        try:
            val = int(tokens[4])
        except:
            val = float(tokens[4])
        return ParameterNumber(tokens[0], tokens[1], tokens[2], tokens[3], val)

class ParameterRaster(Parameter):

    def __init__(self, name="", description="", optional=False):
        Parameter.__init__(self, name, description)
        self.optional = optional
        self.value = None
        self.exported = None


    def setValue(self, obj):
        #TODO: check that obj is a valid object    
        if obj == None:
            if self.optional:
                self.value = None
                return True
            else:
                return False
        self.value = obj
        return True
    
    def serialize(self):
        return self.__class__.__name__ + "|" + self.name + "|" + self.description +\
                        "|" + str(self.optional)

    def deserialize(self, s):
        tokens = s.split("|")
        return ParameterRaster(tokens[0], tokens[1], str(True) == tokens[2])

class ParameterSelection(Parameter):

    def __init__(self, name="", description="", options=[], default = 0):
        Parameter.__init__(self, name, description)
        self.options = options
        self.value = None ## values is the zero-based index of the selected option
        self.default = default

    def setValue(self, n):
        if n is None:
            self.value = self.default
            return True
        try:
            n = int(n)
            self.value = n
            return True
        except:
            return False

    def deserialize(self, s):
        tokens = s.split("|")
        if len(tokens) == 4:
            return ParameterSelection(tokens[0], tokens[1], tokens[2].split(";"), int(tokens[3]))
        else:
            return ParameterSelection(tokens[0], tokens[1], tokens[2].split(";"))

    def serialize(self):
        return self.__class__.__name__ + "|" + self.name + "|" + self.description +\
                        "|" + ";".join(self.options)
                                                
class ParameterString(Parameter):

    def __init__(self, name="", description="", default="", multiline = False):
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
        return self.__class__.__name__ + "|" + self.name + "|" + self.description +\
                        "|" + str(self.default)

    def deserialize(self, s):
        tokens = s.split("|")
        return ParameterString(tokens[0], tokens[1], tokens[2])


class ParameterTable(Parameter):

    def __init__(self, name="", description="", optional=False):
        Parameter.__init__(self, name, description)
        self.optional = optional
        self.value = None

    def setValue(self, obj):
        #TODO: check that obj is a valid object    
        if obj == None:
            if self.optional:
                self.value = None
                return True
            else:
                return False
        self.value = obj
        return True

    def serialize(self):
        return self.__class__.__name__ + "|" + self.name + "|" + self.description +\
                        "|" + str(self.optional)

    def deserialize(self, s):
        tokens = s.split("|")
        return ParameterTable(tokens[0], tokens[1], str(True) == tokens[2])

class ParameterTableField(Parameter):

    DATA_TYPE_NUMBER = 0
    DATA_TYPE_STRING = 1
    DATA_TYPE_ANY = -1

    def __init__(self, name="", description="", parent=None, datatype=-1):
        Parameter.__init__(self, name, description)
        self.parent = parent
        self.value = None
        self.datatype = datatype

    def setValue(self, obj):
        if obj is None:            
            return False
        self.value = str(obj)
        return True

    def serialize(self):
        return self.__class__.__name__ + "|" + self.name + "|" + self.description +\
                "|" + str(self.parent) + "|" + str(self.datatype)


    def deserialize(self, s):
        tokens = s.split("|")
        if len(tokens) == 4:
            return ParameterTableField(tokens[0], tokens[1], tokens[2], int(tokens[3]))
        else:
            return ParameterTableField(tokens[0], tokens[1], tokens[2])

    def __str__(self):
        return self.name + " <" + self.__class__.__name__ +" from " + self.parent     + ">"


class ParameterVector(Parameter):

    VECTOR_TYPE_POINT = 0
    VECTOR_TYPE_LINE = 1
    VECTOR_TYPE_POLYGON = 2
    VECTOR_TYPE_ANY = -1

    def __init__(self, name="", description="", shapetype=-1, optional=False):
        Parameter.__init__(self, name, description)
        self.optional = optional
        self.shapetype = shapetype
        self.value = None
        self.exported = None

    def setValue(self, obj):
        #TODO: check that obj is a valid object    
        if obj == None:
            if self.optional:
                self.value = None
                return True
            else:
                return False
        self.value = obj
        return True
    
    def serialize(self):
        return self.__module__.split(".")[-1] + "|" + self.name + "|" + self.description +\
                        "|" + str(self.shapetype) + "|" + str(self.optional)

    def deserialize(self, s):
        tokens = s.split("|")
        return ParameterVector(tokens[0], tokens[1], int(tokens[2]), str(True) == tokens[3])

def getparameterfromstring(s):
        classes = [ParameterBoolean, ParameterMultipleInput,ParameterNumber,
                   ParameterRaster, ParameterString, ParameterVector, ParameterTableField,
                   ParameterTable, ParameterSelection, ParameterFixedTable,
                   ParameterExtent, ParameterCrs]
        for clazz in classes:
            if s.startswith(clazz().__class__.__name__):
                return clazz().deserialize(s[len(clazz().__class__.__name__)+1:])