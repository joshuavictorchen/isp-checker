import requests
import warnings
from abc import ABC, abstractmethod
from cryptography.utils import CryptographyDeprecationWarning
from ispchecker import tools as t

# filter irrelevant deprecation warnings, which pop up when using the requests module
# https://github.com/pyca/cryptography/issues/6456#issue-1033689568
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)


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
