# -*- coding: UTF-8 -*-
class Error(Exception):
    pass

class NoDeviceError(Error):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class PictureNotFoundError(Error):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class PictureNotExistError(Error):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)