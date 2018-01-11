def test_save(simple):
    model = simple['model']
    for person in simple['data'][0:-1]:
        record = model(name=person['name'],
                       age=person['age'],
                       website=person['website'])
        record.save()


def test_create(simple):
    model = simple['model']
    person = simple['data'][-1]
    record = model.objects.create(**person)
    assert record


def test_get_by_id(simple):
    model = simple['model']
    record = model.objects.get(eid=1)
    assert record
    assert record.name == 'Alice'


def test_get_by_field(simple):
    # model = simple['model']
    # record = model.objects.get(name='Eve')
    # assert record
    pass


def test_all(simple):
    model = simple['model']
    assert len(model.objects.all()) == 5


def test_filter_eq(simple):
    model = simple['model']
    records = model.objects.filter(age=30)
    assert len(records) == 2


def test_filter_gt(simple):
    model = simple['model']
    records = model.objects.filter(age__gt=30)
    assert len(records) == 1
    assert list(records)[0].name == 'Bob'


def test_filter_lte(simple):
    model = simple['model']
    records = model.objects.filter(age__lte=23)
    assert len(records) == 2
    assert list(records)[0].name == 'Alice'


def test_filter_returns_qs(simple):
    model = simple['model']
    records = model.objects.filter(age__gt=20)
    records = records.filter(age__lt=30)
    assert len(records) == 1
    assert list(records)[0].name == 'Alice'


def test_exclude(simple):
    model = simple['model']
    records = model.objects.exclude(age=30)
    assert len(records) == 3


def test_exclude_returns_qs(simple):
    model = simple['model']
    records = model.objects.exclude(age=35).filter(age__gt=20)
    assert len(records) == 3


def test_delete(simple):
    model = simple['model']
    record = model.objects.get(eid=1)
    record.delete()
    assert len(model.objects.all()) == 4
