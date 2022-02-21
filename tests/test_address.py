import unittest
from ispchecker.main import Address

STREET = "street"
CITY = "city"
STATE = "state"
ZIP = "zip"


class TestAddress(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # instantiate an Address with a properly-formatted address of the form:
        # street, city, state zip
        cls.address = Address(f"{STREET}, {CITY}, {STATE} {ZIP}")

    def test_instantiation(self):
        # check that the Address is instantiated
        self.assertTrue(type(self.address) == Address)

    def test_parse_address(self):
        # check that the address components have been parsed into the 'address' dict attribute
        self.assertTrue(
            self.address.address["full_address"] == f"{STREET}, {CITY}, {STATE} {ZIP}"
        )
        self.assertTrue(self.address.address["street"] == STREET)
        self.assertTrue(self.address.address["city"] == CITY)
        self.assertTrue(self.address.address["state"] == STATE)
        self.assertTrue(self.address.address["zip"] == ZIP)


if __name__ == "__main__":

    unittest.main()
