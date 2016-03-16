'''
iframe_extract.py - download video and ffmpeg i-frame extraction
Usage: 
(ex) python iframe_extract.py -u https://www.youtube.com/watch?v=dP15zlyra3c

Test Cases
python iframe_extract.py -u https://www.youtube.com/watch?v=dP15zlyra3c
python iframe_extract.py -u https://www.youtube.com/watch?v=usYC_Z36rHw
python iframe_extract.py -u https://www.youtube.com/watch?v=I4L2XirSJw0
python iframe_extract.py -u https://www.youtube.com/watch?v=2wCgpdeQWZA
python iframe_extract.py -u https://www.youtube.com/watch?v=iyisAjHdhas
python iframe_extract.py -u https://www.youtube.com/watch?v=GqV7KMjw9jY
python iframe_extract.py -u https://www.youtube.com/watch?v=Yb2okDst0oc

This code does two things:
1. Download using youtube-dl
2. Extract i-frames via ffmpeg
'''

from __future__ import unicode_literals
import youtube_dl

import sys
import os
import subprocess
import argparse
import glob



def iframe_extract(inFile):

# extract i-frame using ffmpeg
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
    print "creating iframes ...."
    subprocess.call(cmd)

    # Move the extracted iframes to a subfolder
    # imgPrefix is used as a subfolder name that stores iframe images
    cmd = 'mkdir -p ' + imgPrefix
    os.system(cmd)
    print "make subdirectoy", cmd
    mvcmd = 'mv ' + imgPrefix + '*.png ' + imgPrefix
    print "moving images to subdirectoy", mvcmd
    os.system(mvcmd)



def get_info_and_download(download_url):

    # Get video meta info and then download using youtube-dl

    ydl_opts = {}

    # get meta info from the video
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(download_url, download=False)

    # renaming the file 
    # remove special characters from the file name
    out = ''.join(c for c in meta['title'] if c.isalnum() or c =='-' or c =='_' ) 
    extension = meta['ext']
    video_out = out + '.' + extension
    cmd = ['youtube-dl', '-k', '-o', video_out, download_url]

    # download the video
    subprocess.call(cmd)

    # Sometimes output file has format code in name such as 'out.f248.webm'
    # so, in this case, we want to rename it 'out.webm' 
    glob_str = '*.' + extension
    for f in glob.glob(glob_str):
       if out in f:
          if os.path.isfile(f):
             video_out = f
             break
       
    # call iframe-extraction : ffmpeg
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

'''
Usage sample:
    syntax: python iframe_extract.py -u url
    (ex) python iframe_extract.py -u https://www.youtube.com/watch?v=dP15zlyra3c
'''
if __name__ == '__main__':
    u,i,o = check_arg(sys.argv[1:])
    meta = get_info_and_download(u)
