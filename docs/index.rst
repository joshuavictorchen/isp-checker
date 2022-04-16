Overview
--------

Internet Service Provider (ISP) serviceability data are not readily available for listings
on real estate websites such as Zillow and Trulia.

This means that homebuyers must manually navigate through the web interface for each potential ISP,
one at a time, in order to assess the internet connectivity options for a given listing.

The **isp-checker** program provides a framework for retrieving ISP serviceability data across providers
at any address - without having to trudge through each ISP website's clunky UI - 
by directly accessing specific API endpoints to retrieve this data.

The following ISPs and metadata are currently supported:

+---------------------------+---------------------+--------------+
| Internet Service Provider | Availability Status | Plan Details |
+===========================+=====================+==============+
| Spectrum                  | Yes                 | Coming soon* |
+---------------------------+---------------------+--------------+
| AT&T                      | Coming soon         | Coming soon  |
+---------------------------+---------------------+--------------+
| CenturyLink               | Yes                 | Yes          |
+---------------------------+---------------------+--------------+
| Verizon LTE Home Internet | Yes                 | N/A**        |
+---------------------------+---------------------+--------------+

*\* virtually all Spectrum connections have options for 200+ Mbps plans*

*\*\* all Verizon LTE Home Internet plans have stated download speeds of 25-50 Mbps*

Contents
--------

.. toctree::
   :maxdepth: 1

   manual
   architecture
   api