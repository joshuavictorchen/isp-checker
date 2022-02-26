Architecture
------------

Framework
=========

.. note::

   Documentation is under construction. This section describes the program at a very high level, for now.
   This is just a prototype, and the structure here is subject to change.

This program is structured as follows:

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

Tooling
=======

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