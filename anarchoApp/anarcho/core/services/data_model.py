class DataModel(object):
    def __init__(self, **kwargs):
        for name, value in kwargs.iteritems():
            if hasattr(self, name):
                setattr(self, name, value)
        super(DataModel, self).__init__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return '{0}:{1}'.format(self.__class__, str(self.__dict__))

    @classmethod
    def from_row(cls, row):
        """
        Convert RowProxy to obj
        :param row:
        :type: row: RowProxy
        """
        if row:
            return cls.__call__(**dict(row.items()))
