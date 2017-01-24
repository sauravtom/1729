import cv2
import sys
import os
import requests
import unirest
# from faceslide import faceslide_main
old_face = []
sumx = 0
sumy = 0
count = 0
def main():

	for x in os.popen("pwd"):
		video_path = x
	
	if not video_path :
		print "You are expected to run the file with video name ."

	else :
		print "The show begins"
		os.system("mkdir %s"%frames_dir)
		os.system("mkdir %s/frames"%frames_dir)
		os.system("mkdir %s/cropped_frames"%frames_dir)
		os.system("mkdir %s/intro_frames"%frames_dir)
		os.system("mkdir %s/finalvideo"%frames_dir)
		os.system("mkdir %s/notes"%frames_dir)
		os.system("mkdir %s/dump"%frames_dir)
		os.system("mkdir %s/dump/frames/"%frames_dir)
		

		#testing 
		# ffmpeg -ss 00:30:00.00 -i test.mkv -t 00:10:00.00 -vf scale=160:120 test.mkv 
		#(if don't want to cut video
		# remove the timing durartions i.e ffmpeg -i test.mkv -vf scale=160:120 test.mkv )

		os.system("ffmpeg -ss 1 -i %s -r 30 -t 600 -vf scale=640:480 -f image2 %s/frames/frame-%%07d.png"%(video,frames_dir))

		
		# os.system("ffmpeg -i %s -r 30 -vf scale=640:480 -f image2 %s/frames/frame-%%07d.png"%(video,frames_dir))

		arr = os.listdir("%s/frames"%frames_dir)
		arr.sort()

		# frames for the introduction of the video 
		try :
			os.system("ffmpeg -ss 00:02:00.00 -i %s 30 -t 00:00:10.00 -vf scale=480:320 -f image2 %s/intro_frames/new-%%03d.png"%(video,frames_dir))

		except :
			os.system("ffmpeg -ss 0.5 -i %s -t 0.5 -vf scale=480:320 -f image2 %s/intro_frames/new-%%03d.png"%(video,frames_dir))
		use_api = "no"
		avgx = 0
		avgy = 0
		for file_name in arr:
			print file_name
			if not use_api  :
				x,y= upload2("%s/frames/%s"%(frames_dir,file_name))
				w=250
				h=250
				print 'ffmpeg -i %s/frames/%s -vf "crop=%s:%s:%s:%s" %s/cropped_frames/face_%s'%(frames_dir,file_name,w,h,x,y,frames_dir,file_name)
				# os.system('ffmpeg -i %s/frames/%s -vf "crop=%s:%s:%s:%s" %s/face_frames/face_%s'%(frames_dir,file_name,w,h,x,y,frames_dir,file_name))
				os.system('ffmpeg -ss 60 -i %s/frames/%s -t 120 -vf "crop=%s:%s:%s:%s" %s/cropped_frames/face_%s'%(frames_dir,file_name,w,h,x,y,frames_dir,file_name))
			else:
				# Create the haar cascade
				faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #`
				
				# Read the image
				print '%s/%s/%s'%(frames_dir,"frames",file_name)
				image = cv2.imread('%s/frames/%s'%(frames_dir,file_name))
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

				# Detect faces in the image
				faces = faceCascade.detectMultiScale(gray,
					scaleFactor=1.1,
					minNeighbors=5,
					minSize=(150, 150),
					flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
				print "Found {0} faces!".format(len(faces))
				
				global old_face,sumx,sumy,count 
				# If face is not found then crop with the previous dimensions
				if not len(old_face) :
					if not len(faces):
						os.system('ffmpeg -i %s/frames/%s -vf "crop=250:250" %s/cropped_frames/face_%s'%(frames_dir,file_name,frames_dir,file_name))
					else :

						for (x,y,w,h) in faces:
							count = count + 1
							sumx = sumx + x
							sumy = sumy + y
							avgx = sumx/count
							avgy = sumy/count	
						try :
							old_face=[avgx-20,avgy-20,250,250]
							os.system('ffmpeg -i %s/frames/%s -vf "crop=%d:%d:250:250" %s/cropped_frames/face_%s'%(frames_dir,file_name,old_face[0],old_face[1],frames_dir,file_name))
						except :
							print "Not getting the dimension of face from the frames"

				else :
					if not len(faces):
						os.system('ffmpeg -i %s/frames/%s -vf "crop=%d:%d:250:250" %s/cropped_frames/face_%s'%(frames_dir,file_name,old_face[0],old_face[1],frames_dir,file_name))
					else :
						for (x,y,w,h) in faces:
							count = count + 1
							sumx = sumx + x
							sumy = sumy + y
							avgx = sumx/count
							avgy = sumy/count	
						try :
							old_face=[avgx-20,avgy-20,250,250]
							os.system('ffmpeg -i %s/frames/%s -vf "crop=%d:%d:250:250" %s/cropped_frames/face_%s'%(frames_dir,file_name,old_face[0],old_face[1],frames_dir,file_name))
						except :
							print "Not getting the dimension of face from the frames"

		# making the video
		try :
			os.system("ffmpeg -framerate 1/24 -r 30 -i %s/cropped_frames/face_frame-%%07d.png -vcodec libx264 -pix_fmt yuv420p %s/finalvideo/final_%s"%(frames_dir,frames_dir,video))
		except :
			print "Making the video from the cropped frames "

		#adding audio
		try :
			os.system("ffmpeg -ss 1 -i %s -t 300 %s/audio.mp3"%(video,frames_dir))
		except :
			print "the audio"

		#combining audio and video

		try :
			os.system("ffmpeg -i %s/finalvideo/final_%s -i %s/audio.mp3 -vcodec copy -acodec aac -strict experimental %s/finalvideo/compressed_%s"%(frames_dir,video,frames_dir,frames_dir,video))
			print "Compressed video done"
		except :
			print "making the compressed video"
		os.system("mv %s %s/"%(video,frames_dir))
		
if __name__ == '__main__':
	if sys.argv[1] == 'test':
		upload2('uber1/frames/frame-0000001.png')

	elif sys.argv[1] == 'api':
		video=sys.argv[2]
		frames_dir=video.split(".")[0]
		main(use_api=True)
		
	elif sys.argv[1] == 'local':
		video = sys.argv[2]
		frames_dir = video.split('.')[0]
		main()
		os.system("python faceslide1.py %s"%(video))