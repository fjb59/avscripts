import os.path
import glob
from time import ctime
from pathlib import Path
import shutil
from datetime import datetime
src = "E:\\My Pictures\\wnk\\Hollyoaks\\Pale Brunette"
if os.path.isdir(src):
    p = Path(src)
    files = [f for ext in ("*.jpg", "*.png") for f in p.glob(ext)]
    for file in files:

        ct = os.path.getctime(file)
        ft = ctime(ct)
        #ft = ft.strftime("%a-%b-%d-%Y")
        dt = datetime.strptime(ft, "%a %b %d %H:%M:%S %Y")
        date_only = dt.strftime("%a %b %d %Y")

        ft = date_only.replace(" ","-")
        #ft = ft.replace(":", "_")
        destFolder = os.path.join(src,ft)
        baseFile = os.path.basename(file)
        destFile = os.path.join(destFolder, baseFile)

        if not os.path.exists(destFolder):
            print (f"{destFolder} folder does not exist. Creating!")

            os.mkdir(destFolder)
        print (f"Moving {file} to {destFile}")
        shutil.move(file,destFile)
        pass

