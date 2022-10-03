import os
import sys
from argparse import ArgumentParser
from glob import glob
from os import listdir
from os.path import isfile, join
import colorama


def progress_bar(progress, total,color =colorama.Fore.YELLOW):
    for i in range(100): 
        percent = 100 * (i/float(total))
        bar = '🤖' * int(percent) + '-' * (100 - int(percent))
        print(color + f"\r\n|{bar}|{percent:.2f}%",end ="\r")  
 



def in_directory(files, directory):
    directory = os.path.join(os.path.realpath(directory), '')
    file = os.path.realpath(file)
    return os.path.commonprefix([file, directory]) == directory

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
     for testcase,filenames in files.items():
         pprint(f" TESTCASE : {testcase} ")  
         for filename in filenames[1:]:
             pprint(f"     PROCESSING  : {filename}")
             numbers = list(range(0,100))
         #    progress_bar(0,100)
 
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
   print(colorama.Fore.RESET)
