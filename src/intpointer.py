#Wrapper for a value that a slider can change, because classes are passed as pointers
class IntPointer:
    def __init__(self, var):
        self.var = var
