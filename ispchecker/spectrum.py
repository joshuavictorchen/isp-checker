import requests
from ispchecker import tools as t
from ispchecker.isp import ISP


class Spectrum(ISP):
    def __init__(self, address_dict: dict):

        super().__init__(address_dict)

        t.print_isp_loader("Spectrum")

        # retrieve address/session response
        r = self.retrieve_address_and_session_metadata()

        # get dict from response, parse availability, and update self.metadata
        self.metadata.update(self.parse_address_and_session_metadata(r))

        print(self.available)
        t.print_recursive_dict(self.summary)

    def retrieve_address_and_session_metadata(self):
        """_summary_

        Returns:
            _type_: _description_

        .. code-block::

            # (response mapping may be incomplete)

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
        return t.convert_response(self.session.post(url, json=data, headers=headers))

    def parse_address_and_session_metadata(self, response_dict):
        """placeholder text

        Args:
            response (dict): _description_

        Returns:
            _type_: _description_
        """

        # get the relevant Spectrum address metadata by looping through the addresses list
        # and comparing: address line, city, territory (state), zip
        # notes:
        #   1. convert relevant elements UPPERCASE for comparison w/ self.address
        #   2. ignore last token of line1 to avoid comparing things like 'ROAD' and 'RD'
        #   3. only take first 5 digits of zip codes
        spectrum_address_dict = {}
        for i in response_dict.get("addresses"):
            if (
                self.address.get("street").rsplit(" ", 1)[0]
                == i.get("line1").rsplit(" ", 1)[0].upper()
                and self.address.get("city") == i.get("city").upper()
                and self.address.get("state") == i.get("territoryCode").upper()
                and self.address.get("zip")[:5] == i.get("zipCode")[:5]
            ):

                spectrum_address_dict = i

        # update summary dict
        self.summary = {
            "line1": spectrum_address_dict.get("line1"),
            "zipCode": spectrum_address_dict.get("zipCode"),
            "isLocationServiceable": response_dict.get("serviceabilityFlags").get(
                "isLocationServiceable"
            ),
            "locationKey": spectrum_address_dict.get("locationKey"),
            "serviceStatus": spectrum_address_dict.get("serviceStatus"),
        }

        # update availability
        # isLocationServiceable is misleading:
        #   if True, then must also have a locationKey to truly have serviceability
        #   if False, then must also NOT have a locationKey to truly NOT have serviceability
        #   otherwise, serviceability is indeterminate (website UI throws an error and prompts a customer service call)
        if spectrum_address_dict.get("locationKey"):
            if response_dict.get("serviceabilityFlags").get("isLocationServiceable"):
                self.available = "Available"
            else:
                self.available = "Indeterminate"
        elif (
            spectrum_address_dict.get("line1") is None
        ):  # this means no matching address was found in the response
            self.available = "Address not found"
        else:
            self.available = "No service"

        return response_dict

    def get_offers(self, locationKey, transactionId):
        """_summary_

        .. admonition:: TODO

            `This endpoint <https://www.spectrum.com/services/spectrum/buyflow/residential/proxy.api/root-v2/offers>`__
            returns a list of offers and internet speeds when provided with a ``serviceLocationId`` query,
            and ``session-id`` and ``client-id`` headers.

            These the query and header inputs correspond to the ``locationKey`` and ``transactionId`` attributes,
            respectively, in the response dictionary from
            :py:obj:`parse_address_and_session_metadata<ispchecker.main.Spectrum.parse_address_and_session_metadata>`.
            This nomenclature inconsistency is a quirk of the Spectrum API.

            While this endpoint works well in a browser setting, the requests return bad responses when queried
            programmatically. This is likely due to session/cookie issues, which have yet to be worked out.

        Args:
            locationKey (_type_): _description_
            transactionId (_type_): _description_

        Returns:
            _type_: _description_
        """

        url = "https://www.spectrum.com/services/spectrum/buyflow/residential/proxy.api/root-v2/offers"

        querystring = {"serviceLocationId": locationKey}

        headers = {
            "User-Agent": "",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "session-id": transactionId,
            "client-id": transactionId,
            "Connection": "keep-alive",
        }

        return t.convert_response(
            self.session.get(url, headers=headers, params=querystring)
        )
