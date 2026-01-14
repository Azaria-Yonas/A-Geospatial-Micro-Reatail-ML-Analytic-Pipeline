from . import APIError


class ArcGISError (APIError):
    def __init__(self, resonse):
        super().__init__()
        self.response = resonse


class False200 (ArcGISError):
    
        



def validate_argis():
    pass
    
