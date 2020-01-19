from collections import OrderedDict

class Field:
    pass


class StringField(Field):
    
    def __init__(self, required=False, *args, **kwargs):
        pass

class FieldBoolean(Field):
    
    def __init__(self):
        pass


class PasswordField(StringField):
    pass

