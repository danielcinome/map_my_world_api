
class ExistingValueError(Exception):
    def __init__(self, message):
        self.message = message
    
class CreationError(Exception):
    def __init__(self, message):
        self.message = message