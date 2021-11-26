from pydub import AudioSegment
import os
import sys
import removeSilence.silenceremove as sr


def soundProcess(filePath):
    sound = AudioSegment.from_file(f'{filePath}')
    print("----------Before Conversion--------")
    print("Frame Rate", sound.frame_rate)
    print("Channel", sound.channels)
    print("Sample Width",sound.sample_width)
    # Change Frame Rate
    sound = sound.set_frame_rate(48000) #set this to 48000
    # Change Channel
    sound = sound.set_channels(1)
    # Change Sample Width
    sound = sound.set_sample_width(2)
    # Export the Audio to get the changed contentsound.export("convertedrate.wav", format ="wav")
   
    fileName = filePath.split('/')[-1]
   
    sound.export(f"removeSilence/convertedTest/{fileName}converted.wav", format ="wav")
    
    
    for filename in os.listdir(r'removeSilence/convertedTest'):
        filePath = f'removeSilence/convertedTest/{filename}'
        #os.system("py taBortTystnad/silenceremove.py 3 " + filePath)
        silencedFilePath = sr.silenceRemoveFunc(2, filePath)
        return (silencedFilePath)


def soundProcessMain(path):
    #if len(args) != 1:
     #   sys.stderr.write(
      #      'Usage: soundprocess.py <path to folder>\n')
       # sys.exit(1)
    filePath = soundProcess(path)
   
    return (filePath)

    


