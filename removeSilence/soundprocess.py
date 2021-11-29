from pydub import AudioSegment
import os
import sys
import removeSilence.silenceremove as sr
# This code is based on 
"""/***************************************************************************************
*    Title: Audio Processing
*    Author: Bala Murugan NG
*    Date: 2020/06/13
*    Code version: <code version>
*    Availability: https://github.com/ngbala6/Audio-Processing
*
***************************************************************************************/"""


def soundProcess(filePath):
    sound = AudioSegment.from_file(f'{filePath}')
    print("----------Before Conversion--------")
    print("Frame Rate", sound.frame_rate)
    print("Channel", sound.channels)
    print("Sample Width",sound.sample_width)
    # Change Frame Rate
    sound = sound.set_frame_rate(48000) #set this to 48000, lower if machine get memorry error, this will reduce quality of sound and might effect ML prediction
    # Change Channel
    sound = sound.set_channels(1)
    # Change Sample Width
    sound = sound.set_sample_width(2)
    # Export the Audio to get the changed contentsound.export("convertedrate.wav", format ="wav")
   
    fileName = filePath.split('/')[-1]
   
    sound.export(f"removeSilence/converted/{fileName}converted.wav", format ="wav")
    
    
    for filename in os.listdir(r'removeSilence/converted'):
        filePath = f'removeSilence/converted/{filename}'
        
        silencedFilePath = sr.silenceRemoveFunc(2, filePath)
        return (silencedFilePath)


def soundProcessMain(path):

    filePath = soundProcess(path)
   
    return (filePath)

    


