Bound Methods
=============

Some Pyrofork types define what are called bound methods. Bound methods are functions attached to a type which are
accessed via an instance of that type. They make it even easier to call specific methods by automatically inferring
some of the required arguments.

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")


    @app.on_message()
    def hello(client, message)
        message.reply("hi")


    app.run()

-----

.. currentmodule:: pyrogram.types

Message
-------

.. hlist::
    :columns: 3

    {message_hlist}

.. toctree::
    :hidden:

    {message_toctree}

Story
-----

.. hlist::
    :columns: 3

    {story_hlist}

.. toctree::
    :hidden:

    {story_toctree}

Chat
----

.. hlist::
    :columns: 4

    {chat_hlist}

.. toctree::
    :hidden:

    {chat_toctree}

User
----

.. hlist::
    :columns: 2

    {user_hlist}

.. toctree::
    :hidden:

    {user_toctree}

CallbackQuery
-------------

.. hlist::
    :columns: 3

    {callback_query_hlist}

.. toctree::
    :hidden:

    {callback_query_toctree}

InlineQuery
-----------

.. hlist::
    :columns: 2

    {inline_query_hlist}

.. toctree::
    :hidden:

    {inline_query_toctree}

PreCheckoutQuery
----------------

.. hlist::
    :columns: 2

    {pre_checkout_query_hlist}

.. toctree::
    :hidden:

    {pre_checkout_query_toctree}

ShippingQuery
-------------

.. hlist::
    :columns: 2

    {shipping_query_hlist}

.. toctree::
    :hidden:

    {shipping_query_toctree}

ChatJoinRequest
---------------

.. hlist::
    :columns: 2

    {chat_join_request_hlist}

.. toctree::
    :hidden:

    {chat_join_request_toctree}

