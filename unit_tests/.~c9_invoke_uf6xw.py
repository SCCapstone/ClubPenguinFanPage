import unittest
import sys

sys.path.insert(1, '/path/to/application/app/folder')

    

class TFIDFTest(unittest.TestCase):
    
    def test_clean_up(self):
        txt = "The dog \n ran over \n the hill \r."
        clean_txt = ['The', 'dog', 'ran', 'over', 'the', 'hill']
        
        assert(clean_up(txt) == clean_txt)
        

if __name__ == '__main__':
    unittest.main()