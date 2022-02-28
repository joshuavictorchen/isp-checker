[![](https://github.com/joshuavictorchen/isp-checker/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/joshuavictorchen/isp-checker/actions/workflows/main.yml)

# isp-checker

This is a new project. Performance may be neither accurate nor robust. [Documentation can be found here.](https://joshuavictorchen.github.io/isp-checker/)

## Installation

Prerequisites:

* Python 3.8+
* Git 2.33+

Navigate into a directory of your choice and grab the code from this repository:

    git clone https://github.com/joshuavictorchen/isp-checker.git

`cd` into `isp-checker` and install the application (note: the `.` is part of the command):

    cd isp-checker
    pip install -U -e .

## Use

Once installed, the `ispcheck` command can be executed from any working directory to check for ISP availability at a given address, or for a given Zillow or Trulia listing.

The program is currently in its early stages, and is not very robust. The command MUST be entered in one of the following forms, with no deviation. Two-liner addresses are not yet supported for manual address entry.

    ispcheck [street address], [city name], [state abbreviation], [5 digit zip code]
    - or -
    ispcheck [URL for Zillow listing]
    - or -
    ispcheck [URL for Trulia listing]

For example:

    ispcheck 123 neutronland road, reactorville, nc 12345

Sample output:

![sample output](docs/_images/example1.png)

Refer to the [documentation](https://joshuavictorchen.github.io/isp-checker/) for further instructions.