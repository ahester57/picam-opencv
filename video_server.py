import cv2
import numpy as np
import subprocess as sp
import sys
import threading

from datetime import datetime as dt

# use ffmpeg to deal with pipe and encode 
FFMPEG_BIN = "ffmpeg"
command = [ FFMPEG_BIN,
		'-i', '-',
		'-pix_fmt', 'bgr24',
		'-vcodec', 'rawvideo',
		'-an', '-sn',
		'-f', 'image2pipe', '-']

filename = 'log_' + dt.utcnow().strftime('%Y%m%d%H%M%S') + '.video_log'
flag_save = False
face_recognition = False
file_accumulator = []
face_cascade = cv2.CascadeClassifier('./xml/lbpcascade_frontalface.xml')
video_log_filename = 'log_20201102025939.video_log'


def save_to_file(file_accumulator):
    with open(filename, 'ab') as _:
        for fa in file_accumulator:
            _.write(b'%s\n' % fa)

def face_recognize():
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)

def start():
    global file_accumulator
    pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
    video_log = open(video_log_filename, 'rb')

    while True:
        # read from pipe, convert, reshape
        try:
            raw_image = pipe.stdout.read(960*800*3)
            #raw_image = video_log.readline()
            if flag_save:
                file_accumulator.append(raw_image)
            # add the raw image to file accumulator
            image = np.frombuffer(raw_image, dtype='uint8')
            image = image.reshape((800,960,3))
        except:
            print('oops')
            if flag_save:
                save_thread = threading.Thread(target=save_to_file, args=(file_accumulator,))
                save_thread.start()
                file_accumulator = []
                pipe.stdout.flush()
            #video_log.close()
            pipe.stdout.close()
            break;
        # show the image
        #if face_recognition:
            #face_recognize()
        cv2.imshow('video', image)

        # save to file
        if flag_save and len(file_accumulator) % 100 == 0:
            save_thread = threading.Thread(target=save_to_file, args=(file_accumulator,))
            save_thread.start()
            file_accumulator = []
            pipe.stdout.flush()

        cv2.waitKey(1)


# This 'nameguard' runs start() if this file is called directly from python
if __name__ == '__main__':
    try:
        start()
    except EOFError:
        print("^D")
    print('over and out')
    cv2.destroyAllWindows()

