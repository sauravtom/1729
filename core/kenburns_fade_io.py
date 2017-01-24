from wand.image import Image
from wand.color import Color
from subprocess import Popen, PIPE, STDOUT
import time

start_time = time.time()

width = 1280
height = 720

width = 720
height = 576

img_file = 'slide_4.png'

dst = 'out.ts'

cmd = ['ffmpeg1', '-report', '-loglevel', 'info', '-y', '-f', 'image2pipe', '-vcodec', 'ppm', '-s', '%sx%s' % (width, height), '-r', '30', '-i', '-', '-vcodec', 'libx264', '-preset', 'slow', '-tune', 'stillimage', '-bsf', 'h264_mp4toannexb', '-f', 'mpegts', dst]

print cmd

p = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=STDOUT)

X = 0
Y = 0
Z = 100
zoom = False
with Image(background=Color('black'), width=width, height=height) as bg_image:
    with Image(filename=img_file) as image:
        image.transform(resize='%sx%s>' % (width, height))
        print 'w: %s, h: %s' % image.size,
        cw, ch = image.size
        """
        video duration 4 seconds
        """
        fps = 4 * 30
        fps_end = fps - 30
        image.resize(cw + fps, ch + fps)
        print 'fps:', fps,
        print '[w: %s, h: %s]' % image.size
        for i in range(fps):
            with bg_image.clone() as result:
                with image.clone() as img:
                    ox, oy =  img.size
                    #print '%s - w: %s, h: %s [X:%s, Y:%s]' % (i, ox, oy, X, Y)
                    if X >= ox:
                        X = ox - 1
                    if Y >= oy:
                        Y = oy - 1
                    img.crop(X, Y, width=int(cw), height=int(ch))
                    #print '%s - [X:%s, Y:%s] w: %s, h: %s' % (i, X, Y, cw, ch)
                    result.composite(img, (result.width - img.width) / 2, (result.height - img.height) / 2)

                    if i <= 30:
                        percentage = i / 30.0
    #                    print i, percentage
                        result.watermark(
                            image=bg_image,
                            transparency=percentage,
                            left=0,
                            top=0
                        )
                    elif i >= fps_end:
                        percentage = (fps - i) / 30.0
    #                    print i, percentage
                        result.watermark(
                            image=bg_image,
                            transparency=percentage,
                            left=0,
                            top=0
                        )

                    p.stdin.write(result.make_blob('ppm'))


                    X += 1
                    Y += 1

out, err = p.communicate()

print out, err
print "\nElapsed time: %s" % (time.time() - start_time)
