import rene
import sys 
import unittest
from importlib.util import module_from_spec, spec_from_loader

def new_module(code, name):
    module = module_from_spec(spec_from_loader(name, loader=None))
    exec(code, module.__dict__)
    sys.modules[name] = module
    return module

class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        code = rene.generate_code(source_file="lcs.rene")
        cls.lcs = new_module(code, "lcs").lcs

    def test_strings(self):
        """ test strings """
        x = "asd"
        y = "affd"
        actual = Test.lcs(len(x), len(y), x, y)
        self.assertEqual(actual, 2, f"x={x} ; y={y}")

    def test_lists(self):
        """ test lists """
        x = [1, 4, 5, 1, 2]
        y = [4, 1, 3, 2, 1, 5]
        actual = Test.lcs(len(x), len(y), x, y)
        self.assertEqual(actual, 3, f"x={x} ; y={y}")

if __name__ == "__main__":
    unittest.main(verbosity=1)

