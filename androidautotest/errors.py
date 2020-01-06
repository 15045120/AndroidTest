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

class PathNotExistError(Error):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class CaseNotFoundError(Error):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class CaseHasExistError(Error):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class ADBNotFoundError(Error):
    def __init__(self):
        self.message = r'ADB is not install in your computer, visit https://developer.android.google.cn/studio/releases/platform-tools'
    def __str__(self):
        return repr(self.message)

class TesseractNotFoundError(Error):
    def __init__(self):
        self.message = r'Tesseract is not install in your computer, visit https://github.com/tesseract-ocr/tesseract'
    def __str__(self):
        return repr(self.message)

class JavaNotFoundError(Error):
    def __init__(self):
        self.message = r'Java is not install in your computer, visit https://www.oracle.com/technetwork/java/javase/downloads/index.html'
    def __str__(self):
        return repr(self.message)