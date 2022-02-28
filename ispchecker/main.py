import sys
import warnings
from cryptography.utils import CryptographyDeprecationWarning
from ispchecker import tools as t
from ispchecker.spectrum import Spectrum
from ispchecker.centurylink import CenturyLink
from ispchecker.verizon import Verizon

# filter irrelevant deprecation warnings
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)


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

    # check for isps
    a.check_isps()
    t.print_divider()


class Address:
    """Placeholder text.

    **Relevant instance attributes:** \n
        * **address** (*dict*): Dictionary of addresses.
        * **isps** (*dict*): Dictionary of instantiated ISPs.
    """

    def __init__(self):

        self.address = {}
        self.isps = {}

    def parse_address(self, full_address):

        # split the comma-delimited string and store trimmed elements in list
        address_components = [i.strip() for i in full_address.split(",")]

        # store each address component, along with the full original address, in a dict
        # the last two elements in the list are assumed to be state and zip (i.e. NC 12345)
        address_dict = {
            "full_address": full_address.strip().upper(),
            "street": address_components[0].upper(),
            "city": address_components[1].upper(),
            "state": address_components[2].split()[0].upper(),
            "zip": address_components[2].split()[1],
        }

        self.address = address_dict
        return self.address

    def check_isps(self):

        if self.address == {}:
            print("\n Address is empty - please parse in an address first.")
            return None

        isps = {
            "Spectrum": Spectrum(self.address),
            "CenturyLink": CenturyLink(self.address),
            "Verizon LTE": Verizon(self.address),
        }

        self.isps = isps

        return isps


if __name__ == "__main__":

    main()
