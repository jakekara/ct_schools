#
# update.py
# dev script for ct-schools package
# by Jake Kara
# jake@jakekara.com
#
# Get the latest data from state data portal
# to bundle with package
#
# Also add some columns with lat long separate
# from the street address
#

import pandas as pd
import re

def location_split(loc_str):
    result = re.search('.*\((.*),(.*)\).*', loc_str, re.IGNORECASE)

    if result:
        lat = result.group(1)
        lng = result.group(2)

        return (lat,lng)

def get_lat(loc_tup):
    if loc_tup is None: return
    return loc_tup[0]

def get_lng(loc_tup):
    if loc_tup is None: return
    return loc_tup[1]

def download_df():
    URL = "https://data.ct.gov/api/views/shww-dhc6/rows.csv?accessType=DOWNLOAD"

    return pd.read_csv(URL)

def add_cols(df):
    ret = df.copy()

    ret["lat_lng"] = ret["Location 1"].apply(location_split)
    ret["lat"] = ret["lat_lng"].apply(get_lat)
    ret["lng"] = ret["lat_lng"].apply(get_lng)

    print "Found location values for " +\
        str(len(ret[(ret["lat"].notnull()) & (ret["lng"].notnull())]))\
        + " out of " + str(len(ret)) + " records."
        
        
            
    return ret

def save(df):
    df.to_csv("ct_schools/data/schools.csv")


def main():

    save(add_cols(download_df()))

main()
