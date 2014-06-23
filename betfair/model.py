# -*- coding: utf-8 -*-

import inflection

from .meta.model import Model


class BetfairModel(Model):
    """Handle conversions between internal (underscore) and external (camel-
    cased) key formatting; handle trailing underscores used to avoid conflicts
    with build-ins (e.g. from_).

    """
    def serialize_key(self, key):
        return inflection.camelize(
            key, uppercase_first_letter=False
        ).rstrip('_')

    def unserialize_key(self, key):
        key = inflection.underscore(key)
        if key in self._fields:
            return key
        return key + '_'
