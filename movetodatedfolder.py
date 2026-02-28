import argparse
import os.path
import glob
import re
from time import ctime
from pathlib import Path
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS



def getfileDateFromFile(tFilename,pattern = r'\D(\d{8}|\d{4}-\d{2}-\d{2})\D', verbose =False):
#r'[_-](\d{8})[_-]'
    if os.path.exists(tFilename):
        if pattern == "-":
            ct = os.path.getctime(tFilename)
            ft = ctime(ct)
            # ft = ft.strftime("%a-%b-%d-%Y")
            dt = datetime.strptime(ft, "%a %b %d %H:%M:%S %Y")
        else:

            filename = os.path.basename(tFilename)

#try getting date from filename via regex pattern

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
#pattern match failed. Try reading metadata.
                img = Image.open(tFilename)
                exif =img.getexif()
                if exif:
                    date_taken = None
                    for tag_id, value in exif.items():
                        tag = TAGS.get(tag_id, tag_id)
                        if TAGS.get(tag_id) == "DateTime":
                            dt = datetime.strptime(value, "%Y:%m:%d %H:%M:%S")

                            year_only = dt.strftime("%Y")
                            date_only = dt.strftime("%m%d")
                            return  year_only,date_only

                        else:
                            if verbose:
                                print(f"{tag}: {value}")
                else:



                        ct = os.path.getctime(tFilename)
                        date_str= ctime(ct)
                        dt = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
                        year_only = os.path.join("predated",dt.strftime("%Y"))




        date_only = dt.strftime("%b %d")
        ft = date_only.replace(" ", "-")
        return year_only,ft
def moveFiles(srcFolder,verbose = False):
    if os.path.isdir(srcFolder):
        p = Path(srcFolder)
        files = [f for ext in ("*.jpg", "*.png") for f in p.glob(ext)]
        for file in files:

            year,ft = getfileDateFromFile(file,verbose=verbose)
            yearFolder = os.path.join(srcFolder, year)
            destFolder = os.path.join(yearFolder,ft)
            baseFile = os.path.basename(file)
            destFile = os.path.join(destFolder, baseFile)

            if not os.path.exists(destFolder):
                if verbose:
                    print (f"{destFolder} folder does not exist. Creating!")
                os.makedirs(destFolder,exist_ok=True)
                #os.mkdir(destFolder)
            if verbose:
                print (f"Moving {file} to {destFile}")
            shutil.move(file,destFile)

    else:
        print (f"{srcFolder} is not a folder.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move files to folder based on their created date")
    parser.add_argument("source_folder", type=str,
                        help="Path to text file containing files to be moved.")
    parser.add_argument("--verbose", type=str, default="false",
                        help="display activity.")
    args = parser.parse_args()
    srcFolder = args.source_folder
    verbose = args.verbose.lower() =="true"

    moveFiles(srcFolder=srcFolder)

    #datestr = getfileDateFromFile(r"E:\My Pictures\wnk\Corrie\Alison King\Alison-Coronation Street_11176.jpg")