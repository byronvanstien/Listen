.. currentmodule:: listen

Full Listen API reference
=========================

.. note::
   Logging should be implemented on your end

.. note::
   A feature that will get previous song names may be added at some point


Find out your version
=====================

.. data:: __version__
   A string that represents the version of Listen you're using.


Client
======

.. autoclass:: listen.client.Client
   :members:


DataClasses
===========

.. note::
   These are not for creating yourself, they are handed to you from the library backend

.. autoclass:: Song
   :members:

.. autoclass:: User
   :members:

Exceptions
==========
.. note::
   :func:`listen.Client.start` throws `RuntimeError`_ if the absence of a handler is spotted.

.. autoexception:: KanaError
.. autoexception:: ListenError

.. _coroutine: https://docs.python.org/3/library/asyncio-task.html#coroutine
.. _RuntimeError: https://docs.python.org/3/library/exceptions.html#RuntimeError
.. |coro| replace:: This function is a `coroutine`_
