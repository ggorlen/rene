import rene
import unittest
import sys 
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
        a = "asd"
        b = "affd"
        actual = Test.lcs(len(a), len(b), a, b)
        self.assertEqual(actual, 2)

    def test_lists(self):
        """ test lists """
        a = [1, 4, 5, 1, 2]
        b = [4, 1, 3, 2, 1, 5]
        actual = Test.lcs(len(a), len(b), a, b)
        self.assertEqual(actual, 3)

if __name__ == "__main__":
    unittest.main(verbosity=1)

