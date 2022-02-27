Architecture
------------

Framework
=========

.. note::

   Documentation is under construction. This section describes the program at a very high level, for now.
   This is just a prototype, and the structure here is subject to change.

This program is structured as follows:

   #. User executes the program and provides a formatted, case-insensitive address via the command line.
   #. The provided address is parsed into dict of sub-components by
      :py:obj:`Address.parse_address<ispchecker.main.Address.parse_address>`.
   #. :py:obj:`Address.check_isps<ispchecker.main.Address.check_isps>` instantiates a series of
      :py:obj:`ISP<ispchecker.main.ISP>`-based objects,
      which perform unique ISP-specific actions to retrieve metadata (serviceability, supported internet speed, etc.)
      based on their own execution stacks.
   #. Results are printed to the console at runtime.

More ISPs can be checked by simply creating new :py:obj:`ISP<ispchecker.main.ISP>`-based classes and adding them to the
:py:obj:`Address.check_isps<ispchecker.main.Address.check_isps>` function.

Methodology
===========

The key to directly retrieving ISP serviceability data via API requests lies in figuring out
*what* API endpoints exist in the first place, and identifying which of those endpoints
are required to obtain a list of service plans and internet speeds for a given address.

High-level instructions
^^^^^^^^^^^^^^^^^^^^^^^

   #. Navigate to the ISP's website using a broswer of choice.
   #. Open the browser's network inspector.
   #. Using a sample address, navigate through the website's UI to determine
      if the address is serviced by the provider - and the available service plans and internet speeds, if so.
   #. Inspect the XHR objects that were passed between the server and the client during the previous step.
      Using the request and response attributes of those XHR objects, create an API request structure
      that can be used to retrieve serviceability data for *any* address for this ISP. Usually, more than one
      request is needed to get from a street address to an offerings list.
   #. Repeat the above steps with a comprehensive suite of addresses to determine
      the request/response syntax under different scenarios: addresses with different levels
      of service, addresses not serviced by the ISP, addresses not recognized by the website, etc.
   #. Use the above findings to implement a new :py:obj:`ISP<ispchecker.main.ISP>`-based class into the
      `framework`_.

Example walk-through
^^^^^^^^^^^^^^^^^^^^

*Coming soon.*

Tooling
=======

The following tools are used in the construction and maintenance of this program:

+---------------+----------------+
| Item          | Tool           |
+===============+================+
| Unit testing  | Pytest         |
+---------------+----------------+
| Linting       | Black          |
+---------------+----------------+
| Documentation | Sphinx* + RTD  |
+---------------+----------------+
| CI automation | Tox            |
+---------------+----------------+
| CI execution  | GitHub Actions |
+---------------+----------------+

*\*the default make.bat file that is created with sphinx-quickstart has been customized for this program*