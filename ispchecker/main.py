import requests
import sys
import warnings
from cryptography.utils import CryptographyDeprecationWarning
from ispchecker import tools as t

# filter irrelevant deprecation warnings
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)


def main():

    # create a string from the sys args list
    # the first element in list is the name of the calling function; it is ignored
    full_address = " ".join(sys.argv[1:])

    # instantiate an Address
    a = Address(full_address)

    a.check_verizon_home_LTE()

    a.print_isps()


class Address:
    def __init__(self, full_address):

        self.address = self.parse_address(full_address)
        self.isps = {}

    def parse_address(self, full_address):

        # split the comma-delimited string and store trimmed elements in list
        address_components = [i.strip() for i in full_address.split(",")]

        # store each address component, along with the full original address, in a dict
        # the last two elements in the list are assumed to be state and zip (i.e. NC 12345)
        address_dict = {
            "full_address": full_address.strip(),
            "street": address_components[0],
            "city": address_components[1],
            "state": address_components[2].split()[0],
            "zip": address_components[2].split()[1],
        }

        return address_dict

    def print_isps(self):

        t.print_recursive_dict(self.isps)

    def check_verizon_home_LTE(self):

        # user-agent must be provided for the request to succeed
        # (no other header requirements for this endpoint)
        headers = {"User-Agent": ""}

        # data (json) parameters to post
        data = {
            "address1": self.address.get("street").upper(),
            "city": self.address.get("city").upper(),
            "state": self.address.get("state").upper(),
            "zipcode": self.address.get("zip"),
        }

        # post the request and obtain the response in dict form
        response = requests.post(
            "https://www.verizon.com/vfw/v1/check5GAvailability",
            headers=headers,
            json=data,
        ).json()

        # ASSUMING NO ERRORS FOR NOW
        verizon_LTE = response.get("output").get("qualified4GHome")

        self.isps.update({"verizon-LTE": verizon_LTE})

        return verizon_LTE


if __name__ == "__main__":

    main()
