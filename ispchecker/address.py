import sys
from ispchecker.spectrum import Spectrum
from ispchecker.centurylink import CenturyLink
from ispchecker.verizon import Verizon


class Address:
    """Placeholder text.

    **Relevant instance attributes:** \n
        * **address** (*dict*): Dictionary of addresses.
        * **isps** (*dict*): Dictionary of instantiated ISPs.
    """

    def __init__(self):

        self.address = {}
        self.isps = {}

    def check_isps(self):

        if self.address == {}:
            print("\n Address is empty - please parse in an address first.")
            return None

        isps = {
            "Spectrum": Spectrum(self.address),
            "CenturyLink": CenturyLink(self.address),
            "Verizon LTE": Verizon(self.address),
        }

        self.isps = isps

        return isps

    def parse_address(self, full_address):

        # check if address is actually a zillow or trulia URL
        # if so, parse the address out of the URL before proceeding
        if "www.zillow.com" in full_address:
            full_address = self.parse_url("zillow", full_address)
        elif "www.trulia.com" in full_address:
            full_address = self.parse_url("trulia", full_address)

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

    def parse_url(self, site, full_address):
        """_summary_

        Args:
            site (_type_): _description_
            full_address (_type_): _description_

        Returns:
            _type_: _description_
        """

        # this is a temporary, janky, stop-gap measure for parsing addresses from URLs

        # get list of address components (strings) from URL
        #   1. remove query params (everything after '?')
        #   2. split by '/' and obtain URL section containing the address (url_index)
        #   3. make everything UPPER CASE for downstream string comparison consistency
        #   4. split URL tokens by '-' for parsing

        # first, set up parsing variables
        # supported urls: zillow, trulia (hard-coded for now)
        # more thorough documentation TBD
        if site == "zillow":
            url_index = 4
            state_index = -2
            final_trim = None

            # zillow links come in two forms, depending on if the listing was searched for directly,
            # or if the listing was shared via the 'get shareable link' feature
            # perform some string cleaning to force consistency for zillow URLs
            full_address = full_address.replace(",", "").replace("_rb", "")

        elif site == "trulia":
            url_index = 6
            state_index = -4
            final_trim = -1
        else:
            return full_address

        # now, break down address
        address_breakdown = (
            full_address.split("?")[0].split("/")[url_index].upper().split("-")
        )

        # iterate through the relevant address components until a street abbreviation is found
        # if no abbreviations are found, then terminate the program
        # iteration stops at state_index, so that state abbreviations are not mixed up with street abbreviations
        valid_url = False
        for index, element in enumerate(address_breakdown[:state_index]):
            if element in STREET_ABBREVIATIONS:
                valid_url = True
                break

        if not valid_url:
            sys.exit(
                "\n Error: unable to parse URL. Please verify the URL or enter the address directly."
            )

        # add a comma after the street abbreviation (important for downstream parsing)
        address_breakdown[index] += ","

        # add a comma after the last token of the city name (i.e., one token before the state index)
        # (important for downstream parsing)
        address_breakdown[state_index - 1] += ","

        # join the components back together, leaving out extra tokens as applicable
        full_address = " ".join(address_breakdown[0:final_trim])

        return full_address


# hard-coded list of street abbreviations
# (placed at the bottom of this file for legibility)
# this is a temporary stop-gap measure for parsing addresses from URLs
# source: https://pe.usps.com/text/pub28/28apc_002.htm
STREET_ABBREVIATIONS = (
    "ALY",
    "ANX",
    "ARC",
    "AVE",
    "BYU",
    "BCH",
    "BND",
    "BLF",
    "BLFS",
    "BTM",
    "BLVD",
    "BR",
    "BRG",
    "BRK",
    "BRKS",
    "BG",
    "BGS",
    "BYP",
    "CP",
    "CYN",
    "CPE",
    "CSWY",
    "CTR",
    "CTRS",
    "CIR",
    "CIRS",
    "CLF",
    "CLFS",
    "CLB",
    "CMN",
    "CMNS",
    "COR",
    "CORS",
    "CRSE",
    "CT",
    "CTS",
    "CV",
    "CVS",
    "CRK",
    "CRES",
    "CRST",
    "XING",
    "XRD",
    "XRDS",
    "CURV",
    "DL",
    "DM",
    "DV",
    "DR",
    "DRS",
    "EST",
    "ESTS",
    "EXPY",
    "EXT",
    "EXTS",
    "FALL",
    "FLS",
    "FRY",
    "FLD",
    "FLDS",
    "FLT",
    "FLTS",
    "FRD",
    "FRDS",
    "FRST",
    "FRG",
    "FRGS",
    "FRK",
    "FRKS",
    "FT",
    "FWY",
    "GDN",
    "GDNS",
    "GTWY",
    "GLN",
    "GLNS",
    "GRN",
    "GRNS",
    "GRV",
    "GRVS",
    "HBR",
    "HBRS",
    "HVN",
    "HTS",
    "HWY",
    "HL",
    "HLS",
    "HOLW",
    "INLT",
    "IS",
    "ISS",
    "ISLE",
    "JCT",
    "JCTS",
    "KY",
    "KYS",
    "KNL ",
    "KNLS",
    "LK",
    "LKS",
    "LAND",
    "LNDG",
    "LN",
    "LGT",
    "LGTS",
    "LF",
    "LCK",
    "LCKS",
    "LDG",
    "LOOP",
    "MALL",
    "MNR",
    "MNRS",
    "MDW",
    "MDWS",
    "MEWS",
    "ML",
    "MLS",
    "MSN",
    "MTWY",
    "MT",
    "MTN",
    "MTNS",
    "NCK",
    "ORCH",
    "OVAL",
    "OPAS",
    "PARK",
    "PKWY",
    "PASS",
    "PSGE",
    "PATH",
    "PIKE",
    "PNE ",
    "PNES",
    "PL",
    "PLN",
    "PLNS",
    "PLZ",
    "PT",
    "PTS",
    "PRT",
    "PRTS",
    "PR",
    "RADL",
    "RAMP",
    "RNCH",
    "RPD",
    "RPDS",
    "RST",
    "RDG",
    "RDGS",
    "RIV",
    "RD",
    "RDS",
    "RTE",
    "ROW",
    "RUE",
    "RUN",
    "SHL",
    "SHLS",
    "SHR",
    "SHRS",
    "SKWY",
    "SPG",
    "SPGS",
    "SPUR",
    "SQ",
    "SQS",
    "STA",
    "STRA",
    "STRM",
    "ST",
    "STS",
    "SMT",
    "TER",
    "TRWY",
    "TRCE",
    "TRAK",
    "TRFY",
    "TRL",
    "TRLR",
    "TUNL",
    "TPKE",
    "UPAS",
    "UN",
    "UNS",
    "VLY",
    "VLYS",
    "VIA",
    "VW",
    "VWS",
    "VLG",
    "VLGS",
    "VL",
    "VIS",
    "WALK",
    "WALL",
    "WAY",
    "WAYS",
    "WL ",
    "WLS",
)
