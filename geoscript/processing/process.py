class Process():
    
    ''''A class implementing a process'''
    def __init__(self):
        pass
    
    def __str__(self):
        s=self.name + "\n"
        s+=self.description + "\n\nPARAMETERS:\n"
        for inp in self.inputs.values():
            lines = str(inp).split("\n");
            for line in lines:
                s += len("PARAMETERS:") * " " + line + "\n"        
        for out in self.outputs.values():
            s += len("PARAMETERS:") * " " + str(out) + "\n"        
        return s;
    
    def run(self, **args):            
        for inp in self.inputs.values():
            if inp.name in args.keys():
                if not inp.setValue(args[input.name]):
                    print "Error in parameter " + inp.name
                    return 
            else:
                if not inp.setValue(None):
                    print "Error in parameter " + inp.name
                    return 
        self._run()    
            
    