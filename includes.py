import subprocess
def get_media_file_type(file_path) -> str:
    allowedCodecs = ('WAV', 'MP3', 'fLAC', 'AAC','MP4','MKV','AVI','TS')
    retVal: str = ""
    with open(file_path, 'rb') as file:
        header = file.read(13)

    # Check for common audio file headers
    if header.startswith(b'RIFF'):
        retVal = "WAV"
    elif header.startswith(b'ID3'):
        retVal = "MP3"
    elif header.startswith(b'fLaC'):
        retVal = "FLAC"
    elif header[4:8] .startswith(b'ftyp'):
        retVal = "MP4"
    elif header.startswith(b'\x1A\x45\xDF\xA3'):
        retVal = "MKV"
    elif header[:4] == b'RIFF' and header[8:12] == b'AVI ':
        retVal = "AVI"
    elif header[0] == 71:
        retVal = "TS"
    else:
        retVal= ""
    file.close()
    if retVal in allowedCodecs:
        return retVal
    else:
        return ""




#exit_code = convert("input.ts", "output.mp4")
#print(f"Process exited with code: {exit_code}")
