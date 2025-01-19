import os
import argparse
from breakMP3IntoChunks import MediaFileBreaker

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Breaks mp3 file into chunks")
    parser.add_argument("source_file", type=str,
                        help="Path to text file containing information about file to be split, where to put output chunks, and names and position of chunks etc .")
    parser.add_argument("--destination_subdirectory", type=str,
                        help=" (optional) Name of the subdirectory to move chunks into. Overrides location in text file")
    parser.add_argument("--delimiter", default="=", type=str,
                        help=" (optional) parameter delimiter.")
    parser.add_argument("--operation", default="break", help="what do you want me to do? break= break a file into segments.")
    parser.add_argument("--codec_in", type=str, default="mp3", help="(optional))input file codec, e.g mp3")

    parser.add_argument("--codec_out", type=str, default="mp3", help="(optional) output file codec, e.g mp3")

    args = parser.parse_args()
    srcTextFile, dstPath, delimiter, operation, codecin, codecout = args.source_file, args.destination_subdirectory, args.delimiter, args.operation, args.codec_in, args.codec_out

    match operation:
        case "break":
            if os.path.exists(srcTextFile):
                afb = MediaFileBreaker(srcTextFile, dstPath, tdCodec=codecout)
                afb.go()

        case "downsize":
            pass
            afb = MediaFileBreaker(Operation="downsize",SrcPath=srcTextFile)
            afb.go()
