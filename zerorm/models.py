from lifter.backends.python import IterableStore
from schematics.models import Model as SchematicsModel
from schematics.models import ModelMeta
from schematics.types import *  # noqa: F401,F403


class DBOperationError(Exception):
    pass


class DoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class DataManager:
    def __init__(self, klass):
        self.klass = klass
        self._table = klass._table

    def _make_id(self, eid):
        instance = self._table.get(eid=eid)
        instance.update({'id': eid})
        self._table.update(instance, eids=[eid, ])

    def get(self, **kwargs):
        record = self.filter(**kwargs)
        if not record:
            raise DoesNotExist

        elif len(record) > 1:
            raise MultipleObjectsReturned

        return list(record)[0]

    def all(self):
        all_instances = [self.klass(eid=i.eid, **i) for i in self._table.all()]
        store = IterableStore(all_instances)
        manager = store.query(self)
        return manager.all()

    def filter(self, *args, **kwargs):
        all_objects = self.all()
        store = IterableStore(all_objects)
        manager = store.query(self)
        return manager.filter(*args, **kwargs)

    def exclude(self, *args, **kwargs):
        all_objects = self.all()
        store = IterableStore(all_objects)
        manager = store.query(self)
        return manager.exclude(*args, **kwargs)

    def create(self, *args, **kwargs):
        eid = self._table.insert(kwargs)
        if not eid:
            raise DBOperationError('Failed to create record')

        return self.get(id=eid)

    def save(self, data, eid=None):
        if not eid:
            eid = self._table.insert(data)
            if not eid:
                raise DBOperationError('Failed to save record')
            self._make_id(eid)

        else:
            eid = self._table.update(data, eids=[eid, ])[0]
            if not eid:
                raise DBOperationError(
                    'Failed to update record {}'.format(eid))

        return eid

    def delete(self, eid):
        eid = self._table.remove(eids=[eid, ])
        if not eid:
            raise DBOperationError('Failed to remove record {}'.format(eid))

        return True


class ZeroMeta(type):
    def __getattr__(cls, key):
        if key == '_table':
            return cls.Meta.database.table(cls._schema.name.lower())

        elif key == 'objects':
            return DataManager(cls)

        return getattr(cls, key)


class FinalMeta(ModelMeta, ZeroMeta):
    pass


class Model(SchematicsModel, metaclass=FinalMeta):
    id = IntType()

    def __repr__(self):
        return '<{}: {}>'.format(
            self.__class__.__name__,
            str(self),
        )

    def __str__(self):
        return '{} object'.format(self.__class__.__name__)

    def __init__(self, eid=None, *args, **kwargs):
        super().__init__()

        self.id = eid
        self._table = self.Meta.database.table(self._schema.name.lower())
        self.manager = DataManager(self)

        for k, v in kwargs.items():
            if k in self._valid_input_keys:
                setattr(self, k, v)

    def __iter__(self):
        for k, v in self._data.items():
            yield k, v

    @property
    def pk(self):
        return self.id

    def save(self):
        self.id = self.manager.save(dict(self._data), self.id)
        return self.id

    def delete(self):
        if not self.id:
            raise DBOperationError('Could not delete unsaved object')
        return self.manager.delete(self.id)
