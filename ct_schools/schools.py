from fuzzywuzzy import fuzz, process
import os, re
import pandas as pd

cached = None

#
# schooldf() - Get the schools dataframe, from disk or cache.
#
#       args - none
#
#       rets - Pandas dataframe of all school data
#
#      notes - Always use this to retrieve the data in subsequent
#              functions, rather than loading it directly to prevent
#              unnecessary disk reads.
#
def schooldf():

    global cached

    dir_path = os.path.dirname(os.path.realpath(__file__))

    if cached is None:
        cached = pd.read_csv(os.path.join(dir_path, "data","schools.csv"))

    return cached

#
# name_col() - Get the school name column as a Pandas Series
#
def name_col():
    return schooldf()["School Name"]

#
# clean_name() - Clean a school name for comparison purposes
#                   
#
def clean_name(n):
    return str(n).upper().strip()

#
# clean_series - Clean a Pandas Series of school names 
#
def clean_series(s):
    return s.apply(clean_name)

#
# clean_name_col - Get the school name column from the dataframe and clean
#                  it up for comparison
#
def clean_name_col():
    return clean_series(name_col())

#
# fuzz_ratio - Determine the fuzz ratio (see fuzzywuzzy lib) between two
#              strings
#
def fuzz_ratio(a, b):

    return fuzz.ratio(clean_name(a), clean_name(b))

#
# fuzz_min - Determine whether two strings are at or above the given fuzz
#            ratio
#
def fuzz_min(a, b, min_ratio=90):

    return fuzz_ratio(a,b) >= min_ratio

#
# fuzz_df - Add a FUZZ_RATIO column to the base schools dataframe with the
#           ratio between each school's name and the name argument supplied
#
def fuzz_df(name):

    df = schooldf().copy()

    df["FUZZ_RATIO"] = df["School Name"].apply(lambda x: fuzz_ratio(x, name))

    return df

# def __school_by_name_closest(name, lim=1):

#     df = fuzz_df(name)

#     return df.sort_values(by="FUZZ_RATIO", ascending=False).head(lim)

# def __school_by_name_minfuzz(name, ratio=75):

#     df = fuzz_df(name)

#     return df[df["FUZZ_RATIO"] >= ratio].sort_values(by="FUZZ_RATIO",
#                                                      ascending=False)


# def __school_by_name_exact(name):
#     df = schooldf()
#     ret = df[clean_name_col() == clean_name(name)]

#     if len(ret) < 1:
#         raise Exception("School not found")
#     if len(ret) > 1:
#         raise Exception("Multiple schools found")
#     return ret

# def __school_by_name_contains(name):
#     df = schooldf()
#     ret = df[clean_name_col().str.contains(clean_name(name))]
#     return ret

#
# 
#
# def school_by_name(name, partial=True, min_fuzz=None, closest=True):

#     if closest is not False:
#         return __school_by_name_closest(name)

#     if partial is False:
#         return __school_by_name_exact(name)
    
#     if min_fuzz is not None and type(min_fuzz) is int:
#         return __school_by_name_minfuzz(name, min_fuzz)

#     # default
#     return __school_by_name_contains(name)

def closest(name, lim=1):

    df = fuzz_df(name)

    return df.sort_values(by="FUZZ_RATIO", ascending=False).head(lim)
    
    # return __school_by_name_closest(name,lim=3)


def exact(name):
    df = schooldf()
    ret = df[clean_name_col() == clean_name(name)]

    if len(ret) < 1:
        raise Exception("School not found")
    if len(ret) > 1:
        raise Exception("Multiple schools found")
    return ret
    
    # return __school_by_name_exact(name)

def contains(name):
    df = schooldf()
    ret = df[clean_name_col().str.contains(clean_name(name))]
    return ret
    
    # return __school_by_name_contains(name)

def fuzzy(name, ratio=75):

    df = fuzz_df(name)

    return df[df["FUZZ_RATIO"] >= ratio].sort_values(by="FUZZ_RATIO",
                                                     ascending=False)
    
    # return __school_by_name_minfuzz(name, ratio=ratio)
