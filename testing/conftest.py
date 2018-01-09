import os
import sys
import pytest
from zerorm import db, models


sys.path.append(os.getcwd())


@pytest.fixture(scope='session')
def db_instance(tmpdir_factory):
    return {'db': db(str(tmpdir_factory.getbasetemp().join('db.json')))}


@pytest.fixture()
def base_model(db_instance):
    class BaseModel(models.Model):
        class Meta:
            database = db_instance['db']

    return {'model': BaseModel}


@pytest.fixture()
def simple(base_model):
    class Person(base_model['model']):
        name = models.StringType(required=True)
        age = models.IntType()
        website = models.URLType()

        def __str__(self):
            return self.name

    data = [
        {'name': 'Alice', 'age': 23, 'website': 'http://alice.example.com'},
        {'name': 'Bob', 'age': 35, 'website': 'http://bob.example.com'},
        {'name': 'Chloe', 'age': 30, 'website': 'http://chloe.example.com'},
        {'name': 'Dylan', 'age': 30, 'website': 'http://dylan.example.com'},
        {'name': 'Eve', 'age': 20, 'website': 'http://eve.example.com'},
    ]

    return {'model': Person, 'data': data}
