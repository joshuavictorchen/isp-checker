import requests
from abc import ABC, abstractmethod
from ispchecker import tools as t


class ISP(ABC):
    """Base class for ISPs. More documentation TBD."""

    def __init__(self):

        self.session = requests.Session()
        self.available = None
        self.summary = {}
        self.metadata = {}

    @abstractmethod
    def main_routine(self):
        pass

    def check_availability(self, address_dict: dict):
        """_summary_

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

        t.print_divider()
        t.print_isp_loader(type(self).__name__)

        self.address = address_dict

        self.main_routine()

        print(self.available)
        if self.summary != {}:
            t.print_recursive_dict(self.summary)
