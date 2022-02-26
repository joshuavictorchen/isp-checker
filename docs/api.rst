API Documentation
-----------------

Address
=======

.. autoclass:: ispchecker.main.Address
   :members:
   :undoc-members:
   :show-inheritance:

ISP
===

.. autoclass:: ispchecker.main.ISP
   :members:
   :undoc-members:
   :show-inheritance:

Spectrum
========

.. admonition:: TODO

   The https://www.spectrum.com/services/spectrum/buyflow/residential/proxy.api/root-v2/offers endpoint returns a list of offers
   and internet speeds, given a ``serviceLocationId`` query, and ``session-id`` and ``client-id`` headers.
   
   These correspond to the ``locationKey`` and ``transactionId`` attributes, respectively, in the parsed response dictionary from
   :py:obj:`parse_address_and_session_metadata<ispchecker.main.Spectrum.parse_address_and_session_metadata>`
   (this is not a typo; the names are that uninuitive).

   While this works in a browser setting, the requests return bad responses when queried programmatically. Being able to query
   this endpoint will enable inspection of offered internet speeds, and better error checking.

   More details TBD.
   

.. autoclass:: ispchecker.main.Spectrum
   :members:
   :undoc-members:
   :show-inheritance:

CenturyLink
===========

.. autoclass:: ispchecker.main.CenturyLink
   :members:
   :undoc-members:
   :show-inheritance:

Verizon
=======

.. autoclass:: ispchecker.main.Verizon
   :members:
   :undoc-members:
   :show-inheritance:

Tools
=====

.. automodule:: ispchecker.tools
   :members:
   :undoc-members:
   :show-inheritance: