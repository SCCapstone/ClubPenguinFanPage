import unittest
import sys

sys.path.insert(0, '../Main/Main/')

from views import clean_up

class TFIDFTest(unittest.TestCase):
    
    def test_clean_up(self):
        txt = "The dog\r\n ran over\r\n the hill\r\n."
        clean_txt = ['The dog', ' ran over', ' the hill', '.']
        
        assert(clean_up(txt) == clean_txt)
        

if __name__ == '__main__':
    unittest.main()