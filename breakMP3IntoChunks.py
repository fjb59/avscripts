import math
import os

from pydub import AudioSegment
import simpleaudio as sa
import ffmpeg
import subprocess
from includes import get_media_file_type
from enum import Enum
import re
from PIL import Image

class modes(Enum):
    audio = 0
    video = 1
class errors(Enum):
    fileNotFound = -1
    pathNotFound = -2
    resizeError = -3
    invalidType = -4
class MediaFileBreaker:
    allowedAudioCodecs = ('WAV','MP3','mp3','FLAC','flac','AAC')
    allowedVideoCodecs = ('AVI','MKV','MP4',"TS",'mpegts','mov,mp4,m4a,3gp,3g2,mj2')
    allowedImageExtensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff','image2')
    allowedOperations = ('break',"quickconvert", "convert","dumpframes")


    @property
    def source_codec(self ):
        return self.sCodec
    @source_codec.setter
    def source_codec(self,tCodec="Mp3"):
        if tCodec in self.allowedAudioCodecs:
            self.mediaType = modes.audio
        if tCodec in self.allowedVideoCodecs:
            self.mediaType = modes.video
        else:
            print ("Source Codec Not Supported")
            return

        self.sCodec=tCodec
    @property
    def destination_codec(self):
        return self.dCodec
    @destination_codec.setter
    def destination_codec(self,tCodec):

        self.dCodec = tCodec

    @property
    def override_codec(self):
        return self.override_codec
    override_codec.setter
    def override_codec(self,isOveridable):
        self.override_codec = isOveridable
    def time_to_milliseconds(self, tTime):
        #tTime is a tuple
        hours, minutes, seconds = tTime
        return (hours * 60 * 60 * 1000) + (minutes * 60 * 1000) + (seconds * 1000)

    def time_difference(self,start, end):

        start_ms = self.time_to_milliseconds(start)
        end_ms= self.time_to_milliseconds(end)
        diff_ms = abs(end_ms - start_ms)
        return diff_ms

    def time_fromstring(self,param,precision="hhmmss"):
        colons = param.count(':')
        sHours,sMinutes,sSeconds = 0,0,0

        try:
            match colons:
                case 1:
                    sHours = 0
                    sMinutes, sSeconds = param.rstrip().split(":")
                case 2:
                    sHours, sMinutes, sSeconds = param.rstrip().split(":")
        except ValueError:
            sHours, sMinutes = param.rstrip().split(":")
            sSeconds = '0'
        match precision:
            case "hhmm":
                retval = int(sHours),int(sMinutes)
            case "ss":
                retval = int(sSeconds)
            case "ms":
                retval = self.time_to_milliseconds((int(sHours),int(sMinutes),int(sSeconds)))
            case _:
                retval = int(sHours),int(sMinutes),int(sSeconds)
        return retval

    def breakFile(self, tSrcTxt, tDstPath, tDelimiter):
        #queue = {}


        srcPath = ""
        dstPath = ""
        sTime = 0
        eTime = 0
        if tDstPath is not None:
            dstPath = tDstPath

        with (open(tSrcTxt, 'r', encoding='utf-8') as myfile):
            for line in myfile:
                if line == "\n":
                    continue
                if line.startswith("#"):
                    continue
                if tDelimiter not in line:
                    continue

                name, param = line.split(tDelimiter)
                name = name.strip().lower()

                match name:
                    case "operation":
                        if param in self.allowedOperations:
                            self.operation = param
                    case "file":
                        self.srcPath = param.strip()
                        if os.path.exists(self.srcPath):
                            header, result = self.get_file_metadata(self.srcPath.strip())
                            if header == '[FORMAT]':
                                self.metaData =result
                                self.formatName = result['format_name']
                                self.formatLongName = result['format_long_name']
                                self.duration = result['duration']
                                self.bitRate = result['bit_rate']
                                self.validFile = True
                                continue
                            else:
                                myfile.close()
                                print (f"File Type not recognised on {self.srcPath}")
                                exit(errors.invalidType)
                            del result

                        else:
                            print(f"error: {self.srcPath} does not exist!")
                            myfile.close()
                            exit(errors.fileNotFound)

                    case "fps":
                        if self.operation in ("dumpframes"):
                            self.fps=int(param.strip())
                            pass
                    case "outputfolder":
                        if dstPath == "":
                            dstPath = param.rstrip()
                            continue
                    case "outputformat":
                        if (param.rstrip() in self.allowedVideoCodecs and self.mediaType == modes.video) or (param.rstrip() in self.allowedAudioCodecs and self.mediaType == modes.audio):
                            self.destination_codec=param.rstrip()
                    case "prefix":
                        self.prefix=param.strip()
                    case "audiostream":
                        audios = int(param.strip())
                        if audios > 0 and audios <= self.metaData["AudioStreams"]:
                            self.audiostream = audios


                    case _ :
                        match self.operation:
                            case "break" | "dumpframes":
                                hyphens = param.count('-')
                                match hyphens:
                                    case 1:
                                        sTime,eTime = param.split('-')
                                        sTime,eTime = sTime.strip(),eTime.strip()
                                        sHours, sMinutes, sSeconds = self.time_fromstring(sTime, precision="hhmmss")
                                        eHours, eMinutes, eSeconds = self.time_fromstring(eTime, precision="hhmmss")
                                        self.addToQueue(name, (sHours, sMinutes, sSeconds,eHours,eMinutes,eSeconds))
                                    case 0:
                                        sTime = param
                                        eTime = -1
                                        hours, minutes, seconds = self.time_fromstring(sTime, precision="hhmmss")
                                        self.addToQueue(name, (hours, minutes, seconds))

                                    case _:
                                        print (f"Invalid line: {line}")
                                        continue
                            case "convert":
                                    if param.count(">") >0:
                                        lFrom,lTo = param.split(">")

                                    



            myfile.close()
            self.dstFolder = os.path.join(os.path.dirname(tSrcTxt), dstPath)
            startTime = 0

            keys = list(self.queue.keys())

            for item in enumerate(keys):

                diff = 0
                itemindex=item[0]
                itemName = item[1]
                if itemName in self.queue:


                    itemTime = self.queue[itemName]
                    match len(itemTime):
                        case 3:
                            startTime = self.time_to_milliseconds(itemTime)
                        case 6:
                            startTime = self.time_to_milliseconds(itemTime[0:3])
                            eTime =  self.time_to_milliseconds(itemTime[3:6])


                    try:
                        here = keys[itemindex]
                        nextName, nextTime = keys[itemindex+1], self.queue[keys[itemindex+1]]
                        if eTime >0:
                            endTime = eTime
                            eTime = -1
                        else:
                            endTime =self.time_to_milliseconds(nextTime)
                        pass
                        #  diff = self.time_difference(itemTime, nextTime)

                    except IndexError:

                        startTime= self.time_to_milliseconds(itemTime[0:3])
                        if eTime > startTime:
                            endTime = eTime
                        else:
                            endTime = -1



                self.writeQueue.append({itemName:(startTime,endTime)})
                #startTime = diff + 1
            del self.queue
        myfile.close()




    def addToQueue(self,tName, tParam):
        if tName not in self.queue:
            self.queue[tName]=tParam
            pass

    def get_file_metadata(self,file_path):
        # Get metadata using ffprobe
        command = [
            "ffprobe",
            "-i", file_path,
            "-show_format",
            "-v", "quiet"
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
        except Exception as e:
            print(f"Error: {e}")

        metadata = {}
        for line in result.stdout.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                metadata[key] = value.strip()


        header =  result.stdout.split("\n")[0]
        # get audio

        try:
            # Run ffprobe to get the number of audio channels
            command = [
            "ffprobe",
            "-i", file_path,                   # Input file
            "-select_streams", "a",            # Select only audio streams
            "-show_entries", "stream=channels",# Show the 'channels' field
            "-of", "default=noprint_wrappers=1:nokey=1", # Simplified output format
            "-v", "error"                      # Suppress unnecessary output

            ]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            audio_streams = result.stdout.strip().splitlines()
            metadata["AudioStreams"] = len(audio_streams)

            #return int(channels) if channels.isdigit() else None
        except Exception as e:
            print(f"Error: {e}")

        #

        return header, metadata

    def getVideoLength(self,input_video):

        if self.duration ==0.0:
            self.metaData, header  = self.get_file_metadata(input_video)


        else:
            return float(self.duration)
    def writeToFile(self,tSourceFileName ="",withM3u=False,asImages = False):
        sections = []
        if not os.path.exists(self.dstFolder):
            os.makedirs(self.dstFolder,exist_ok=True)
        for item in self.writeQueue:
            name = list(item.keys())[0]
            startms,endms = list(item.values())[0]
            start, end =int(startms/1000),int(endms/1000)
            if endms > 0:
                durationInSeconds=end-start
            else :
                durationInSeconds =0
            fullPath = os.path.join(self.rootFolder, self.srcPath)
            lCodec = get_media_file_type(fullPath)
            self.source_codec =lCodec
            self.destination_codec = lCodec



            dstFileName = os.path.join(self.dstFolder, self.prefix+name + "." + self.destination_codec)

            if not os.path.exists(dstFileName) or asImages:

                if self.mediaType == modes.audio:
                    if durationInSeconds>0:
                        audio_segment = AudioSegment.from_file(fullPath, format=self.source_codec, start_second=start,duration=durationInSeconds)
                    else:
                        audio_segment = AudioSegment.from_file(fullPath, format=self.source_codec, start_second=start)

                    if not os.path.exists(self.dstFolder):
                        os.makedirs(self.dstFolder)

                    audio_segment.export(dstFileName,format=self.destination_codec)
                    del audio_segment
                elif  self.mediaType ==modes.video:

                    total_duration = math.ceil(self.getVideoLength(fullPath))
                    if total_duration == -1:
                        print ("Cannot determine file length. File not supported")
                        exit(errors.invalidType)
                    if end>0:
                        end_time = min(end, total_duration)
                    else:
                        end_time = total_duration

                    if not asImages:
                        print(f"creating {dstFileName}")
                        (
                            subprocess.run(
                                [
                                    "ffmpeg",
                                    "-i", fullPath,
                                    "-ss", f"{start:.3f}",
                                    "-to", f"{end_time:.3f}",
                                    "-map", f"0:v:{self.videostream-1}",
                                    "-map", f"0:a:{self.audiostream-1}",
                                    "-c", "copy",
                                    dstFileName,
                                    "-v", "quiet"
                                ],
                                check=True
                            )
                        )

                    else:

                        dstFileName = os.path.join(self.dstFolder, self.prefix + name + "_%05d.png")
                        print (f"processing {dstFileName}" )
                        try:
                            # FFmpeg command
                            command = [
                                "ffmpeg",
                                "-i", fullPath,
                                "-ss", f"{start:.3f}",
                                "-to", f"{end_time:.3f}",
                                "-v", "quiet",
                                "-vf", f"fps={self.fps}",
                                dstFileName  # Example: "frame_%04d.png"
                            ]

                          #  sections.append((start,end))
                            subprocess.run(command, check=True)
                            print("Frames have been extracted successfully.")
                        except subprocess.CalledProcessError as e:
                            print(f"Error running ffmpeg: {e}")
                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")

            else:
                print(f"{dstFileName} already exists. Skipping.")
        # if len (sections) >0 and asImages:
        #     time_filters = "+".join([f"between(t,{start},{end})" for start, end in sections])
        #     name =list(self.writeQueue[0].keys())[0]
        #     dstFileName = os.path.join(self.dstFolder, self.prefix + name + "_%05d.png")
        #     try:
        #         command = [
        #             "ffmpeg",
        #             "-i", fullPath,
        #             "-vf", f"select='{time_filters}',fps={self.fps}",
        #             "-vsync", "vfr",
        #             "-v", "quiet", # no reporting
        #             dstFileName
        #         ]
        #         subprocess.run(command, check=True)
        #         print ("done")
        #
        #     except subprocess.CalledProcessError as e:
        #         print(f"Error running ffmpeg: {e}")
        #     except Exception as e:
        #         print(f"An unexpected error occurred: {e}")
        #

    # !/usr/bin/env python3



    def downscale_images(self,input_dir, output_dir="", percentage=50,outputextension=""):
        if percentage >99:
            print ("you can only shrink images here, not grow them")
            exit(errors.resizeError)
        if output_dir=="":
            output_dir=input_dir
        ratio = 100//percentage
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Loop through all files in the input directory
        for filename in os.listdir(input_dir):
            input_path = os.path.join(input_dir, filename)

            partfile,inputExtension = os.path.splitext(input_path)
            if outputextension == "":
                outputextension = inputExtension
            if (input_dir == output_dir) and (outputextension == inputExtension):
                print ("Source and destination can't be the same!")
                continue
            if not outputextension.startswith("."):
                outputextension = "."+outputextension
            output_path = os.path.join(output_dir, partfile+outputextension)
            # Check if the file is an image
            if filename.lower().endswith(self.allowedImageExtensions):
                try:
                    # Open the image
                    with Image.open(input_path) as img:
                        # Calculate the new size
                        new_width = img.width // ratio
                        new_height = img.height // ratio

                        # Resize the image
                        scaled_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                        # Save the scaled image in the output directory


                        scaled_img.save(output_path,format=outputextension[1:])
                        img.close()
                        scaled_img.close()


                        print(f"Scaled {filename} to {new_width}x{new_height} and saved to {output_path}")

                except Exception as e:
                    print(f"Failed to process {filename}: {e}")



    def playSection(self,tSectionNAme):
        # frst convert the list into the dictionary
        my_dict = {k: v for d in self.writeQueue for k, v in d.items()}
        if tSectionNAme in my_dict:
            startTime, endTime = my_dict[tSectionNAme]
            duration =endTime-startTime
            startTimeInSeconds = int(startTime/1000)
            durationInSeconds = int(duration/1000)
            fullPath=os.path.join(self.rootFolder,self.srcPath)


            audio_segment = AudioSegment.from_file(fullPath,format=self.source_codec,start_second=startTimeInSeconds,duration=durationInSeconds)

            raw_data = audio_segment.raw_data
            sample_rate = audio_segment.frame_rate
            channels = audio_segment.channels
            sample_width = audio_segment.sample_width
            audio_wave = sa.play_buffer(raw_data, num_channels=channels, bytes_per_sample=sample_width,
                                        sample_rate=sample_rate)
            audio_wave.wait_done()


    def export_frames(self,infile,outfolder,frames =[00,00],fpsw=30, quality=1):
        #ffmpeg -ss 00:09:40 -i Part1.1.MP4 -t 00:09:48 -q:v 1 -vf "fps=18" images/output_mp4
        # ffmpeg - ss
        # 00: 06:30 - to
        # 00: 0
        # 8: 14 - i
        # "Subservience.2024.1080p.WEBRip.x264.AAC5.1-[YTS.MX].mp4" - vf
        # "fps=12"
        # dump / meganS_ % 04
        # d.png

        pass


    def getClip(self,filename,startFrame,endFrame,fps=30):
        pass
    def mergeclips(self,inclips,outclip):
        pass
    def export_clip(self,infile,outfolder,startframe=0,endframe=0,fpsw=30,codec = "copy", quality=1):
        #ffmpeg -ss 00:09:40 -i Part1.1.MP4 -t 00:09:48 -q:v 1 -c:copy output.mp4

        pass
    def convert(self,input_fileMask, output, tCodec="copy"):
        codec = tCodec
        regex=re.compile(input_fileMask)
        files = [f for f in os.listdir(source_folder) if regex.search(f)]
        total_files = len(files)
        if total_files ==0:
            print(f"No files found matching the pattern: {input_fileMask}")
            return
        for thisfile in files:
            print (thisfile)


        command = [
            "ffmpeg",
            "-i", input_file,
            "-c", codec,
            output_file
        ]

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for line in process.stderr:
            print(line, end="")  # Print FFmpeg progress in real-time

        process.wait()  # Wait for the process to finish
        return process.returncode

    def __init__(self,Operation="break", SrcTextFile="",SrcPath ="", DstPath="", Delimiter='=',sCodec="MP3", dCodec="mp3"):
        self.queue = {}
        self.writeQueue = []
        self.srcPath=SrcPath
        self.OutputFile=""
        self.mediaType = modes.audio
        self.operation = Operation
        self.prefix = ""
        self.formatName = ""
        self.formatLongName = ""
        self.duration = 0.0
        self.fps = 0
        self.bitRate = 0
        self.audiostream = 1
        self.videostream = 1
        self.metaData = {}

        self.srcTextFile, self.dstFolder, self.delimiter = SrcTextFile, DstPath, Delimiter

        if sCodec in self.allowedAudioCodecs:
            self.source_codec = sCodec
        else:
            self.source_codec = "MP3"
        if dCodec in self.allowedAudioCodecs:
            self.destination_codec = dCodec
        else:
            self.destination_codec = "MP3"

        self.rootFolder = os.path.dirname(self.srcTextFile)


    def go(self):
        match self.operation:
            case "break":
                self.breakFile(self.srcTextFile, self.dstFolder, self.delimiter)
                self.writeToFile()

            case "dumpframes":
                self.destination_codec = "PNG"
                self.breakFile(self.srcTextFile, self.dstFolder, self.delimiter)

                self.writeToFile(asImages=True)
            case "downsize":
                self.downscale_images(self.srcPath,outputextension=".png")


