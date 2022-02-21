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
            # "Verizon": Verizon(self.address),
            # "CenturyLink": CenturyLink(self.address),
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
        self.available = "Undetermined"
        self.top_speed = "Undetermined"
        self.metadata = {}

        print(" Spectrum ".ljust(LJUST, ".") + " ", end="")

        # retrieve address/session response
        r = self.retrieve_address_and_session_metadata()

        # get dict from response and update self.metadata
        self.metadata.update(self.parse_address_and_session_metadata(r))

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
                # "line2": <-- unused for now
                "postalCode": self.address.get("zip"),
            }
        }

        # post the request and return the response
        return requests.post(url, json=data, headers=headers)

    def parse_address_and_session_metadata(self, response: requests.Response):
        """placeholder text

        .. code-block::

            {
                'transactionId': str,
                'rdofMatchLevel': str,
                'availableForCampaigns': list,
                'reasonCode': int,
                'serviceabilityFlags': {
                    'isPotentialExistingCustomer': bool,
                    'isProspectPendingConnect': bool,
                    'isPendingDisconnect': bool,
                    'hasNoLobsServiceable': bool,
                    'isTenant': bool,
                    'hasOpenWorkOrder': bool,
                    'isOutOfFootprint': bool,
                    'isMultiUnitGTMax': bool,
                    'isMultiUnitGTMinLTMaxPlusOne': bool,
                    'hasMultipleMsos': bool,
                    'isMsoNotFound': bool,
                    'isServiceabilityContinue': bool,
                    'isRepeatNonPay': bool,
                    'is2MNPH1NPD': bool,
                    'isNearbyMatch': bool,
                    'isZip4Match': bool,
                    'isMobileEligible': bool,
                    'isMultiLocation': bool,
                    'isAddressModified': bool,
                    'hasFiberToPremise': bool,
                    'isLocationServiceable': bool,
                    'isNonPayStatus': bool,
                    'isAddressConfirmed': bool,
                    'isSIAeligible': bool,
                    'isSMBCOMPOFF1Eligible': bool,
                    'isCandidateForBulkPilot': bool
                },
                'gisColor': str,
                'scrubbedAddress': {
                    'line1': str,
                    'line2': str,
                    'city': str,
                    'territoryCode': str,
                    'zipCode': str
                },
                'addresses': [{
                    'soloAddressId': int,
                    'line1': str,
                    'line2': str,
                    'city': str,
                    'territoryCode': str,
                    'zipCode': str,
                    'locationKey': str,
                    'locationType': str,
                    'serviceStatus': str,
                    'spcDivisionId': str,
                    'normalized': bool
                }],
                'msoCandidates': {
                    'ewsBusinessUnit': str,
                    'g2bBusinessUnit': str,
                    'gisBusinessUnit': str,
                    'defaultMSO': str
                }
            }

        Args:
            response (requests.Response): _description_

        Returns:
            _type_: _description_
        """

        # TODO: response status/error checking, robust conversion to dict, etc.
        #       (perhaps via ispchecker.tools)

        # for now, just convert to dict with no error checking
        response_dict = response.json()

        # check whether spectrum is available by looping through addresses list
        #   1. compare address line, city, territory (state), zip
        #   2. if match, then check if locationKey exists
        #      the ASSUMPTION is that it only exists if location is able to be serviced

        for i in response_dict.get("addresses"):

            # compare address elements
            # convert relevant elements UPPERCASE for comparison w/ self.address
            # ignore last token of line1 to avoid comparing things like 'ROAD' and 'RD'
            # only take first 5 digits of zip codes
            if (
                self.address.get("street").rsplit(" ", 1)[0]
                == i.get("line1").rsplit(" ", 1)[0].upper()
                and self.address.get("city") == i.get("city").upper()
                and self.address.get("state") == i.get("territoryCode").upper()
                and self.address.get("zip")[:5] == i.get("zipCode")[:5]
            ):

                # check if locationKey exists and set self.available accordingly
                if i.get("locationKey"):
                    self.available = True
                else:
                    self.available = False

                # availability has been determined, so response_dict can be returned now
                return response_dict

        # if no matches are found, do not update self.available and simply return response_dict
        return response_dict

    # incorporate later
    # note: transactionId is actually the sptoken
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
    def __init__(self, address_dict: dict):

        self.address = address_dict
        self.available = None
        self.top_speed = None
        self.metadata = {}

        print(" CenturyLink ".ljust(LJUST, ".") + " ", end="")
        self.execute_centurylink_stack()
        print(self.top_speed)

    def execute_centurylink_stack(self):

        access_token = self.retrieve_and_parse_access_token()
        address_metadata_response = self.retrieve_address_metadata(access_token)
        parsed_address_metadata = self.parse_address_metadata(address_metadata_response)
        wireCenter_response = self.retrieve_wireCenter(
            access_token,
            parsed_address_metadata.get("provider"),
            parsed_address_metadata.get("fullAddress"),
            parsed_address_metadata.get("addressId"),
        )
        wireCenter = self.parse_wireCenter(wireCenter_response)
        mbps_response = self.retrieve_mbps(
            access_token,
            parsed_address_metadata.get("fullAddress"),
            parsed_address_metadata.get("addressId"),
            wireCenter,
        )
        mbps = self.parse_mbps(mbps_response)

        self.top_speed = mbps

    def retrieve_and_parse_access_token(self):

        url = "https://shop.centurylink.com/uas/oauth"
        headers = {"Connection": "keep-alive"}
        response = requests.post(url, headers=headers)

        # check response here

        response = response.json()

        access_token = "Bearer " + response.get("access_token")

        return access_token

    def retrieve_address_metadata(self, access_token):

        url = "https://api.lumen.com/Application/v4/DCEP-Consumer/addressPredict"
        headers = {"Authorization": access_token, "Connection": "keep-alive"}
        params = (("addr", self.address.get("full_address")),)
        response = requests.get(url, headers=headers, params=params)

        return response

    def parse_address_metadata(self, response: requests.Response):

        # check response here

        response = response.json()

        # get fullAddress, addressId, and provider

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

        # just use the first match for now
        provider = response.get("provider")
        fullAddress = response.get("predictedAddressList")[0].get("fullAddress")
        addressId = response.get("predictedAddressList")[0].get("addressId")

        metadata = {
            "provider": provider,
            "fullAddress": fullAddress,
            "addressId": addressId,
        }

        return metadata

    def retrieve_wireCenter(self, access_token, provider, fullAddress, addressId):

        headers = {
            "Authorization": access_token,
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
        )

        return response

    def parse_wireCenter(self, response: requests.Response):

        # check response here

        response = response.json()

        wireCenter = response.get("addrValInfo").get("wireCenter")

        return wireCenter

    def retrieve_mbps(self, access_token, addressId, fullAddress, wireCenter):

        headers = {
            "Authorization": access_token,
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
        )

        return response

    def parse_mbps(self, response: requests.Response):

        # check response here

        response = response.json()

        mbps = response.get("offersList")[0].get("downloadSpeedMbps")

        return mbps


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
