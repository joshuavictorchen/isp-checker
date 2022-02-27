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
^^^^^^^^

.. admonition:: TODO

   `This endpoint <https://www.spectrum.com/services/spectrum/buyflow/residential/proxy.api/root-v2/offers>`__ returns a list of offers
   and internet speeds when provided with a ``serviceLocationId`` query, and ``session-id`` and ``client-id`` headers.
      
   These correspond to the ``locationKey`` and ``transactionId`` attributes, respectively, in the parsed response dictionary from
   :py:obj:`parse_address_and_session_metadata<ispchecker.main.Spectrum.parse_address_and_session_metadata>`. This is not a typo;
   the Spectrum API is simply uninuitive.

   While this works in a browser setting, the requests return bad responses when queried programmatically. This is likely due to
   session/cookie issues, which have yet to be worked out.
   
.. autoclass:: ispchecker.main.Spectrum
   :members:
   :undoc-members:
   :show-inheritance:

CenturyLink
^^^^^^^^^^^

.. autoclass:: ispchecker.main.CenturyLink
   :members:
   :undoc-members:
   :show-inheritance:

Verizon
^^^^^^^

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