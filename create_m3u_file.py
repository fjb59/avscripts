import argparse
import os
from includes import get_media_file_type

def createm3u(tSrc: str,tDst :str,tExclude: str):
    if ',' in tSrc:
        sourceFiles = tSrc.split(',')
    else:
        if os.path.isfile(tSrc):
            sourceFiles = [tSrc]
        elif os.path.isdir(tSrc):
            pass
        else:
            print ("Invalid source parameter.")
            exit(-1)
        for infile in sourceFiles:
            print (get_media_file_type(infile))
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="creates m3u files from files or a folder")
    parser.add_argument("source", type=str,
                        help="A quoted comma seperated list of files, or a folder name.")
    parser.add_argument("output_file", type=str,
                        help="Name of m3u to write changes to. The file will be overwritten")
    parser.add_argument("--exclude", default="", type=str,
                        help=" (optional) Quoted comma seperated list of files to exlude when generatin m3u from a folder.")


    args = parser.parse_args()
    srcTextFile, dstFile, excluded,  = args.source, args.output_file, args.exclude
    createm3u(srcTextFile,dstFile,excluded)
