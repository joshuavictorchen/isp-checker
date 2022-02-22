import requests
import sys
import warnings
from abc import ABC
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
            "CenturyLink": CenturyLink(self.address),
            "Verizon": Verizon(self.address),
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

        print(" Spectrum ".ljust(LJUST, ".") + " ", end="", flush=True)

        # retrieve address/session response
        r = self.retrieve_address_and_session_metadata()

        # get dict from response, parse availability, and update self.metadata
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

        Args:
            response (requests.Response): _description_

        Returns:
            _type_: _description_

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
                'addresses': [
                    {
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
                    }
                ],
                'msoCandidates': {
                    'ewsBusinessUnit': str,
                    'g2bBusinessUnit': str,
                    'gisBusinessUnit': str,
                    'defaultMSO': str
                }
            }
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

                # availability has been determined, so response_dict can be returned now
                return response_dict

        # if this line is reached, then no matching addresses were found
        self.available = False

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
        self.available = "Undetermined"
        self.top_speed = "Undetermined"
        self.metadata = {}

        print(" CenturyLink ".ljust(LJUST, ".") + " ", end="", flush=True)
        self.execute_centurylink_stack()

        if not self.available or self.available == "Undetermined":
            print(self.available)
        else:
            print(f"{self.available} ({self.top_speed} Mbps)")

    def execute_centurylink_stack(self):

        # get security token
        access_token = self.retrieve_and_parse_access_token()

        # get initial address response
        address_metadata_response = self.retrieve_address_metadata(access_token)

        # check for returned address matches
        parsed_address_metadata = self.parse_address_metadata(address_metadata_response)

        # exit routine if no matches found
        if not parsed_address_metadata:
            self.available = False
            return

        # get request wireCenter attribute using the parsed_address_metadata
        wireCenter_response = self.retrieve_wireCenter(
            access_token,
            parsed_address_metadata.get("provider"),
            parsed_address_metadata.get("fullAddress"),
            parsed_address_metadata.get("addressId"),
        )

        # parse wireCenter attribute from response
        wireCenter = self.parse_wireCenter(wireCenter_response)

        # exit routine if no match found
        # NOTE: NOT checking for null wireCenter
        if wireCenter == "No match":
            self.available = False
            self.top_speed = 0
            return

        offering_response = self.retrieve_offerings(
            access_token,
            parsed_address_metadata.get("addressId"),
            parsed_address_metadata.get("fullAddress"),
            wireCenter,
        )

        self.metadata.update(self.parse_offerings(offering_response))

    def retrieve_and_parse_access_token(self):
        """_summary_

        Returns:
            _type_: _description_

        .. code-block::

            {
                'expires_in': str,
                'access_token': str,
                'issued_at': str
            }
        """

        url = "https://shop.centurylink.com/uas/oauth"
        headers = {"Connection": "keep-alive"}
        response = requests.post(url, headers=headers)

        # TODO: response status/error checking, robust conversion to dict, etc.
        #       (perhaps via ispchecker.tools)

        # for now, just convert to dict with no error checking
        response_dict = response.json()

        # subsequent API requests use access_token prepended by "Bearer "
        access_token = "Bearer " + response_dict.get("access_token")

        return access_token

    def retrieve_address_metadata(self, access_token):
        """_summary_

        Args:
            access_token (_type_): _description_

        Returns:
            _type_: _description_

        .. code-block::

            {
                'status': int,
                'message': str,
                'provider': str,
                'predictedAddressList': [
                    {
                        'fullAddress': str,
                        'addressId': str,
                        'mdu': bool
                    }
                ]
            }
        """

        url = "https://api.lumen.com/Application/v4/DCEP-Consumer/addressPredict"
        headers = {"Authorization": access_token, "Connection": "keep-alive"}
        params = (("addr", self.address.get("full_address")),)
        response = requests.get(url, headers=headers, params=params)

        return response

    def parse_address_metadata(self, response: requests.Response):
        """_summary_

        Args:
            response (requests.Response): _description_

        Returns:
            _type_: _description_
        """

        # TODO: response status/error checking, robust conversion to dict, etc.
        #       (perhaps via ispchecker.tools)

        # for now, just convert to dict with no error checking
        response_dict = response.json()

        # if no predicted addresses found, then return None
        if len(response_dict.get("predictedAddressList")) == 0:
            return None

        # check if queried address is in predicted address list
        match = False
        for i in response_dict.get("predictedAddressList"):

            # fullAddress is returned in the form: 123 NAME RD,CITY,STATE 12345,USA
            # reformat and remove the 'RD' and 'USA' for comparison to self.address element

            # get list of address components, minus the last token
            fullAddress = i.get("fullAddress").split(",")[:-1]

            # remove last sub-token of first token (i.e., the 'RD')
            fullAddress[0] = fullAddress[0].rsplit(" ", 1)[0]

            # join the components back together
            fullAddress = ", ".join(fullAddress)

            # perform comparison
            if fullAddress == (
                self.address.get("street").rsplit(" ", 1)[0]
                + ", "
                + self.address.get("city")
                + ", "
                + self.address.get("state")
                + " "
                + self.address.get("zip")
            ):

                match = True
                fullAddress = i.get("fullAddress")
                addressId = i.get("addressId")
                break

        # if no matches found, then return None
        if not match:
            return None

        # get provider
        provider = response_dict.get("provider")

        # store parsed values in dict
        metadata = {
            "provider": provider,
            "fullAddress": fullAddress,
            "addressId": addressId,
        }

        return metadata

    def retrieve_wireCenter(self, access_token, provider, fullAddress, addressId):
        """_summary_

        Args:
            access_token (_type_): _description_
            provider (_type_): _description_
            fullAddress (_type_): _description_
            addressId (_type_): _description_

        Returns:
            _type_: _description_

        .. code-block::

            {
                'status': int,
                'message': str,
                'addrValInfo': {
                    'result': str,
                    'billingSource': str,
                    'fullAddress': str,
                    'addressId': str,
                    'mduInfo': TBD,
                    'wireCenter': str,
                    'nearMatchAddress': TBD,
                    'nearMatchList': TBD,
                    'exactMatchAddress': TBD
                },
                'loopQualInfo': {
                    'message': str,
                    'messageDetail': TBD
                },
                'leadIndicator': str,
                'leadIndicatorStatus': TBD,
                'addressId': str,
                'unitNumber': TBD,
                'geoSecUnitId': TBD,
                'googleInfo': TBD,
                'biwfInfo': {
                    'fiberQualified': bool,
                    'redirectUrl': TBD
                },
                'below940': bool,
                'existingService': bool,
                'expectedCompDate': TBD
            }
        """

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
        """_summary_

        Args:
            response (requests.Response): _description_

        Returns:
            _type_: _description_
        """

        # TODO: response status/error checking, robust conversion to dict, etc.
        #       (perhaps via ispchecker.tools)

        # for now, just convert to dict with no error checking
        response_dict = response.json()

        # ensure the system has found an exact match for the address
        # TODO: move this message string to a settings/config file
        if response_dict.get("message") != "GREEN - exact match":
            return "No match"

        # get the wireCenter name
        wireCenter = response_dict.get("addrValInfo").get("wireCenter")

        return wireCenter

    def retrieve_offerings(self, access_token, addressId, fullAddress, wireCenter):
        """_summary_

        Args:
            access_token (_type_): _description_
            addressId (_type_): _description_
            fullAddress (_type_): _description_
            wireCenter (_type_): _description_

        Returns:
            _type_: _description_

        .. code-block::

            {
                'fixedWirelessQualified': bool,
                'groupId': TBD,
                'dynamicRuleVersion': TBD,
                'offersList': [
                    {
                        'downloadSpeed': str,
                        'uploadSpeed': str,
                        'downloadSpeedMbps': str,
                        'uploadSpeedMbps': str,
                        'downloadDisplaySpeed': str,
                        'uploadDisplaySpeed': str,
                        'internetTypeSortOrder': int,
                        'internetType': str,
                        'productType': str,
                        'priceType': str,
                        'skuName': str,
                        'price': float,
                        'networkInfrastructure': str,
                        'offerName': str,
                        'mandatoryTechInstallFlag': bool,
                        'qualificationColorName': str,
                        'catalogSpecId': str,
                        'catalogId': str,
                        'offerType': str,
                        'productOfferingId': str,
                        'productIdentifierKey': str,
                        'discountedOtc': float,
                        'discountedRc': float,
                        'otc': float,
                        'rc': float,
                        'strikePrice': float,
                        'discount': list(TBD),
                        'derivedDownSpeed': str,
                        'derivedUpSpeed': str,
                        'offerDescription': str,
                        'priceKey': str,
                        'productDisplayName': str,
                        'description': str,
                        'bmOfferDetails': str,
                        'modem': [
                            {
                                (truncated - SKUs)
                            }
                        ],
                        'groupId': TBD,
                        'vas': [
                            {
                                (truncated - SKUs)
                            }
                        ]
                    }
                ],
                'fixedWirelessOffersList': TBD,
                'secureWifiOffersList': TBD,
                'dialUp': bool,
                'noCatalogueProducts': bool,
                'errorMessage': TBD,
                'billingSource': TBD,
                'status': str,
                'defaultOffer': bool,
                'cityOmaha940Offer': bool,
                'orderNumber': TBD,
                'gfastFlag': bool,
                'giftCardFlag': bool,
                'sling': bool,
                'thirtyDollarFiberOffer': bool,
                'epix': bool,
                'gc200for940M': bool,
                'caf': bool,
                'defaultSpeedServiceFailure': TBD
            }
        """

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

    def parse_offerings(self, response: requests.Response):
        """_summary_

        Args:
            response (requests.Response): _description_

        Returns:
            _type_: _description_
        """

        # TODO: response status/error checking, robust conversion to dict, etc.
        #       (perhaps via ispchecker.tools)

        # for now, just convert to dict with no error checking
        response_dict = response.json()

        # get the top speed in mbps
        # CenturyLink lists the fastest offer first, per their website
        self.top_speed = response_dict.get("offersList")[0].get("downloadSpeedMbps")

        # this also means that it's available by definition
        self.available = True

        return response_dict


class Verizon(ISP):
    def __init__(self, address_dict: dict):

        self.address = address_dict
        self.available = "Undetermined"
        self.top_speed = "Undetermined"
        self.metadata = {}

        print(" Verizon LTE ".ljust(LJUST, ".") + " ", end="", flush=True)

        # retrieve plan availability
        r = self.retrieve_plan_availability()

        # get dict from response, parse availability, and update self.metadata
        self.metadata.update(self.parse_plan_availability(r))

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
        """_summary_

        Args:
            response (requests.Response): _description_

        Returns:
            _type_: _description_

        .. code-block::

            (response mapping is incomplete)

            {
                'output': {
                    'qualified': bool,
                    'reservation': TBD,
                    'emailAddress': TBD,
                    'addressLine1': str,
                    'addressLine2': str,
                    'city': str,
                    'state': str,
                    'zipCode': str,
                    'reasonCode': str,
                    'addressType': TBD,
                    'installType': TBD,
                    'floorToStreetsMap': {},
                    'phoneNumber': TBD,
                    'addressfromAccount': bool,
                    'currentFloorNumber': TBD,
                    'eventCorrelationId': str,
                    'verifyE911Address': bool,
                    'polylines': {},
                    'launchType': str,
                    'apartmentNumberRequired': bool,
                    'floorPlanAvailable': bool,
                    'addressMapStatus': TBD,
                    'maxFloor': TBD,
                    'buildingDetails': TBD,
                    'uberPinEligible': bool,
                    'intersectionCoordinatesLst': TBD,
                    'coveragePercentage': TBD,
                    'equipType': TBD,
                    'addressDescriptorList': TBD,
                    'bundleNames': TBD,
                    'qualified4GHome': bool,
                    'qualifiedCBand': bool,
                    'preOrder5GFlow': bool,
                    'preOrderLaunchDate': TBD,
                    'isExpiredCart': bool,
                    'isStreetSelected': bool,
                    'isRevisitor': bool,
                    'uberPinQualificatioIsRequired': bool,
                    'displayStreetSelection': bool,
                    'mucOfferEligible': bool,
                    'storeSessionId': str,
                    'fiosQualified': bool,
                    'HSI': bool,
                    'fiosResponse': {
                        'meta': {
                            'code': str,
                            'description': str,
                            'timestamp': str
                        },
                        'qualification': {
                            'gigqualified': bool,
                            'fiosqualified': bool,
                            'hsiqualified': bool,
                            'posturl': str,
                            'visitId': str,
                            'visitorId': str,
                            'commonLq': str,
                            'lbo': TBD,
                            'captcha': TBD
                        },
                        'postValues': {
                            'campaignCode': str,
                            'config': {
                                'addressInfo': {
                                    'addressid': str,
                                    'addressLine1': str,
                                    'addressLine2': str,
                                    'city': str,
                                    'state': str,
                                    'zipCode': str
                                }
                            },
                            'vendorName': str,
                            'targetUrl': str
                        },
                        'qualificationDetails': {
                            'data': {
                                'hoaServiceType': TBD,
                                'qualified': TBD,
                                'services': TBD,
                                'pendingOrder': TBD,
                                'smartCartDetails': TBD,
                                'inService': TBD,
                                'hoaFlag': TBD,
                                'hoaContractNumber': TBD,
                                'isLennarEligible': TBD,
                                'tarCode': TBD,
                                'cpnelg': TBD,
                                'fiosSelfInstall': TBD,
                                'fiosReady': TBD,
                                'quantumEligible': TBD,
                                'parsedAddress': TBD,
                                'fiveG': bool,
                                'addressNotFound': bool,
                                'encryptedAddressFor5G': TBD,
                                'qualified4GHome': bool,
                                'state': TBD,
                                'zip': TBD,
                                'isError': TBD,
                                'wirelessPlanType': TBD,
                                'occupancyType': TBD
                            }
                        },
                        'multipleAddressMatch': TBD,
                        'parsedAddress': TBD
                    }
                },
                'errorMap': TBD,
                'statusMessage': str,
                'statusCode': str
            }
        """

        # TODO: response status/error checking, robust conversion to dict, etc.
        #       (perhaps via ispchecker.tools)

        # for now, just convert to dict with no error checking
        response_dict = response.json()

        # TODO: find reliable way of checking if address is valid

        # check if 4G LTE home internet is available at address
        self.available = response_dict.get("output").get("qualified4GHome")

        # if available, then speed is 50 mbps
        # TODO: find this value dynamically via another API request
        if self.available:
            self.top_speed = 50
        else:
            self.top_speed = 0

        return response_dict


if __name__ == "__main__":

    main()
