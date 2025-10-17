
import glob
import os
import tqdm
from CRN import *

path="utils/biomodels/BIOMD*"
files = sorted(glob.glob(path))

skip = ["utils/biomodels/BIOMD0000000013.xml" #works but slow
        ,"utils/biomodels/BIOMD0000000024.xml" #delay error
        ,"utils/biomodels/BIOMD0000000025.xml" #delay error
        ,"utils/biomodels/BIOMD0000000034.xml" #delay error
        ,"utils/biomodels/BIOMD0000000055.xml" # TIME involved
        ]

def dropWhile(list_, skiplist):
    skip = skiplist.copy()
    l = list_.copy()
    
    while skip != []:
        if l[0] in skip:
            skip = skip[1:]
        l = l[1:]
    return l


fails="fail.log"

report = []
success = 0
total = 0



with open(fails, "w") as f:
    total += 1
    f.write("Parsing failed on the following files\n------------------------\n")

    files = dropWhile(files, skip)
    print ("Starting from ", files[0])
    for file in tqdm.tqdm(files):
        try:
            crn = CRN(file)
            success += 1
        except ValueError as e:
            print (file,":",str(e))
            f.write(file + ":" + str(e) + "\n")
        except Exception as e:
            print ("[!]" + file,":",str(e))
            f.write(file + ":" + str(e) + "\n")


print (f"{success/total*100}% success: success={success} fail={total-success} total={total}")



