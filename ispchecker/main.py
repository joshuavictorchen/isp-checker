from audioop import add
import requests
import sys
import warnings
from cryptography.utils import CryptographyDeprecationWarning
from ispchecker import tools as t

# filter irrelevant deprecation warnings
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

DIVIDER = "\n ---------------------------------------"


def main():

    # create a string from the sys args list
    # the first element in list is the name of the calling function; it is ignored
    full_address = " ".join(sys.argv[1:])

    # instantiate an Address
    a = Address(full_address)
    t.print_recursive_dict(a.address)

    # check ISP offerings for that Address
    # add more functions to this call stack as applicable
    a.check_spectrum()
    a.check_centurylink()
    a.check_verizon_home_LTE()


class Address:
    """Placeholder text.

    Args:
        full_address (str): Placeholder text.

    **Relevant instance attributes:** \n
        * **address** (*dict*): Dictionary of addresses.
        * **isps** (*dict*): Dictionary of ISPs and offerings.
    """

    def __init__(self, full_address):

        self.address = self.parse_address(full_address)
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

        return address_dict

    def check_spectrum(self):

        # spectrum is a 2-step process
        # first step required to get address and session metadata
        # second step uses the metadata to get specific offerings

        print("\n spectrum ... ", end="")

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
        response = requests.post(url, json=data, headers=headers).json()

        # ASSUMING NO ERRORS FOR NOW
        spectrum = [
            max(False, True if i.get("locationKey") else False)
            for i in response.get("addresses")
        ][0]

        print(spectrum)
        self.isps.update({"spectrum": spectrum})

        # 2nd commented out - incorporate later
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

        return spectrum

    def check_verizon_home_LTE(self):

        # verizon is a one-step process

        print("\n verizon home LTE ... ", end="")

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
        ).json()

        # ASSUMING NO ERRORS FOR NOW
        verizon_LTE = response.get("output").get("qualified4GHome")

        print(verizon_LTE)
        self.isps.update({"verizon-LTE": verizon_LTE})

        return verizon_LTE

    def check_centurylink(self):

        print("\n centurylink ... ", end="")

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


if __name__ == "__main__":

    main()
