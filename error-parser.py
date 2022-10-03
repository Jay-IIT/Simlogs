import os
import sys
from argparse import ArgumentParser
from glob import glob
from os import listdir
from os.path import isfile, join
import pandas as pd
import numpy as np
import gzip



def getargs():
   parser = ArgumentParser()
   parser.add_argument("-dir", "--directory",help="starts parsing the directory")
   args = parser.parse_args()
   return args

def pprint(text):
   size = os.get_terminal_size()
   print(text.center(size.columns),"\n")

def process(files):
   try:
     result = []
     res = dict()
     for testcase,filenames in files.items():
         testcase = testcase.upper()
         pprint(f" TESTCASE : 👉 {testcase}  ")  
         res[testcase] = []
         for filename in filenames[1:]:
             pprint(f"     PROCESSING  : {filename}")
             if filename.endswith(".gz"):
                fp = gzip.open(filename, "rb")
                contents = fp.read()
                fp.close()
                contents = contents.decode('utf-8')
             else:
                contents = open(filename).readlines()   
             for line in contents:
                 if "UVM_ERROR" in line:
                    res[testcase].append(line)
     result.append(res)
     df = pd.DataFrame({ key: pd.Series(val) for x in result for key, val in x.items() })
     df.index = np.arange(1, len(df) + 1)
     df.to_excel("result.xls")                        
   except Exception as e:
     pprint(f" PROCESSING ERROR : {e}") 




def parse_errors(folders):
   try:
      if not os.path.exists(folders):
        pprint(f" ERROR :  {folder} Does Not Exist ")
        sys.exit()
      files_list = {"sim.ps.log.gz","run.grid.out"}
      files = {}
      for folder in  glob(folders+"/**/*", recursive = True):
          if isfile(folder) and  os.path.basename(folder) in files_list:
             files.setdefault(os.path.basename(os.path.dirname(folder)),[os.path.dirname(folder)])
      for testcase,folder in files.items():
          for filenames in  glob(folder[0]+"/**/*", recursive = True):
              if isfile(filenames) and  os.path.basename(filenames) in files_list:
                 files[testcase].append(filenames)
      print(files)
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
