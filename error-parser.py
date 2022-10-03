import os
import sys
from argparse import ArgumentParser
from glob import glob
from os import listdir
from os.path import isfile, join
import pandas as pd

result = []


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
     files_list = {"sim.ps.log.gz","run.grid.out"}
     for testcase,filenames in files.items():
         pprint(f" TESTCASE : 👉 {testcase}  ")  
         res = {testcase:[]}
         for filename in filenames[1:]:
             pprint(f"     PROCESSING  : {filename}")
             if os.path.basename(filename) in files_list:
                for line in open(filename).readlines():
                    if "UVM_ERROR" in line:
                       res[testcase].append(line)
     result.append(res)  
     df = pd.DataFrame(result)
     df.to_excel("result.xls")                        
   except Exception as e:
     pprint(f" PROCESSING ERROR : {e}") 




def parse_errors(folders):
   try:
     if not os.path.exists(folders):
        pprint(f" ERROR :  {folder} Does Not Exist ")
        sys.exit()
   
     files = {}
     for folder in  glob(folders+"/*", recursive = True):
         if not isfile(folder):
            files.setdefault(os.path.basename(folder),[folder])
     for testcase,folder in files.items():
         for filenames in  glob(folder[0]+"/**/*", recursive = True):
             if isfile(filenames): 
             	files[testcase].append(filenames)
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
   print(result)
