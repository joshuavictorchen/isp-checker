import sys
import traceback
from ispchecker import tools as t
from ispchecker.address import Address
from ispchecker.spectrum import Spectrum
from ispchecker.centurylink import CenturyLink
from ispchecker.verizon import Verizon

DIVIDER = (
    "\n ------------------------------------------------------------------------------ "
)


def main():

    # rudimentary CLI - outputs just printed to the console for now

    # if no arg is provided, then allows users to start the program and continuously check different addresses/URLs
    # if args are provided, then simply executes a one-off ISP check
    args = sys.argv

    if len(args) > 1:

        # create a string from the sys args list
        # the first element in list is the name of the calling function; it is ignored
        arg = " ".join(sys.argv[1:])

        # check the address and exit the program
        check_address(arg)
        sys.exit()

    while True:

        print(DIVIDER)

        try:

            # gather user input as one string; re-prompt if no input is provided
            # convert arg to lowercase for input processing
            arg = ""
            while len(arg) == 0:
                arg = input("\n>>> ").lower()

            # exit the program
            if arg in ("quit", "q"):
                break

            # check the address (input checking/cleaning routines TBD)
            else:
                check_address(arg)

        except Exception:

            # if an exception was thrown, print the stack trace
            print(
                "\n ERROR: prototype interface encountered the following exception:\n"
            )
            [print(f"   {i}") for i in traceback.format_exc().split("\n")]


def check_address(arg):

    # check ISP availability for the supplied argument (address or supported URL)

    # instantiate an Address
    a = Address()

    # load in the argument
    t.print_divider()
    a.parse_address(arg)
    t.print_recursive_dict(a.address)

    # check for ISP availability
    a.check_isps([Spectrum(), CenturyLink(), Verizon()])


if __name__ == "__main__":

    main()
