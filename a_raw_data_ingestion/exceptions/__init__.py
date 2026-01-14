
class APIError (Exception):
    def __init__ (self, code, attempt):
        self._status_code = code
        self._attempt_number = attempt
