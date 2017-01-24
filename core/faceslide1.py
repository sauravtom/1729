
import sys
import os
import subprocess

def faceslide_main(frames_dir,video_file):
	print "Frames_dir" , frames_dir
	print "video_file",video_file


	#onverting the video to 1x1 frames
	print "ffmpeg -i %s/finalvideo/compressed_%s -r 1 -f image2 -s 1x1 %s/dump/frames/image-%%07d.png"%(frames_dir,video_file,frames_dir)
	os.system("ffmpeg -i %s/finalvideo/compressed_%s -r 1 -f image2 -s 1x1 %s/dump/frames/image-%%07d.png"%(frames_dir,video_file,frames_dir))
	print "line 17"

	#Variables Declared
	num_arr = {"startLow":[],"startHigh":[]}
	prev_prev_ppp =''
	prev_ppp = ''
	flag = 0
	state = ""

	file_list = os.listdir("%s/dump/frames"%frames_dir)
	file_list.sort()
	for filename in file_list:
		if filename.startswith('.'):
			continue
		print "Starting with the file -->" , filename
		pixel_det  = os.popen("convert %s/dump/frames/%s -format '%%[pixel:u]' info:-"%(frames_dir,filename)).readlines()
		
		print "Length of the Pixel object" , len(pixel_det)
		if len(pixel_det):
			if not pixel_det[0].startswith('srgb'):
				#print "OH BOYYY "*30
				continue
			
			pixel_avg = 0
			count = 0
			if len(pixel_det):
				for p in pixel_det[0].split(','):
					if count == 0 :
						p = p[5:-1] + p[-1]
						print p , int(p)
					elif count == 2 :
						p = p[0:len(p)-2]
						print p , int(p)
					else :
						print p , int(p)
					count = count +1			
					pixel_avg = pixel_avg + int(p)

				pixel_avg = pixel_avg/3
				count = 0
				print pixel_avg,pixel_det,filename

				if pixel_avg < 150:
					if flag == 0 :
						state = "startLow"
					ppp = "LOWW"
				else:
					if flag == 0:
						state = "startHigh"
					ppp = "HIGH"


				if ppp != prev_ppp:
					seconds = filename.split('-')[-1]
					seconds = seconds.split('.')[0]
					if ppp == 'LOWW':
						print "face start: %s"%(seconds)
					else:
						print "face enddd: %s"%(seconds)

					num_arr[state].append(seconds)
					print "%s : %s to %s"%(filename,ppp,prev_ppp)
				prev_prev_ppp = prev_ppp
				prev_ppp = ppp
		if flag == 0 :
			flag = 1 
			print "flag" ,flag
			print state

		print "************** Different file ********** \n"


	print "line 67"
	print "flag" ,flag
	print state
	print num_arr[state]

	for i in xrange(0,len(num_arr[state])-2,2):
		print num_arr[state][i],num_arr[state][i+1]
		start = str(int(num_arr[state][i]))
		end = str(int(num_arr[state][i+1]))
		if state == "startHigh":
			print "entered High"
			try :
				for x in range(int(num_arr[state][i])+2,int(num_arr[state][i+1])-2,1):
					os.system("ffmpeg -ss %d -i %s -vf scale=320:240 -frames:v 1 -q 15 %s/notes/slide_%d.png"%(x,video_file,frames_dir,x))
			except :
				print "Its alright"		
		else :
			print "Entered low"
			try :
				for x in range(int(num_arr[state][i+1])+2,int(num_arr[state][i+2])-2,1):
					os.system("ffmpeg -ss %d -i %s -vf scale=320:240 -frames:v 1 -q 15 %s/notes/slide_%d.png"%(x,video_file,frames_dir,x))
			except :
				print "Its alright"				
		print "line 77"
		os.system("ffmpeg -i %s/finalvideo/compressed_%s -ss %s -to %s -async 1 %s/dump/face_%s.mp4"%(frames_dir,video_file,start,num_arr[state][i+2],frames_dir,start))
		os.system("ffmpeg -i %s/dump/face_%s.mp4 -vf scale=100:100 %s/notes/face_%s.mp4"%(frames_dir,start,frames_dir,start))
	# os.system("rm -rf %s/dump/frames"%frames_dir)
	# os.system("mv %s %s"%(video_file,frames_dir))
	print "line 80"
if __name__ == '__main__':
	if not sys.argv[1]:
		print "Please supply video file"
	else:
		file_name = sys.argv[1]
		frames_dir = file_name.split('/')[-1].split('.')[0]
		os.system("mkdir %s"%frames_dir)
		os.system("mkdir %s/frames"%frames_dir)
		os.system("mkdir %s/cropped_frames"%frames_dir)
		os.system("mkdir %s/intro_frames"%frames_dir)
		os.system("mkdir %s/finalvideo"%frames_dir)
		faceslide_main(frames_dir,sys.argv[1])
		
		

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



