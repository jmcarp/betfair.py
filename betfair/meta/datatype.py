# -*- coding: utf-8 -*-

class DataType(object):

    def __init__(self, type, preprocessor=None):
        self.type = type
        self.preprocessor = preprocessor

    def preprocess(self, value):
        return self.preprocessor(value) if self.preprocessor else value

    def serialize(self, value):
        return value

    def unserialize(self, value):
        processed = self.preprocess(value)
        if isinstance(processed, self.type):
            return processed
        if type(processed) == dict:
            return self.type(**processed)
        return self.type(processed)
