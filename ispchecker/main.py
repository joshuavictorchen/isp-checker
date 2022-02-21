import requests
import sys
import warnings
from abc import ABC, abstractmethod
from cryptography.utils import CryptographyDeprecationWarning
from ispchecker import tools as t

# filter irrelevant deprecation warnings
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

DIVIDER = "\n ---------------------------------------"
LJUST = 19


def main():

    # create a string from the sys args list
    # the first element in list is the name of the calling function; it is ignored
    full_address = " ".join(sys.argv[1:])

    # instantiate an Address
    a = Address()

    # load in an address
    print(DIVIDER)
    a.parse_address(full_address)
    t.print_recursive_dict(a.address)

    # check for isps
    print(DIVIDER)
    print()
    a.check_isps()


class Address:
    """Placeholder text.

    Args:
        full_address (str): Placeholder text.

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
            "Verizon": Verizon(self.address),
            # "CenturyLink": CenturyLink()
        }

        self.isps = isps
        return isps


class ISP(ABC):
    def get_availability(self):
        return self.available

    def get_top_speed(self):
        return self.top_speed

    def get_metadata(self):
        return self.metadata


class Spectrum(ISP):
    def __init__(self, address_dict: dict):

        self.address = address_dict
        self.top_speed = None
        self.metadata = {}

        # checking spectrum availability is a 2-step process:
        #   1. get address metadata and session metadata
        #   2. use this metadata to get specific offerings
        print(" Spectrum ".ljust(LJUST, ".") + " ", end="")
        r = self.retrieve_address_and_session_metadata()
        self.available = self.parse_address_and_session_metadata(r)
        print(self.available)

    def retrieve_address_and_session_metadata(self):

        # spectrum endpoint for obtaining address and session metadata
        url = "https://location.spectrum.com/api-v2/svc/serviceability/v2"

        # the following headers must be provided for the request to succeed
        headers = {
            "User-Agent": "",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json",
            "Origin": "https://location.spectrum.com",
            "Connection": "keep-alive",
        }

        # json parameters for posting to the endpoint
        data = {
            "address": {
                "line1": self.address.get("street"),
                "postalCode": self.address.get("zip"),
            }
        }

        # post the request and obtain the response in dict form
        response = requests.post(url, json=data, headers=headers)

        return response

    def parse_address_and_session_metadata(self, response: requests.Response):

        # error checking here

        response = response.json()

        spectrum = [
            max(False, True if i.get("locationKey") else False)
            for i in response.get("addresses")
        ][0]

        return spectrum

    # incorporate later
    # note: sptoken doesn't work here, though it does via browser (more details TBD)

    # serviceLocationId = response.get('addresses')[0].get('locationKey')
    # sptoken = response.get('transactionId')

    # url = "https://www.spectrum.com/services/spectrum/buyflow/residential/proxy.api/root-v2/offers"

    # querystring = {"serviceLocationId":serviceLocationId}

    # headers = {
    #     "User-Agent": "",
    #     "Accept": "*/*",
    #     "Accept-Language": "en-US,en;q=0.5",
    #     "Accept-Encoding": "gzip, deflate, br",
    #     "session-id": sptoken,
    #     "client-id": sptoken,
    #     "Connection": "keep-alive",
    # }

    # response = requests.request("GET", url, headers=headers, params=querystring)


class CenturyLink(ISP):
    def check_centurylink(self):

        print(" CenturyLink ".ljust(LJUST, ".") + " ", end="")

        # get access token
        url = "https://shop.centurylink.com/uas/oauth"
        headers = {"Connection": "keep-alive"}
        response = requests.post(url, headers=headers).json()
        cltoken = "Bearer " + response.get("access_token")

        # get fullAddress, addressId, and provider
        url = "https://api.lumen.com/Application/v4/DCEP-Consumer/addressPredict"
        headers = {"Authorization": cltoken, "Connection": "keep-alive"}
        params = (("addr", self.address.get("full_address")),)
        response = requests.get(url, headers=headers, params=params).json()

        # just use the first match for now
        provider = response.get("provider")
        fullAddress = response.get("predictedAddressList")[0].get("fullAddress")
        addressId = response.get("predictedAddressList")[0].get("addressId")

        # match = False
        # for i in response.get('predictedAddressList'):
        #    print(", ".join(i.get('fullAddress').split(',')[:-1]))
        #    if (", ".join(i.get('fullAddress').split(',')[:-1])) == self.address.get('full_address'):
        #        match = True
        #        fullAddress = i.get('fullAddress')
        #        addressId = i.get('addressId')
        #        break
        # if not match:
        #    return False

        # get wireCenter
        headers = {
            "Authorization": cltoken,
            "Connection": "keep-alive",
        }
        data = {
            "addressId": addressId,
            "fullAddress": fullAddress,
            "provider": provider,
        }
        response = requests.post(
            "https://api.lumen.com/Application/v4/DCEP-Consumer/identifyAddress",
            headers=headers,
            json=data,
        ).json()

        wireCenter = response.get("addrValInfo").get("wireCenter")

        # get speed
        headers = {
            "Authorization": cltoken,
            "Connection": "keep-alive",
        }

        data = {
            "addressId": addressId,
            "fullAddress": fullAddress,
            "wireCenter": wireCenter,
        }

        response = requests.post(
            "https://api.centurylink.com/Application/v4/DCEP-Consumer/offer",
            headers=headers,
            json=data,
        ).json()

        mbps = response.get("offersList")[0].get("downloadSpeedMbps")

        print(mbps)


class Verizon(ISP):
    def __init__(self, address_dict: dict):

        self.address = address_dict
        self.top_speed = 50  # <-- parse from web later
        self.metadata = {}

        # verizon is a one-step process
        print(" Verizon ".ljust(LJUST, ".") + " ", end="")
        r = self.retrieve_plan_availability()
        self.available = self.parse_plan_availability(r)
        print(self.available)

    def retrieve_plan_availability(self):

        # home LTE availability is encompassed in this endpoint
        url = "https://www.verizon.com/vfw/v1/check5GAvailability"

        # the following headers must be provided for the request to succeed
        headers = {"User-Agent": ""}

        # json parameters for posting to the endpoint
        data = {
            "address1": self.address.get("street"),
            "city": self.address.get("city"),
            "state": self.address.get("state"),
            "zipcode": self.address.get("zip"),
        }

        # post the request and obtain the response in dict form
        response = requests.post(
            url,
            headers=headers,
            json=data,
        )

        return response

    def parse_plan_availability(self, response: requests.Response):

        # error checking here

        response = response.json()

        verizon_LTE = response.get("output").get("qualified4GHome")

        return verizon_LTE


if __name__ == "__main__":

    main()
