import os
import argparse

def swapParameters(tSrc,tDest,tDelimiter,tDDelimiter,tForcedOverwrite="no"):
    if os.path.exists(tDest) and tForcedOverwrite != "yes":
        print ("Error. Desitination exists. Please add parameter '--forced_overwrite' to write to desitnation anyway.")
        exit(-1)
    if not os.path.exists(tSrc):
        print ("Error. Souce does not exist. ")
        exit (-2)

    src = open(tSrc, encoding='utf-8')
    dst = open (tDest, "wt", encoding='utf-8')
    for srcLine in src:
        if srcLine == "\n":
            continue
        if tDelimiter not in srcLine:
            continue
        arg1, arg2= srcLine.split(tDelimiter,maxsplit=1)
        arg1, arg2 = arg1.strip(), arg2.strip()
        destLine = arg2+tDDelimiter+arg1+"\n"
        dst.write(destLine)
    src.close()
    dst.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Swaps parameters in a textfile seperated by a delimiter")
    parser.add_argument("source_file", type=str,
                        help="Path to text file containing information pairs of parameters seperated by a delimiter.")
    parser.add_argument("destination_file", type=str,
                        help="Name of file to write changes to")
    parser.add_argument("--delimiter", default="=", type=str,
                        help=" (optional) parameter delimiter.")
    parser.add_argument("--dest_delimiter", default="=", type=str,
                        help=" (optional) parameter  destinaion file delimiter.")
    parser.add_argument("--forced_overwrite",default="no",type=str,help="force overwrite of destination file without prompting")

    args = parser.parse_args()
    srcTextFile, dstPath, delimiter, dDelimiter ,forcedOverwrite = args.source_file, args.destination_file, args.delimiter,args.dest_delimiter,args.forced_overwrite
    swapParameters(srcTextFile,dstPath,delimiter,dDelimiter,forcedOverwrite)