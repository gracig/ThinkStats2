"""This file contains code for uses with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2014 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from __future__ import print_function, division

import numpy as np
import sys
import pandas as pd

import nsfg
import thinkstats2

# GG: Exercise done
def ReadFemResp(dct_file='2002FemResp.dct',
                dat_file='2002FemResp.dat.gz',
                nrows=None):

    dct = thinkstats2.ReadStataDct(dct_file)
    resp = dct.ReadFixedWidth(dat_file, compression='gzip', nrows=nrows)
    # CleanFemResp(resp)
    return resp


def ValidatePregnum(resp):
    # Data from codebook
    # prenum: Numero de gravidez por respondente
    # 0    NONE                     2610
    # 1    1 PREGNANCY              1267
    # 2    2 PREGNANCIES            1432
    # 3    3 PREGNANCIES            1110
    # 4    4 PREGNANCIES             611
    # 5    5 PREGNANCIES             305
    # 6    6 PREGNANCIES             150
    # 7-95 7 OR MORE PREGNANCIES     158
    #                      Total   7643
    pregnum_Bin = pd.cut(resp.pregnum,
		                 bins=[-1, 0, 1, 2, 3, 4, 5, 6, 95],
		                 include_lowest=True)
    assert ( pregnum_Bin.value_counts()[0] == 2610 )
    assert ( pregnum_Bin.value_counts()[1] == 1267 )
    assert ( pregnum_Bin.value_counts()[2] == 1432 )
    assert ( pregnum_Bin.value_counts()[3] == 1110 )
    assert ( pregnum_Bin.value_counts()[4] == 611  )
    assert ( pregnum_Bin.value_counts()[5] == 305  )
    assert ( pregnum_Bin.value_counts()[6] == 150  )
    assert ( pregnum_Bin.value_counts()[7] == 158  )
    assert (              len(pregnum_Bin) == 7643 )
    # read the pregnancy frame
    preg = nsfg.ReadFemPreg()
    # make the map from caseid to list of pregnancy indices
    preg_map = nsfg.MakePregMap(preg)
    # iterate through the respondent pregnum series
    for index, pregnum in resp.pregnum.items():
        # Get caseid from the index
        caseid = resp.caseid[index]
        indices = preg_map[caseid]
        # check that pregnum from the respondent file equals
        # the number of records in the pregnancy file
        if len(indices) != pregnum:
            print(caseid, len(indices), pregnum)
            return False
    return True

def main(script):
    resp = ReadFemResp()
    assert(len(resp) == 7643)
    assert( ValidatePregnum(resp) )
    print('%s: All tests passed.' % script)


if __name__ == '__main__':
    main(*sys.argv)
