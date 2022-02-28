from ispchecker import tools as t
from ispchecker.isp import ISP


class Verizon(ISP):
    def main_routine(self):

        # retrieve plan availability
        r = self.retrieve_plan_availability()

        # get dict from response, parse availability, and update self.metadata
        self.metadata.update(self.parse_plan_availability(r))

    def retrieve_plan_availability(self):
        """_summary_

        Returns:
            _type_: _description_

        .. code-block::

            # (response mapping is incomplete)

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
        response = self.session.post(
            url,
            headers=headers,
            json=data,
        )

        return t.convert_response(response)

    def parse_plan_availability(self, response_dict: dict):
        """_summary_

        Args:
            response (dict): _description_

        Returns:
            _type_: _description_
        """

        # TODO: find reliable way of checking if address is valid

        # check if 4G LTE home internet is available at address
        if response_dict.get("output").get("qualified4GHome"):
            self.available = "Available"
        else:
            self.available = "No service"

        self.summary.update(
            {
                "addressLine1": response_dict.get("output").get("addressLine1"),
                "zipCode": response_dict.get("output").get("zipCode"),
                "qualified4GHome": response_dict.get("output").get("qualified4GHome"),
            }
        )

        return response_dict
