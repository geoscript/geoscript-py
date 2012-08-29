class Process():
    
    ''''A class implementing a process'''
    
    def __str__(self):
        s=self.name + "\n"
        s+=self.description + "\n"
        s+=str(self.inputs) + "\n"
        s+=str(self.outputs) + "\n"
        return s;
    
    def run(self, **args):
        """
        Executes the process with set of named inputs. The input argument names are
        specified by the :attr:`inputs` property. The output arguments names are 
        specified by the :attr:`outputs` property.
        """
        pass 