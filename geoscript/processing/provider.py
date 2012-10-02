class ProcessProvider():
    '''This is the base class for process providers.
    
    A process provider is a set of related processes, typically from the same
    external application or related to a common area of analysis.
    '''    

    def __init__(self):        
        self._processes = None
        

    def checkprocesses(self):
        if self._processes is None:
            self._processes = []
            self.loadprocesses()
            self._processesmap = {}
            for p in self._processes:
                self._processesmap[p.name.lower()] = p  
    
    
    def processes(self):
        self.checkprocesses()   
        return self._processes    
        
    def lookup(self, name):
        '''Returns a process based on its name.
        
        The *name* parameter is a colon delimited string in the form namespace:name.
        The parameter is not case-sensitive
        
        Returns None if the provider does not contain a process with that name'''
        self.checkprocesses()  
        name =  name.lower()
        for p in self._processes:
            if p.name.lower() == name:
                return p        
        return None
        
    #methods to be overridden.
    #==============================
    
    def name(self):
        '''Returns a short descriptive name of the provider, usually (but not necessarily) representing the namespace'''
        pass
    
    def loadprocesses(self):
        '''Processes should be created/loaded here.
        
        The *self._processes* list object should be filled with *Process* objects
        '''
        pass
    
