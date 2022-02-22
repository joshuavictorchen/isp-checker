Overview
--------

.. warning::

    This is a new project. Performance may be neither accurate nor robust. Results not guaranteed.

User Manual
===========

Detailed user instructions TBD.
For now, refer to the `readme on GitHub <https://github.com/joshuavictorchen/isp-checker/blob/master/README.md>`__.

API Documentation
-----------------

.. note::

   Documentation is under construction. This section describes the program at a very high level, for now.
   Note also that there are likely better ways to implement this, and the structure here is subject to change.

This program provides a framework for checking ISP serviceability at a given address.
The following ISPs are currently considered:

   * Spectrum
   * CenturyLink
   * Verizon (LTE Home Internet)

The framework is structured as follows:

   1. User executes the program and provides a formatted, case-insensitive address via the command line
   2. The provided address is parsed into dict of sub-components by
      :py:obj:`Address.parse_address<ispchecker.main.Address.parse_address>`
   3. :py:obj:`Address.check_isps<ispchecker.main.Address.check_isps>` instantiates a series of
      :py:obj:`ISP<ispchecker.main.ISP>`-based objects,
      which perform unique ISP-specific actions to retrieve metadata (serviceability, supported internet speed, etc.)
      based on their own execution stacks
   4. Results are printed to the console at runtime

More ISPs can be checked by simply creating new :py:obj:`ISP<ispchecker.main.ISP>`-based classes and adding them to the
:py:obj:`Address.check_isps<ispchecker.main.Address.check_isps>` function.

The following tools are used in the construction of this program:

+---------------+----------------+
| Item          | Tool           |
+===============+================+
| Unit tests    | Pytest         |
+---------------+----------------+
| Linting       | Black          |
+---------------+----------------+
| CI automation | Tox            |
+---------------+----------------+
| CI execution  | GitHub Actions |
+---------------+----------------+

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