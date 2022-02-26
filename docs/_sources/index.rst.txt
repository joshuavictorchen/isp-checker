Overview
--------

.. warning::

    This is a new project. Performance may be neither accurate nor robust.

This program provides a framework for checking ISP serviceability at a given address.

The following ISPs and metadata are currently supported:

+---------------------------+---------------------+--------------+
| Internet Service Provider | Availability Status | Plan Details |
+===========================+=====================+==============+
| Spectrum                  | Yes                 | No           |
+---------------------------+---------------------+--------------+
| CenturyLink               | Yes                 | Yes          |
+---------------------------+---------------------+--------------+
| Verizon LTE Home Internet | Yes                 | N/A*         |
+---------------------------+---------------------+--------------+

*\*all Verizon LTE Home Internet plans have download speeds of 25+ Mbps*

Contents
--------

.. toctree::
   :maxdepth: 1

   manual
   architecture
   api