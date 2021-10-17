class RefValue:

    def __init__(self, default_value):
        self.default_value = default_value
        self.name = None
        self.internal_name = None

    def __set_name__(self, owner, name):
        self.name = name
        self.internal_name = "_" + name

    def __get__(self, instance, instance_type):
        if instance:
            val = getattr(instance, self.internal_name, self.default_value)
        else:
            val = getattr(instance_type, self.internal_name, self.default_value)

        if isinstance(val, RefValue):
            return val.__get__(instance, instance_type)

        return val

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class StaticRefValueSupport(type):

    def __setattr__(self, key, value):
        field = self.__dict__.get(key)
        if isinstance(field, RefValue):
            field.__set__(self, value)
        else:
            super().__setattr__(key, value)
