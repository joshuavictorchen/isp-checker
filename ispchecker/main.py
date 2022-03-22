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

    # rudimentary CLI that allows users to start the program and continuously check different addresses
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

                # instantiate an Address
                a = Address()

                # load in the argument
                t.print_divider()
                a.parse_address(arg)
                t.print_recursive_dict(a.address)

                # check for isp availability
                a.check_isps([Spectrum(), CenturyLink(), Verizon()])

        except Exception:

            # if an exception was thrown, print the stack trace
            print(
                "\n ERROR: prototype interface encountered the following exception:\n"
            )
            [print(f"   {i}") for i in traceback.format_exc().split("\n")]
            t.print_divider()


if __name__ == "__main__":

    main()
