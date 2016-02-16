'''
iframe.py - ffmpeg i-frame extraction
'''

import sys, getopt, os
import subprocess

# ffmpeg -i inFile -f image2 -vf "select='eq(pict_type,PICT_TYPE_I)'" -vsync vfr oString%03d.png

def main(argv):
	inFile = ''
	oString = 'out'
	usage = 'usage: python iframe.py -i <inputfile> [-o <oString>]'
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","oString="])
	except getopt.GetoptError:
		print usage
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print usage
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inFile = arg
		elif opt in ("-o", "--oString"):
			oString = arg
	print 'Input file is "', inFile
	print 'oString is "', oString

        # need input, otherwise exit
	if inFile == '':
		print usage
		sys.exit()

	# start extracting i-frames
	home = os.path.expanduser("~")
	ffmpeg = home + '/bin/ffmpeg'
	outFile = oString + '%03d.png'

	cmd = [ffmpeg,'-i', inFile,'-f', 'image2','-vf', 
               "select='eq(pict_type,PICT_TYPE_I)'",'-vsync','vfr',outFile]
	print cmd
	subprocess.call(cmd)

if __name__ == "__main__":
	main(sys.argv[1:])
