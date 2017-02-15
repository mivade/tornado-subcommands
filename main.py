from tornado.options import OptionParser


class Parser(OptionParser):
    """Custom :class:`OptionParser` which accepts information about subcommands
    in order to print available subcommands.

    """
    def __init__(self, subcommands=[]):
        super().__init__()
        self.__dict__["_subcommands"] = subcommands

    def print_help(self, file=None):
        super().print_help(file=file)
        if len(self._subcommands) > 0:
            print("Subcommands:")
            for subcommand in self._subcommands:
                print(" ", subcommand)


main = Parser(subcommands=["subone"])
subone = OptionParser()

main.define("verbose", type=bool, default=False, help="Enable verbose output")

rest = main.parse_command_line()
print(main.as_dict())
print(rest)
if rest[0] == "subone":
    print("subone executed")
