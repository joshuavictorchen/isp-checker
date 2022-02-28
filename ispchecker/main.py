import sys
from ispchecker import tools as t
from ispchecker.address import Address
from ispchecker.spectrum import Spectrum
from ispchecker.centurylink import CenturyLink
from ispchecker.verizon import Verizon


def main():

    # create a string from the sys args list
    # the first element in list is the name of the calling function; it is ignored
    full_address = " ".join(sys.argv[1:])

    # instantiate an Address
    a = Address()

    # load in an address
    t.print_divider()
    a.parse_address(full_address)
    t.print_recursive_dict(a.address)

    # check for isp availability
    a.check_isps([Spectrum(), CenturyLink(), Verizon()])
    t.print_divider()


if __name__ == "__main__":

    main()
