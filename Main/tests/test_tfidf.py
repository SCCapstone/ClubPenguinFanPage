import sys
from django.test import TestCase
import os

from Main.views import clean_up

class TFIDFTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass
    
    def test_clean_up(self):
        print("testing method clean_up from Main.views")
        txt = "The dog\r\n ran over\r\n the hill\r\n."
        clean_txt = ['The dog', ' ran over', ' the hill', '.']
        
        assert(clean_up(txt) == clean_txt)
        