"""
Test the api calls
"""

import pytest
import random
import json
import pandas as pd
from ct_schools import schools

random.seed(100)

def get_wordlist():

    # modify if your system doesn't have this list
    wordfile = "/usr/share/dict/words"
    wordlist = open(wordfile).read().split("\n")
    return wordlist

WORDLIST = get_wordlist()

def test_wordlist_is_long_list():
    assert isinstance(WORDLIST, list)
    assert len(WORDLIST) > 1000

def test_closest_returns_dataframe():
    for n in ["Shepaug","Darien","FINFORFLE","","@#$#@"]:
        assert isinstance(schools.closest(n), pd.DataFrame)

def test_closest_returns_dataframe_of_proper_length():

    for l in [ x * 10 for x in range(100) ]:
        for n in ["Shepaug","Darien","FINFORFLE","","@#$#@"]:
            result = schools.closest(n, lim=l)

            # use -s to disable per-test capturing
            # print (l, len(result))
            
            assert len(result) == l
        
def test_exact_success_returns_dataframe():
    assert isinstance(schools.exact("SHEPAUG VALLEY SCHOOL"), pd.DataFrame)

def test_exact_fail_rasies_exception():
    with pytest.raises(Exception):
        schools.exact("FAKE FAKE SCHOOL")

def test_contains_fail_returns_0_length_DataFrame():
    result = schools.contains(" FAKE ")
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0

def test_contains_returns_DataFrame():
    
    for i in range(25):

        word = random.choice(WORDLIST)
        result = schools.contains(word)
        assert isinstance(result, pd.DataFrame)
        assert len(result) >= 0

def test_contains_result_contains_string():

    for i in range(2500):
        word = random.choice(WORDLIST)
        result = schools.contains(word)
        for w in result["School Name"]:
            assert word.upper().strip() in w.upper().strip()
            
            print ("FOUND '" + word + "' in " +  w)

        
def test_fuzzy_returns_dataframe():

    for i in range(10):
        word = random.choice(WORDLIST)
        fuzz = random.choice(range(101))

        result = schools.fuzzy(word, ratio=fuzz)

        assert isinstance(result, pd.DataFrame)
        assert len(result) >= 0

        if len(result) > 0:
            print "FOUND " + str(len(result)) + " results for '" + word +  "'"\
                "with ratio " + str(fuzz)

def test_jsonify_returns_json():

    result = schools.jsonify(schools.closest("JAKE"))
    assert isinstance(json.loads(result), list)

    result = schools.jsonify(schools.exact("Shepaug Valley School"))
    assert isinstance(json.loads(result), list)
    

def test_dictify_returns_dict():

    result = schools.dictify(schools.closest("JAKE"))
    assert isinstance(result, list)

    result = schools.dictify(schools.exact("Shepaug Valley School"))
    assert isinstance(result, list)
    
    
