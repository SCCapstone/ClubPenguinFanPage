import sys
from django.test import TestCase
import os

from Main.views import clean_up, make_sw_list, tfidf, lda, pos

class TFIDFTest(TestCase):
    @classmethod
    def test_clean_up(self):
        print("testing method clean_up from Main.views")
        txt = "The dog\r\n ran over\r\n the hill\r\n."
        clean_txt = ['The dog', ' ran over', ' the hill', '.']
        
        assert(clean_up(txt) == clean_txt)
    
    def test_tfidf(self):
        print("testing method tfidf from Main.views")
        txt = "Some years ago--never mind how long precisely--having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. "
        txt = clean_up(txt)
        sw = make_sw_list('')
        expected_output = ['little', 0.47140452079103173]
        assert(tfidf(txt, sw)[0].iloc[0].to_list() == expected_output)
        
    def test_lda(self):
        print("testing method lda from Main.views")
        txt = "Call me Ishmael. Some years ago--never mind how long precisely--having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. It is a way I have of driving off the spleen, and regulating the circulation. Whenever I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; whenever I find myself involuntarily pausing before coffin warehouses, and bringing up the rear of every funeral I meet; and especially whenever my hypos get such an upper hand of me, that it requires a strong moral principle to prevent me from deliberately stepping into the street, and methodically knocking people's hats off--then, I account it high time to get to sea as soon as I can. This is my substitute for pistol and ball. With a philosophical flourish Cato throws himself upon his sword; I quietly take to the ship. There is nothing surprising in this. If they but knew it, almost all men in their degree, some time or other, cherish very nearly the same feelings towards the ocean with me."
        txt = clean_up(txt)
        sw = ''
        numberoftopics = 3
        expected_output = 'Topic 10.500 "little"0.500 "time"Topic 20.500 "little"0.500 "time"Topic 30.500 "little"0.500 "time"'
        outputstring, file_string, newtext = lda(txt, sw, numberoftopics)
        assert(file_string.replace('\n', '') == expected_output)
        
    def test_pos(self):
        print("testing method pos from Main.views")
        txt = "Call me Ishmael. Some years ago--never mind how long precisely--having little or no money in my purse, and nothing particular to interest me on shore, I thought I would sail about a little and see the watery part of the world. "
        txt = clean_up(txt)
        sw = ''
        outputstring, file_string, textout = pos(txt, sw)
        expected_output = 'Call_VBIshmael_NNP._.Some_DTyears_NNSago_RB--_:mind_VBlong_JJprecisely_RB--_:having_VBGlittle_JJmoney_NNpurse_NN,_,particular_JJshore_NN,_,I_PRPthought_VBDI_PRPsail_VBPlittle_JJwatery_JJworld_NN._.'
        assert(file_string.replace('\n', '') == expected_output)