import bf
from google.appengine.ext import db
from google.appengine.api import datastore_errors
import logging
import copy

class BitFieldProperty(db.Property):
    def __init__(self, default=None, **kwargs):
        super(BitFieldProperty, self).__init__(default=default, **kwargs)
  
    def default_value(self):
        return BitField()

    def validate(self, value):
        if not isinstance(value, BitField):
            raise datastore_errors.BadValueError("Property %s must be a BitField instance" % self.name)
        value = super(BitFieldProperty, self).validate(value)
        return value

    
    def get_value_for_datastore(self, model_instance):
        value = self.__get__(model_instance, model_instance.__class__)
        return db.Blob(value.tostring())

    def make_value_from_datastore(self, value):
        b = BitField()
        if value is None: return b
        b.fromstring(value)
        return b
  
    data_type=db.Blob