import os
import sys
from argparse import ArgumentParser
from glob import glob
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import gzip

from typing import Iterable, List, TypeVar

T = TypeVar("T")


def sort_by_priority_list(values, priority ):
    priority_dict = {k: i for i, k in enumerate(priority)}
    def priority_getter(value):
        return priority_dict.get(os.path.basename(value), len(values))
    return sorted(values, key=priority_getter) 

def getargs():
   parser = ArgumentParser()
   parser.add_argument("-dir", "--directory",help="starts parsing the directory")
   parser.add_argument("-search", "--search",help="starts parsing the directory",required=False,default="UVM_ERROR")
   args = parser.parse_args()
   return args

def pprint(text):
   size = os.get_terminal_size()
   print(text.center(size.columns),"\n")

def process(files):
   try:
     srch = args.search.upper()
     pprint(f"👋 Searching For  🔎 {srch}  ")
     result = []
     peak_result =[]
     testcases = set()
     """ ⬇️ Set priorities  """
     priority = ["sim.ps.log.gz","sim.log.gz"]
     for testcase,filenames in files.items():
         testcase = testcase.upper()
         pprint(f" TESTCASE : 👉 {testcase}  ") 
         filenames = sort_by_priority_list(filenames,priority) 
         for filename in filenames:
             res = []
             pprint(f"     PROCESSING  : {filename}")
             if  filename.endswith(".gz"):
                with gzip.open( filename, 'rb') as f:
                  for line in f: 
                     if srch in line:
                        result.append([testcase,line])
                        res.append(line)
                     if len(res) == 1 and testcase not in testcases:
                        peak_result.append([testcase,line])
                        testcases.add(testcase)
                  if len(res) == 0:
                     result.append([testcase,"     "]) 
                     peak_result.append([testcase,"     "])      
             else:
               # Code is used if its not gz file 
               with open(filename,'r',buffering=100000) as f:
                  for line in f:
                     if srch in line:
                        result.append([testcase,line])
                        res.append(line)
                     if len(res) == 1 and testcase not in testcases:
                        peak_result.append([testcase,line])   
                        testcases.add(testcase)
                  if len(res) == 0:
                     result.append([testcase,"     "]) 
                     peak_result.append([testcase,"     "]) 
             continue
 
     df = pd.DataFrame.from_records(result,columns=["Testcase","Errors"])
     df.index = np.arange(1, len(df) + 1)
     peak_df = pd.DataFrame.from_records(peak_result,columns=["Testcase","Errors"])
     peak_df.index = np.arange(1, len(peak_df) + 1)
     with pd.ExcelWriter('Results.xlsx') as writer:
      df.to_excel(writer, sheet_name='Detailed')
      peak_df.to_excel(writer, sheet_name='Peak')                      
   except Exception as e:
     pprint(f" PROCESSING ERROR : {e}") 

def parse_errors(folders):
   try:
      if not os.path.exists(folders):
        pprint(f" ERROR :  {folder} Does Not Exist ")
        sys.exit()
      files_list = {"sim.ps.log.gz","sim.log.gz"}
      files = {}
      for folder in  glob(folders+"/**/*.gz", recursive = True): 
          if os.path.basename(folder) in files_list:
             files.setdefault(os.path.basename(os.path.dirname(folder)),[]).append(folder)  
      process(files) 
   except  Exception as e:
     pprint(f"Exception : {e}")   


if __name__ == "__main__":
   os.system('clear')
   pprint("##################################")
   pprint("##### ERROR PARSING STARTED  #####")
   pprint("##################################")
   args = getargs()
   pprint(f"DIRECTORY TO BE PARSED  :{args.directory} \n")
   parse_errors(args.directory)
