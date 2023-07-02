import cv2
import sys
import numpy as np
# import keras
from event_streamer import EventStreamer


video_id = 6
ip = '127.0.0.1'
running = False

if len(sys.argv) > 1:
    video_id = int(sys.argv[1])
if len(sys.argv) > 2:
    ip = sys.argv[2]


cap = cv2.VideoCapture(video_id)
CONDITIONS = ['hover', 'touch']
WINDOW_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
WINDOW_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# this was for ERWIN, but ERWIN sucks
# model = keras.models.load_model("erwin_final")

streamer = EventStreamer(ip, WINDOW_WIDTH, WINDOW_HEIGHT)


def process_img(frame, window_w, window_h):
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contours = cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB)
    img_contours = cv2.drawContours(img_contours, contours, -1, (255, 0, 0), 3)

    for ctn in contours:
        area = cv2.contourArea(contour=ctn)
        gesture = None
        # contour not finger size
        if area < 80 or area > 3500:
            continue
        else:
            # hover / light touch has smaller area
            if 80 < area < 600:
                gesture = 'hover'
                cv2.rectangle(img_contours,(x,y),(x+w,y+h),(0,0,255),2)

            # hard touch has greater area
            elif 600 < area < 3500:
                gesture = 'touch'
                cv2.rectangle(img_contours,(x,y),(x+w,y+h),(0,255,0),2)

            
            # this was for ERWIN, but ERWIN sucks
            # if (x > window_w - 50 or x < 50 or y > window_h - 50 or y < 50):
            #    break
            M = cv2.moments(ctn)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            # draw bounding box around finger
            x,y,w,h = cv2.boundingRect(ctn)
            cv2.circle(img_contours, (cX, cY), 7, (255, 255, 255), -1)
            cv2.rectangle(img_contours,(cX-50, cY-50),(cX+50, cY+50),(0, 0, 255),2)

            # this was for ERWIN, but ERWIN sucks
            # cut = frame[cY-50:cY+50, cX-50:cX+50]
            # resized = cv2.resize(cut, (100, 100))
            # title = f'{time.time()}-hover-s.png'
            # cv2.imwrite(f'hover-data-border-test/{title}', cut)
            try:
                # this was for ERWIN, but ERWIN sucks
                # resized = cv2.resize(cut, (64, 64))
                # reshaped = resized.reshape(-1, 64, 64, 3)
                # y = model.predict(reshaped)
                # print(CONDITIONS[np.argmax(y)], np.max(y))
                # gesture = CONDITIONS[np.argmax(y)]
                # value = np.max(y)
                # print(gesture, value)
                streamer.add_to_stream(type=gesture, x=cX, y=cY, dx=0, dy=0)
            except:
                continue
    streamer.send_stream()
    return img_contours



while True:
    ret, frame = cap.read() 
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if not running:
        # at the beginning, capture average "white" of the touchscreen for finger threshold
        img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        threshold = np.bincount(img_gray.flatten()).argmax() / 2.25
    else:
        img = process_img(frame, WINDOW_WIDTH, WINDOW_HEIGHT)
    cv2.imshow('frame', img)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        running = True
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()