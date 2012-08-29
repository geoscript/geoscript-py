class Process():
    
    ''''A class implementing a process'''
    
    def __str__(self):
        s=self.name + "\n"
        s+=self.description + "\n"
        s+=str(self.inputs) + "\n"
        s+=str(self.outputs) + "\n"
        return s;
    
    def run(self, **args):            
        for inp in self.inputs:
            if inp.name in args.keys():
                if not inp.setValue(args[input.name]):
                    print "Error in parameter " + inp.name
                    return 
            else:
                if not inp.setValue(None):
                    print "Error in parameter " + inp.name
                    return 
        self._run()    
            
    