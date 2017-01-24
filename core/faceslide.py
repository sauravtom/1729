
import sys
import os
import subprocess

def main(video_file):
	video_filename = video_file.split('/')[-1]
	video_filename_no_ext = video_filename.split('.')[-1]

	#converting the video to 1x1 frames
	#os.system("ffmpeg -i %s -r 1 -f image2 -s 1x1 dump/frames/image-%%07d.png"%(video_file))

	num_arr =[]
	prev_prev_ppp =''
	prev_ppp = ''
	for filename in os.listdir("dump/frames"):
		if filename.startswith('.'):
			continue
		pixel_det  = os.popen("convert dump/frames/%s -format '%%[pixel:u]' info:-"%(filename)).readlines()[0]
		
		if not pixel_det.startswith('srgb'):
			#print "OH BOYYY "*30
			continue
		
		pixel_avg = 0
		for p in pixel_det[5:-1].split(','):
			pixel_avg = pixel_avg + int(p)
		pixel_avg = pixel_avg/3
		#print pixel_avg/3,pixel_det,filename
		if pixel_avg < 150:
			ppp = "LOWW"
		else:
			ppp = "HIGH"

		if ppp != prev_ppp:
			seconds = filename.split('-')[-1]
			seconds = seconds.split('.')[0]
			if ppp == 'LOWW':
				print "face start: %s"%(seconds)
			else:
				print "face enddd: %s"%(seconds)

			num_arr.append(seconds)
			#print "%s : %s to %s"%(filename,ppp,prev_ppp)

		prev_prev_ppp = prev_ppp
		prev_ppp = ppp

	for i in xrange(0,len(num_arr)-2,2):
		print num_arr[i],num_arr[i+1]
		start = str(int(num_arr[i]))
		end = str(int(num_arr[i+1]))
		os.system("ffmpeg -i %s -ss %s -to %s -async 1 dump/face_%s.mp4"%(video_file,start,end,start))
		os.system("ffmpeg -i dump/face_%s.mp4 -filter:v 'crop=100:100:95:60' dump/face_%s_compressed.mp4"%(start,start))



if __name__ == '__main__':
	if not sys.argv[1]:
		print "Please supply video file"
	else:
		os.system("mkdir dump/frames")
		main(sys.argv[1])
		#os.system("rm -rf dump/frames")

'''
NOTES:
Dependencies Imagemagick and FFMPEG

cut a video 
ffmpeg -i movie.mp4 -ss 30 -to 40 -async 1 cut.mp4

crop a video_file
ffmpeg -i in.mp4 -filter:v "crop=out_w:out_h:x:y" out.mp4
ffmpeg -i portion_1.mp4 -filter:v "crop=100:100:95:60"  out2.mp4


grab a frame
ffmpeg -ss 0.5 -i inputfile.mp4 -t 1 -s 480x300 -f image2 imagefile.jpg

compress a video
avconv -i myvideo.mp4 -acodec libvorbis -aq 5 -ac 2 -qmax 25 -threads 2 myvideo.webm


split an video into frames
ffmpeg -i 1_compressed.mp4 -r 1 -f image2 frames/image-%07d.png


(imagemagick)average pixel value
convert frames/image-0000420.png -resize 1x1! txt:-

'''


