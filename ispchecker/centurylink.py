import requests
from ispchecker import tools as t
from ispchecker.isp import ISP


class CenturyLink(ISP):
    def __init__(self, address_dict: dict):

        super().__init__(address_dict)

        t.print_isp_loader("CenturyLink")
        self.execute_centurylink_stack()

        print(self.available)

        if self.summary != {}:
            t.print_recursive_dict(self.summary)

    def execute_centurylink_stack(self):
        """_summary_"""

        # get security token
        access_token = self.retrieve_and_parse_access_token()

        # get initial address response
        address_metadata_response = self.retrieve_address_metadata(access_token)

        # check for returned address matches
        parsed_address_metadata = self.parse_address_metadata(address_metadata_response)

        # exit routine if no matches found
        if not parsed_address_metadata:
            self.available = "Address not found"
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
        # NOTE: NOT checking for null wireCenter (details TBD)
        if wireCenter == "No match":
            self.available = "No service"
            return

        # request offerings using access token, address metadata, and wireCenter
        offering_response = self.retrieve_offerings(
            access_token,
            parsed_address_metadata.get("addressId"),
            parsed_address_metadata.get("fullAddress"),
            wireCenter,
        )

        # parse offering response
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
        response_dict = t.convert_response(self.session.post(url, headers=headers))

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

            # (response mapping may be incomplete)

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
        response = self.session.get(url, headers=headers, params=params)

        return t.convert_response(response)

    def parse_address_metadata(self, response_dict: dict):
        """_summary_

        Args:
            response (dict): _description_

        Returns:
            _type_: _description_
        """

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

        # update summary dict
        self.summary.update(metadata)

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

            # (response mapping may be incomplete)

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
        response = self.session.post(
            "https://api.lumen.com/Application/v4/DCEP-Consumer/identifyAddress",
            headers=headers,
            json=data,
        )

        return t.convert_response(response)

    def parse_wireCenter(self, response_dict: dict):
        """_summary_

        Args:
            response (dict): _description_

        Returns:
            _type_: _description_
        """

        # ensure the system has found an exact match for the address
        # TODO: move this message string to a settings/config file
        if response_dict.get("message") != "GREEN - exact match":
            return "No match"

        # get the wireCenter name
        wireCenter = response_dict.get("addrValInfo").get("wireCenter")

        # update summary dict
        self.summary.update({"wireCenter": wireCenter})

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

            # (response mapping may be incomplete)

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
                                # (truncated - dict of SKUs)
                            }
                        ],
                        'groupId': TBD,
                        'vas': [
                            {
                                # (truncated - dict of SKUs)
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

        response = self.session.post(
            "https://api.centurylink.com/Application/v4/DCEP-Consumer/offer",
            headers=headers,
            json=data,
        )

        return t.convert_response(response)

    def parse_offerings(self, response_dict: dict):
        """_summary_

        Args:
            response (dict): _description_

        Returns:
            _type_: _description_
        """

        # get the top speed in mbps
        # CenturyLink lists the fastest offer first, per their website
        self.summary.update(
            {
                "downloadSpeedMbps": response_dict.get("offersList")[0].get(
                    "downloadSpeedMbps"
                )
            }
        )

        # this also means that it's available by definition
        self.available = "Available"

        return response_dict
