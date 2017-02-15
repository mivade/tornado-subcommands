import time
from tornado.options import OptionParser


class Subparser(object):
    """Base class for subparsers.

    :param str name: If given, the string used to execute the subcommand. When
        not given, the lowercase class name will be used.

    """
    def __init__(self, name=None):
        self.options = OptionParser()
        self.name = name or self.__class__.__name__.lower()
        self.define_options()

    def define_options(self):
        """Override to define subparser options."""
        pass

    def call(self, parent_options, rest):
        """The command to run when called as a subcommand."""


class Parser(OptionParser):
    """Custom :class:`OptionParser` which accepts information about subcommands
    in order to print available subcommands.

    """
    def __init__(self, subcommands=[]):
        super().__init__()
        self.__dict__["_subcommands"] = subcommands

    def __getattr__(self, name):
        if name == "subcommands":
            return {
                subcommand.name: subcommand
                for subcommand in self.__dict__["_subcommands"]
            }
        else:
            return super().__getattr__(name)

    def print_help(self, file=None):
        super().print_help(file=file)
        if len(self._subcommands) > 0:
            print("Subcommands:")
            for subcommand in self._subcommands:
                assert isinstance(subcommand, Subparser)
                print(" ", subcommand.name, "\n\t", subcommand.__doc__)


class Options(Subparser):
    """Print all options and exit."""
    def define_options(self):
        self.options.define("count", default=1, help="A count")

    def call(self, parent_options, rest):
        self.options.parse_command_line(rest)
        print(parent_options.as_dict())
        print(self.options.as_dict())
        print("Options executed!")


class CountToTen(Subparser):
    """Count to ten and exit."""
    def call(self, parent_options, rest):
        for n in range(1, 11):
            print(n)
            time.sleep(0.2)


def main():
    parser = Parser(subcommands=[Options(), CountToTen(name="count")])
    parser.define("verbose", type=bool, default=False,
                  help="Enable verbose output")
    rest = parser.parse_command_line()

    if len(rest) > 0:
        parser.subcommands[rest[0]].call(parser, rest)


if __name__ == "__main__":
    main()
