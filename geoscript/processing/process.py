from geoscript.processing.utils import gettempfilename
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
    
    def help(self):
        print str(self)
        
    def run(self, **args):            
        for inp in self.inputs.values():
            if inp.name in args.keys():
                if not inp.setValue(args[inp.name]):
                    print "Error in parameter " + inp.name
                    return 
            else:
                if not inp.isDefaultValueOK():
                    print "Missing mandatory " + inp.name
                    return 
                else:
                    inp.setDefaultValue()                
        for out in self.outputs.values():
            if out.name in args.keys():
                out.setValue(args[out.name])
        
        self.resolvetemporaryoutputs()
        self._run()   
        return self.outputs 
            
    def resolvetemporaryoutputs(self):
        '''sets temporary outputs (output.value = None) with a temporary file instead'''
        for out in self.outputs.values():
            if out.value == None:
                out.settempoutput()
    