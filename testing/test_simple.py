def test_save(simple_model):
    model = simple_model['model']
    for person in simple_model['data'][0:-1]:
        record = model(name=person['name'],
                       age=person['age'],
                       website=person['website'])
        record.save()


def test_create(simple_model):
    model = simple_model['model']
    person = simple_model['data'][-1]
    record = model.objects.create(**person)
    assert record


def test_get_by_id(simple_model):
    model = simple_model['model']
    record = model.objects.get(eid=1)
    assert record
    assert record.name == 'Alice'


def test_get_by_field(simple_model):
    # model = simple_model['model']
    # record = model.objects.get(name='Eve')
    # assert record
    pass


def test_all(simple_model):
    model = simple_model['model']
    assert len(model.objects.all()) == 5


def test_filter_eq(simple_model):
    model = simple_model['model']
    records = model.objects.filter(age=30)
    assert len(records) == 2


def test_filter_gt(simple_model):
    model = simple_model['model']
    records = model.objects.filter(age__gt=30)
    assert len(records) == 1
    assert records[0].name == 'Bob'


def test_filter_lte(simple_model):
    model = simple_model['model']
    records = model.objects.filter(age__lte=23)
    assert len(records) == 2
    assert records[0].name == 'Alice'


def test_delete(simple_model):
    model = simple_model['model']
    record = model.objects.get(eid=1)
    record.delete()
    assert len(model.objects.all()) == 4
