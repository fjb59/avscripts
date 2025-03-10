import argparse
import os
import re

from includes import get_media_file_type
class m3uClass:
    def __init__(self):
        self.matched_files = None
        self.folder = ""
    def createm3u(self,tDst :str,tExclude: str):
        if len(self.matched_files) >0:
            outfile = open(os.path.join(self.folder,tDst), "wt", encoding='utf-8')
            outfile.write("#EXTM3U\n")
            for tSrc in self.matched_files:
                if os.path.isfile(tSrc):
                   outfile.write(tSrc+"\n")
                elif os.path.isdir(tSrc):
                    pass
                else:
                    print ("Invalid source parameter.")
                    exit(-1)
            outfile.close()

    def find_Media_files(self,path):
        # Extract the regular expression from the path (assuming the last part of the path is the regex)
        delimiter = os.sep
        idx = path.rfind(delimiter)
        found = []
        if idx >1:
            dir_path = path[:idx]
            regex = path[idx + 1:]


            self.folder = dir_path
            pattern = re.compile(regex,re.IGNORECASE)

            # Walk through the directory tree
            for root, _, files in os.walk(dir_path):
                for file in files:
                    # Check if the filename matches the regex pattern
                    if pattern.search(file):
                        found.append(os.path.join(root, file))
            self.matched_files = sorted(found)





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="creates m3u files from files or a folder")
    parser.add_argument("source", type=str,
                        help="A regular expression path including mask. .eg /home/media/movies/all/^test.*\\.mp4$")
    parser.add_argument("output_file", type=str,
                        help="Name of m3u to write changes to. The file will be overwritten")
    parser.add_argument("--exclude", default="", type=str,
                        help=" (optional) Quoted comma seperated list of files to exlude when generatin m3u from a folder.")


    args = parser.parse_args()
    srcMask, dstFile, excluded,  = args.source, args.output_file, args.exclude
    m3uFile = m3uClass()
    m3uFile.find_Media_files(srcMask)
    m3uFile.createm3u(dstFile,excluded)

