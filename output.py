import sys
from singleton import singleton

class NoPrint:

    def __init__(self, **files):
        self.stdout = sys.stdout
        self.stderr = sys.stderr

        self.files = {
                "stdout" : files["stdout"] if "stdout" in files else True,
                "stderr" : files["stderr"] if "stderr" in files else False }

        class DummyFile:
            def write(self, string): pass

        self.dummy = DummyFile()

    def __enter__(self):
        if self.files["stdout"]:
            sys.stdout = self.dummy
            
        if self.files["stderr"]:
            sys.stderr = self.dummy

    def __exit__(self, *ignore):
        sys.stdout = self.stdout
        sys.stderr = self.stderr

