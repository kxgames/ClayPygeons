import re
import sys

class Simple(object):

    def __init__(self):

        self.arguments = sys.argv[:]
        self.command = self.arguments.pop(0)

        self.flags = []
        self.options = {}
        self.positional = []

        flag_pattern = re.compile(r"-(\w+)")
        option_pattern = re.compile(r"--(\w+)(?:=(\w+))?")

        for argument in self.arguments:

            flag_match = flag_pattern.match(argument)
            option_match = option_pattern.match(argument)

            if flag_match:
                characters = [flag for flag in flag_match.groups()]
                self.flags.extend(characters)

            elif option_match:
                name, value = option_match.groups()
                self.options[name] = value

            else:
                self.positional.append(argument)

    def get_command(self):
        return self.command

    def get_flags(self):
        return self.flags

    def get_positional(self):
        return self.positional

    def has_flag(self, name):
        return name in self.flags

    def get_flag(self, name, yes=True, no=False):
        return yes if self.has_flag(name) else no

    def has_option(self, name):
        return name in self.options

    def get_option(self, name, default=None, cast=lambda x: x):
        option = self.options.get(name, default)
        return cast(option)

    def get_options(self):
        return self.options

    def get_index(self, index):
        return self.positional[index]

    def has_any(self, *names):
        for name in names:
            if self.has_flag(name): return True
            if self.has_option(name): return True
        return False

    def has_all(self, *names):
        for name in names:
            if self.has_flag(name): continue
            if self.has_option(name): continue
            return False
        return True

parser = Simple()

def option(name, default=None, cast=lambda x: x):
    return parser.get_option(name, default, cast)

def flag(name, yes=True, no=False):
    return parser.get_flag(name, yes, no)

def any(*names):
    return parser.has_any(*names)

def first():
    return parser.index(0)

def second():
    return parser.index(1)

def third():
    return parser.index(2)

if __name__ == "__main__":

    def check_arguments(command, positional, flags, options):

        import random

        # Create a randomly ordered argument list.
        arguments = []

        for argument in positional:
            arguments.append(argument)

        for character in flags:
            arguments.append("-%c" % character)

        for name in options:
            option = "--%s" % name
            if options[name]: option += "=%s" % options[name]
            arguments.append(option)

        random.shuffle(arguments)
        arguments.insert(0, command)

        sys.argv = arguments

        # Make sure all the arguments were properly extracted.
        parser = Simple()

        assert sys.argv == arguments
        
        assert parser.get_command() == command

        for index, argument in enumerate(positional):
            assert parser.get_index(index) == argument

        for flag in flags:
            assert parser.has_any(flag)
            assert parser.has_flag(flag)
            assert parser.get_flag(flag, yes=None) is None

        for name in options:
            assert parser.has_option(name)
            assert parser.get_option(name) == options[name]

        assert parser.has_all(*flags)
        assert parser.has_all(*options.keys())

    # Run the tests!
    check_arguments("simple",
            [], [], {}) 

    check_arguments("positional",
            ["first", "second"], [], {})

    check_arguments("flags",
            [], ['a', 'b', 'c'], {})

    check_arguments("options",
            [], [], {"first" : 'a', "second" : None})

    print "All tests passed!"

    

