

import os


shots='''
00:19,introduction
00:38,why ethereum
01:20,the problem
01:46,swiss knife
02:51,windows phone
04:06,the concept
04:13,additions
05:42,hello world in ethereum
07:42,state
09:17,code execution
11:15,important
12:34,gas
15:54,gas limit
17:24,transactions
18:55,receipts
19:45,logs
21:41,EVM
23:54,ABI
24:52,RLP,
26:07,mining algo overview
27:05,mining algo overview 2
28:59,fast block times
29:58,centralisation risks
30:43,solution
31:09,merkel trees meme
31:33,merkel trees maths
33:29,merkel trees in ethereum
34:48,merkel trees in ethereum 2
35:30,future directions

'''

def screenshot(time,name):
	os.system('ffmpeg -ss %s -i temp/slides.mp4 -vframes 1 -q:v 2 temp/%s'%(time,name))

def slicer():
	shot_list = shots.strip().split('\n')
	for i in shot_list:
		t= i.split(',')[0]
		m = t.split(':')[0]
		s = t.split(':')[1]
		seconds = int(m)*60+int(s)
		print t,m,s,seconds
		#n= i.split(',')[1]
		#n=n.replace(' ','_') + '.png'
		#n='00' + t.replace(':','') + n
		n = 'slide_%s.png'%(seconds) 
		screenshot(t,n)


if __name__ == '__main__':
	slicer()
	#screenshot('23:54','foo.png')
