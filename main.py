
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
        ,"utils/biomodels/BIOMD0000000139.xml" # TIME involved
        ,"utils/biomodels/BIOMD0000000140.xml" # TIME involved
        ,"utils/biomodels/BIOMD0000000141.xml" # TIME involved
        ,"utils/biomodels/BIOMD0000000142.xml" # TIME involved
        ,"utils/biomodels/BIOMD0000000112.xml" # TIME involved
        ,"utils/biomodels/BIOMD0000000162.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000164.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000165.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000167.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000179.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000180.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000196.xml" #delay error
        ,"utils/biomodels/BIOMD0000000237.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000238.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000245.xml" # RATE RULE
        ,"utils/biomodels/BIOMD0000000268.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000286.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000301.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000302.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000316.xml" # SYMBOL ERROR
        ,"utils/biomodels/BIOMD0000000317.xml" # SYMBOL ERROR
        ,"utils/biomodels/BIOMD0000000326.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000375.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000400.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000446.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000450.xml" # PIECEWISE INVOLVED
        ,"utils/biomodels/BIOMD0000000469.xml" # SLOW 
        ,"utils/biomodels/BIOMD0000000470.xml" # SLOW
        ]

        #469 and 470 hyper slow with tellurium

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



