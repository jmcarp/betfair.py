# -*- coding: utf-8 -*-

from schematics import models

from . import utils


class BetfairModel(models.Model):

    def __init__(self, **data):
        super(BetfairModel, self).__init__()
        self.import_data(data)

    def import_data(self, data, **kwargs):
        data = utils.unserialize_dict(data)
        return super(BetfairModel, self).import_data(data, **kwargs)

    def serialize(self, *args, **kwargs):
        data = super(BetfairModel, self).serialize(*args, **kwargs)
        return utils.serialize_dict(data)
