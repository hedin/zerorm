You should probably use `alkali <https://github.com/kneufeld/alkali>`_ if you want to use JSON as DB.

Zerorm
======

Zerorm is trying to combine `TinyDB <https://github.com/msiemens/tinydb>`_,
`Schematics <https://github.com/schematics/schematics>`_
and `Lifter <https://github.com/EliotBerriot/lifter>`_ together to look like an ORM.

Installation
------------

.. code-block:: shell

     pip install zerorm

Usage
-----

First declare a model with TinyDB's instance attached to it:

.. code-block:: python

    from zerorm import db, models

    database = db('db.json')


    class Message(models.Model):
        author = models.StringType(required=True)
        author_email = models.EmailType()
        text = models.StringType()
        replies = models.IntType(min_value=0)

        class Meta:
            database = database

Now create some objects:

.. code-block:: pycon

    >>> from models import Message
    >>>
    >>> bob_message = Message(author='Bob',
    ...                       author_email='bob@example.com',
    ...                       text='Hello, everyone!')
    >>> bob_message
    <Message: Message object>
    >>> bob_message.save()  # Save object
    1
    >>>
    >>> bob_message.replies = 1
    >>> bob_message.save()  # Update object
    >>>
    >>> alice_message = Message.objects.create(author='Alice',
    ...                                        text='Hi, Bob!',
    ...                                        replies=0)
    >>> alice_message
    <Message: Message object>

And try to retrieve them via *objects*

.. code-block:: pycon

    >>> Message.objects.all()
    <QuerySet, len() = 2>
    >>> list(Message.objects.all())
    [<Message: Message object>, <Message: Message object>]
    >>>
    >>> second_message = Message.objects.get(id=2)
    >>> second_message.author
    'Alice'
    >>>
    >>> Message.objects.filter(replies__gte=1)  # Only Bob's message has 1 replies
    <QuerySet, len() = 1>
    >>> list(Message.objects.filter(replies__gte=1))
    [<Message: Message object>]

You can redefine model's *__str__* method for better repr.

.. code-block:: python

    class Message(models.Model):
        ...

        def __str__(self):
            return 'by {}'.format(self.author)

.. code-block:: pycon

    >>> list(Message.objects.all())
    [<Message: by Bob>, <Message: by Alice>]

License
-------

MIT. See LICENSE for details.
