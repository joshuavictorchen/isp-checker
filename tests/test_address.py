import unittest
from ispchecker.main import Address

STREET = "street"
CITY = "city"
STATE = "state"
ZIP = "12345"


class TestAddress(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # instantiate an Address with a properly-formatted address of the form:
        # street, city, state zip
        cls.address = Address()

    def test_instantiation(self):
        # check that the Address is instantiated
        self.assertTrue(type(self.address) == Address)

    def test_parse_address(self):
        # supply a good test address
        # check that the address components have been parsed into the 'address' dict attribute
        self.address.parse_address(f"{STREET}, {CITY}, {STATE} {ZIP}")
        self.assertTrue(
            self.address.address["full_address"]
            == f"{STREET.upper()}, {CITY.upper()}, {STATE.upper()} {ZIP.upper()}"
        )
        self.assertTrue(self.address.address["street"] == STREET.upper())
        self.assertTrue(self.address.address["city"] == CITY.upper())
        self.assertTrue(self.address.address["state"] == STATE.upper())
        self.assertTrue(self.address.address["zip"] == ZIP)


if __name__ == "__main__":

    unittest.main()
