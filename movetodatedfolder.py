import argparse
import os.path
import glob
from time import ctime
from pathlib import Path
import shutil
from datetime import datetime


def moveFiles(srcFolder):
    if os.path.isdir(srcFolder):
        p = Path(srcFolder)
        files = [f for ext in ("*.jpg", "*.png") for f in p.glob(ext)]
        for file in files:

            ct = os.path.getctime(file)
            ft = ctime(ct)
            #ft = ft.strftime("%a-%b-%d-%Y")
            dt = datetime.strptime(ft, "%a %b %d %H:%M:%S %Y")
            #date_only = dt.strftime("%a %b %d %Y")

            date_only = dt.strftime("%Y %b %d")
            ft = date_only.replace(" ","-")
            #ft = ft.replace(":", "_")
            destFolder = os.path.join(srcFolder,ft)
            baseFile = os.path.basename(file)
            destFile = os.path.join(destFolder, baseFile)

            if not os.path.exists(destFolder):
                print (f"{destFolder} folder does not exist. Creating!")

                os.mkdir(destFolder)
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