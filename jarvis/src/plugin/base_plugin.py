class BasePluging():
    name = "basepluging"
    description = " basePlugin description"

    def run(self, *args, **kargs):
        raise NotImplementedError("run function was not implemented")
    
    


