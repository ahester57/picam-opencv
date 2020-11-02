import cv2
import subprocess as sp
import numpy as np

# use ffmpeg to deal with pipe and encode 
FFMPEG_BIN = "ffmpeg"
command = [ FFMPEG_BIN,
		'-i', '-',
		'-pix_fmt', 'bgr24',
		'-vcodec', 'rawvideo',
		'-an', '-sn',
		'-f', 'image2pipe', '-']
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)

print("begin")

#face_cascade = cv2.CascadeClassifier('./xml/lbpcascade_frontalface.xml')

while True:
    # read from pipe, convert, reshape
    try:
        raw_image = pipe.stdout.read(960*800*3)
        image = np.fromstring(raw_image, dtype='uint8')
        image = image.reshape((800,960,3))
    except:
        print("oops")
        pipe.close()
        continue;
    # show the image
    if image is not None:
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #gray = image
        #faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        #for (x,y,w,h) in faces:
        #	cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
        cv2.imshow('video', image)
    else:
        # frame not ready yet
        print("frame not ready")
        cv2.waitKey(100)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    pipe.stdout.flush()

print("over and out")
cv2.destroyAllWindows()
