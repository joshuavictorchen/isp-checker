User Manual
-----------

*Detailed user instructions TBD.*

Installation
============

Prerequisites:
    * Python 3.8+
    * Git 2.33+

Navigate into a directory of choice and grab the code from this repository::

    git clone https://github.com/joshuavictorchen/isp-checker.git isp-checker

``cd`` into ``isp-checker`` and install the application. Use of a venv is recommended::

    cd isp-checker
    pip install -U -e .

Basic Use
=========

Once installed, the ``ispcheck`` command can be executed from any working directory to check for ISP availability at a given address, or for a given Zillow or Trulia listing.

The program is in its early stages, and is not very robust. The command MUST be entered in one of the following forms, with no deviation. Two-liner addresses are not yet supported for manual address entry::

    ispcheck [street address], [city name], [state abbreviation], [5 digit zip code]
    - or -
    ispcheck [URL for Zillow listing]
    - or -
    ispcheck [URL for Trulia listing]

For example::

    ispcheck 123 neutronland road, reactorville, nc 12345

Example
^^^^^^^

.. figure:: _images/example1.png

Continuous Input
^^^^^^^^^^^^^^^^

    The program can also check a series of addresses or listing URLs without having to explicitly execute the ``ispcheck`` command each time.

    To activate the continuous input mode, simply call the ``ispcheck`` command with no further arguments, after which addresses or listing URLs may be entered and checked sequentially.
    This mode is useful to have open when actively browsing real estate listings.

    Enter ``quit`` or ``q`` to exit the program.