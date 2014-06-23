# -*- coding: utf-8 -*-


class ModelError(Exception):
    pass


class MissingValueError(ModelError, ValueError):
    pass
