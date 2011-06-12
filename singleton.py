import inspect

def singleton(Class):
    """ Decorator function that turns a class into a singleton. """

    # Create a structure to store instances of any singletons that get
    # created.
    instances = {}

    # Make sure that the constructor for this class doesn't take any
    # arguments.  Since singletons can only be instantiated once, it doesn't
    # make any sense for the constructor to take arguments.
    try:
        specification = inspect.getargspec(Class.__init__)
        positional, variable, keyword, default = specification
        message = "Singleton classes cannot accept arguments to the constructor."

        # The constructor should have a self argument, but no others.
        if len(positional) is not 1: raise TypeError(message)
        if variable is not None or keyword is not None: raise TypeError(message)

    # If the class doesn't have a constructor, that's ok.
    except AttributeError:
        pass

    # This function is what the decorator returns.  In turn, this function is
    # responsible for creating and returning the singleton object.
    def get_instance():

        # Check to see if an instance of this class has already been
        # instantiated.  If it hasn't, create one.  The `instances` structure
        # will be preserved between calls to this function.
        if Class not in instances:
            instances[Class] = Class()

        # Return a previously instantiated object of the requested type.
        return instances[Class]

    # Return the decorator function.
    return get_instance

if __name__ == "__main__":

    # This is the simplest possible singleton class, and it should work
    # without issue.

    @singleton
    class Simple: pass

    assert Simple() is Simple()

    # This should fail, because singleton constructors are not allowed to take
    # any arguments.

    try:
        @singleton
        class Broken:
            def __init__(self, illegal):
                pass

    except TypeError:
        pass
    else:
        raise AssertionError



