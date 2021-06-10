import sqlalchemy.types as types


class EncrypedString(types.UserDefinedType):
    def __init__(self, key, length=255):
        self.key = key
        self.length = length

    def get_col_spec(self, **kw):
        return f'VARCHAR({self.length})'

    def bind_processor(self, dialect):
        def process(value):
            return self.key.encode(value)
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            return self.key.decode(value)
        return process
