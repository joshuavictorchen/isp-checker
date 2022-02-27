import requests
from abc import ABC
from ispchecker import tools as t


class ISP(ABC):
    """Base class for ISPs. More documentation TBD.

    Args:
        address_dict (dict): Dictionary of address attributes in the following form:

            .. code-block::

                {
                    'full_address': str,
                    'street': str,
                    'city': str,
                    'state': str,
                    'zip': str # (5 digits)
                }
    """

    def __init__(self, address_dict: dict):

        t.print_divider()
        self.session = requests.Session()
        self.address = address_dict
        self.available = None
        self.top_speed = None
        self.summary = {}
        self.metadata = {}

    def get_address(self):
        return self.address

    def get_availability(self):
        return self.available

    def get_top_speed(self):
        return self.top_speed

    def get_summary(self):
        return self.summary

    def get_metadata(self):
        return self.metadata
