Usage
=====

.. _installation:

Installation
------------

Install the packages using pip:

.. code-block:: console

   (.venv) $ pip install -r requirements.txt

Using scrapeutils
----------------

To retrieve the beautifulsoup object for a given url,
you can use the ``scrapeutils.GetSoup()`` function:

.. autofunction:: scrapeutils.GetSoup

The ``URL`` parameter should be the URL string.
The ``type`` should be the parser to be used.


For example:

>>> import lumache
>>> lumache.get_random_ingredients()
['shells', 'gorgonzola', 'parsley']

