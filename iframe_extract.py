'''
iframe_extract.py - download video and ffmpeg i-frame extraction

Usage: 
(ex) python iframe_extract.py -u https://www.youtube.com/watch?v=dP15zlyra3c

This code does two things:
1. Download using youtube-dl
cmd = ['youtube-dl', '-f', videoSize, '-k', '-o', video_out, download_url]

2. Extract i-frames via ffmpeg
cmd = [ffmpeg,'-i', inFile,'-f', 'image2','-vf',
        "select='eq(pict_type,PICT_TYPE_I)'",'-vsync','vfr', imgFilenames]
'''

from __future__ import unicode_literals
import youtube_dl

import sys
import os
import subprocess
import argparse
import glob

if sys.platform == "win32":
    FFMPEG_BIN = "ffmpeg.exe"
    MOVE = "move "
    MKDIR = "md "
elif sys.platform == 'linux' or sys.platform == 'linux2':
    FFMPEG_BIN = "ffmpeg"
    MOVE = "mv "
    MKDIR = "mkdir "
elif sys.platform == 'darwin':
    FFMPEG_BIN = "ffmpeg"
    MOVE = "mv "
    MKDIR = "mkdir "


def iframe_extract(inFile):
# ffmpeg -i inFile -f image2 -vf \
#   "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr oString%03d.png

    # infile : video file name 
    #          (ex) 'FoxSnowDive-Yellowstone-BBCTwo.mp4'
    imgPrefix = inFile.split('.')[0]
    # imgPrefix : image file 

    # start extracting i-frames
    home = os.path.expanduser("~")
    ffmpeg = home + '/bin/ffmpeg'

    imgFilenames = imgPrefix + '%03d.png'
  
    cmd = [ffmpeg,'-i', inFile,'-f', 'image2','-vf',
        "select='eq(pict_type,PICT_TYPE_I)'",'-vsync','vfr', imgFilenames]
    
    # create iframes
    print("creating iframes ....")
    subprocess.call(cmd)

    # Move the extracted iframes to a subfolder
    # imgPrefix is used as a subfolder name that stores iframe images
    cmd = MKDIR + '-p ' + imgPrefix
    os.system(cmd)
    print("make subdirectoy=%s" %cmd)
    mvcmd = MOVE + imgPrefix + '*.png ' + imgPrefix
    print("moving images to subdirectoy %s" %mvcmd)
    os.system(mvcmd)



def get_info_and_download(download_url):

    # Get video meta info and then download using youtube-dl

    ydl_opts = {}

    # get meta info from the video
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(download_url, download=False)

    # renaming the file 
    # remove special characters from the file name
    print('meta[title]=%s' %meta['title'])
    out = ''.join(c for c in meta['title'] if c.isalnum() or c =='-' or c =='_' ) 
    print('out=%s' %out)
    extension = meta['ext']
    video_out = out + '.' + extension
    print('video_out=%s' %video_out)
    videoSize = 'bestvideo[height<=540]+bestaudio/best[height<=540]'
    cmd = ['youtube-dl', '-f', videoSize, '-k', '-o', video_out, download_url]
    print('cmd=%s' %cmd)

    # download the video
    subprocess.call(cmd)

    # Sometimes output file has format code in name such as 'out.webm'
    # So, when the best output format happens to be mp4, for example, 'out.webm.mp4' 
    # which is the input file for iframe_extract(). But there is no 'out.webm.mp4' any more.
    # The following will reset the input as the newly merged video output, 'out.webm.mp4' 
    found = False
    extension_list = ['mkv', 'mp4', 'webm']
    for e in extension_list:
       glob_str = '*.' + e
       for f in glob.glob(glob_str):
          if out in f:
             if os.path.isfile(f):
                video_out = f
                found = True
                break
       if found:
          break
       
    # call iframe-extraction : ffmpeg
    print('before iframe_extract() video_out=%s' %video_out)
    iframe_extract(video_out)
    return meta



def check_arg(args=None):

# Command line options
# Currently, only the url option is used

    parser = argparse.ArgumentParser(description='download video')
    parser.add_argument('-u', '--url',
                        help='download url',
                        required='True')
    parser.add_argument('-i', '--infile',
                        help='input to iframe extract')
    parser.add_argument('-o', '--outfile',
                        help='output name for iframe image')

    results = parser.parse_args(args)
    return (results.url,
            results.infile,
            results.outfile)


# Usage sample:
#    syntax: python iframe_extract.py -u url
#    (ex) python iframe_extract.py -u https://www.youtube.com/watch?v=dP15zlyra3c

if __name__ == '__main__':
    u,i,o = check_arg(sys.argv[1:])
    meta = get_info_and_download(u)




'''
-- Test Cases --
# Fox BBC
python iframe_extract.py -u https://www.youtube.com/watch?v=dP15zlyra3c
# If the Moon were replaced with some of our planets
python iframe_extract.py -u https://www.youtube.com/watch?v=usYC_Z36rHw
# CERN News - New boson spotted at the LHC: is it the Higgs?
python iframe_extract.py -u https://www.youtube.com/watch?v=I4L2XirSJw0
# The Large Hadron Collider Returns in the Hunt for New Physics
python iframe_extract.py -u https://www.youtube.com/watch?v=2wCgpdeQWZA
# Cosmic Distance Ladder: Cepheid Variables
python iframe_extract.py -u https://www.youtube.com/watch?v=iyisAjHdhas
# Orion - a brief tour
python iframe_extract.py -u https://www.youtube.com/watch?v=GqV7KMjw9jY
# Amazing Golden Gate Bridge- San Francisco, CA (From The Above)
python iframe_extract.py -u https://www.youtube.com/watch?v=Yb2okDst0oc
# Grand Teton
python iframe_extract.py -u https://www.youtube.com/watch?v=NCTd1IHChug 
'''

