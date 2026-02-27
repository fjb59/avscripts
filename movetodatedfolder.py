import argparse
import os.path
import glob
import re
from time import ctime
from pathlib import Path
import shutil
from datetime import datetime

def getfileDateFromFile(tFilename,pattern = r'\D(\d{8}|\d{4}-\d{2}-\d{2})\D'):
#r'[_-](\d{8})[_-]'
    if os.path.exists(tFilename):
        if pattern == "-":
            ct = os.path.getctime(tFilename)
            ft = ctime(ct)
            # ft = ft.strftime("%a-%b-%d-%Y")
            dt = datetime.strptime(ft, "%a %b %d %H:%M:%S %Y")
        else:

            filename = os.path.basename(tFilename)

            match = re.search(pattern, filename)
            if match is not None:
                date_str = match.group(1)
                date_str = re.sub(r"[-\.]", "", date_str) #date_str.replace(['-','.'],'')
                try:
                    dt = datetime.strptime(date_str, "%Y%m%d")
                    year_only = dt.strftime("%Y")
                except ValueError:
                    ct = os.path.getctime(tFilename)
                    date_str = ctime(ct)
                    dt = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
                    year_only = os.path.join("predated", dt.strftime("%Y"))


            else:
                ct = os.path.getctime(tFilename)
                date_str= ctime(ct)
                dt = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
                year_only = os.path.join("predated",dt.strftime("%Y"))




        date_only = dt.strftime("%b %d")
        ft = date_only.replace(" ", "-")
        return year_only,ft
def moveFiles(srcFolder):
    if os.path.isdir(srcFolder):
        p = Path(srcFolder)
        files = [f for ext in ("*.jpg", "*.png") for f in p.glob(ext)]
        for file in files:

            # ct = os.path.getctime(file)
            # ft = ctime(ct)
            # #ft = ft.strftime("%a-%b-%d-%Y")
            # dt = datetime.strptime(ft, "%a %b %d %H:%M:%S %Y")
            # #date_only = dt.strftime("%a %b %d %Y")
            #
            # date_only = dt.strftime("%Y %b %d")
            # ft = date_only.replace(" ","-")
            # #ft = ft.replace(":", "_")
            year,ft = getfileDateFromFile(file)
            yearFolder = os.path.join(srcFolder, year)
            destFolder = os.path.join(yearFolder,ft)
            baseFile = os.path.basename(file)
            destFile = os.path.join(destFolder, baseFile)

            if not os.path.exists(destFolder):
                print (f"{destFolder} folder does not exist. Creating!")
                os.makedirs(destFolder,exist_ok=True)
                #os.mkdir(destFolder)
            print (f"Moving {file} to {destFile}")
            shutil.move(file,destFile)
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move files to folder based on their created date")
    parser.add_argument("source_folder", type=str,
                        help="Path to text file containing files to be moved.")
    args = parser.parse_args()
    srcFolder = args.source_folder

    moveFiles(srcFolder=srcFolder)

    #datestr = getfileDateFromFile("E:\My Pictures\soaps\Corrie\Alison King\Alison-20241230_20002100_11671.jpg")