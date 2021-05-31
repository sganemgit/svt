
# @author Shady Ganem <shady.ganem@intel.com>

import pandas as pd
import os
from pandas import DataFrame
from datetime import datetime

class dataframe:
    
    def __init__(self, testname):
        self._testname = testname
        self._init_time = datetime.now()
        self._df = DataFrame()
        self._index = None
        self._row = dict()
    
    def flush(self):
        filepath = "/home/{}/logs/{}/table.csv".format(os.environ["USER"], self._testname)
        directory = os.path.dirname(filepath)
        if not os.path.exists(directory):
            os.makedirs(directory)
        self._df.to_csv(filepath) 
    
    def __getitem__(self, key):
        return self._row.get(key, None)
    
    def __setitem__(self, key, val):
        self._row[key] = val

    def get_last_row(self):
        return self._row
        
    def end_row(self):
        now = datetime.now()
        self._row["Time"] = str(now)
        self._df = self._df.append(self._row, ignore_index=True)

